# -*- coding: utf-8 -*-
import types
from django.core.urlresolvers import get_callable
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseServerError, HttpResponseForbidden, HttpResponseNotAllowed
from django.utils import simplejson
from django.shortcuts import render, get_object_or_404, render_to_response 
from django.template import RequestContext, Context, loader
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings
from django.template import RequestContext

from django.contrib.auth.decorators import login_required

from models import *
from settings import *

from review.models import Comment, Vote

@login_required
def view(request, wiki_url):
    
    (article, path, err) = fetch_from_url(request, wiki_url)
    if err:
        return err
        
    perm_err = check_permissions(request, article, check_read=True)
    if perm_err:
        return perm_err
    c = RequestContext(request, {'wiki_article': article,
                                 'wiki_write': article.can_write_l(request.user),
                                 'wiki_attachments_write': article.can_attach(request.user),
                                 } )
    # get related articles
    
    articles = [x for x in Article.objects.all() if not x == Article.get_root()]
    revisions = Revision.objects.filter(article__exact = article).order_by("revision_date")
    contributors = []
    for revision in revisions:
        if revision.revision_user not in contributors:
            contributors.append(revision.revision_user)
    num_uses_total = Comment.objects.filter(text__icontains='#' + article.slug).count()
    current_semester_comments = Comment.objects.filter(chunk__file__submission__milestone__assignment__semester="FA12",
                                                       text__icontains = "#" + article.slug).distinct().exclude(author__username = "checkstyle")
    
    review_data = view_helper(current_semester_comments[0:15])
    commenters = User.objects.filter(comments__chunk__file__submission__milestone__assignment__semester="FA12",
                                     comments__text__icontains = "#" + article.slug).exclude(username="checkstyle").distinct()
    num_checkstyle_uses_semester = Comment.objects.filter(chunk__file__submission__milestone__assignment__semester="FA12",
                                                          text__icontains = "#" + article.slug,
                                                          author__username = "checkstyle").count()
    
    return render(request, "simplewiki/simplewiki_view.html", {
                           'wiki_article': article,
                           'wiki_write': True,
                           # 'wiki_write': article.can_write_l(request.user),
                           'wiki_attachments_write': article.can_attach(request.user),
                           'view': 'read',
                           'review_data': review_data,
                           'articles': articles,
                           'contributors': contributors,
                           'num_student_uses_semester': len(current_semester_comments),
                           'num_uses_total': num_uses_total,
                           'commenters': commenters,
                           'num_checkstyle_uses_semester': num_checkstyle_uses_semester,
    })
    # return render_to_response('simplewiki_view.html', c)
    
def view_helper(comments):
    review_data = []
    for comment in comments:
        if comment.is_reply():
            #false means not a vote activity
            review_data.append(("reply-comment", comment, comment.generate_snippet(), False, None))
        else:
            review_data.append(("new-comment", comment, comment.generate_snippet(), False, None))
    review_data = sorted(review_data, key=lambda element: element[1].modified, reverse = True)
    return review_data

@login_required
def list_all(request):
    articles = None
    try:
        # get all articles besides root
        articles = Article.objects.exclude(id=Article.get_root().id)
    except:
        pass
    return render(request, 'simplewiki/simplewiki_all.html', {
            'articles': articles
    })
    
@login_required
def comment_test(request):
    hashtags = {'repexposure': 'http://www.google.com/',
                'import': 'http://www.yahoo.com/'}
    articles = Article.objects.exclude(id=Article.get_root().id)
    return render(request, 'simplewiki/auto.html', {
                           'hashtags': hashtags,
                           'articles': articles,
    })

@login_required
def root_redirect(request):
    """
    Reason for redirecting:
    The root article needs to to have a specific slug
    in the URL, otherwise pattern matching in urls.py will get confused.
    I've tried various methods to avoid this, but depending on Django/Python
    versions, regexps have been greedy in two different ways.. so I just
    skipped having problematic URLs like '/wiki/_edit' for editing the main page.
    #benjaoming
    """
    try:
        root = Article.get_root()
    except:
        err = not_found(request, 'mainpage')
        return err

    return HttpResponseRedirect(reverse('simplewiki/wiki_view', args=(root.slug,)))

@login_required
def create(request, wiki_url):
    
    url_path = get_url_path(wiki_url)

    if url_path != [] and url_path[0].startswith('_'):
            c = RequestContext(request, {'wiki_err_keyword': True,
                                         'wiki_url': '/'.join(url_path) })
            return render_to_response('simplewiki/simplewiki_error.html', c)        

    # Lookup path
    try:
        # Ensure that the path exists...
        root = Article.get_root()
        # Remove root slug if present in path
        if url_path and root.slug == url_path[0]:
            url_path = url_path[1:]
        
        path = Article.get_url_reverse(url_path[:-1], root)
        if not path:
            c = RequestContext(request, {'wiki_err_noparent': True,
                                         'wiki_url_parent': '/'.join(url_path[:-1]) })
            return render_to_response('simplewiki/simplewiki_error.html', c)
        
        perm_err = check_permissions(request, path[-1], check_locked=False, check_write=True)
        if perm_err:
            return perm_err
        # Ensure doesn't already exist
        article = Article.get_url_reverse(url_path, root)
        if article:
            return HttpResponseRedirect(reverse('wiki_view', args=(article[-1].get_url(),)))
    
        # TODO: Somehow this doesnt work... 
        #except ShouldHaveExactlyOneRootSlug, (e):
    except:
        if Article.objects.filter(parent=None).count() > 0:
            return HttpResponseRedirect(reverse('wiki_view', args=('',)))
        # Root not found...
        path = []
        url_path = [""]

    if request.method == 'POST':
        f = CreateArticleForm(request.POST)
        if f.is_valid():
            article = Article()
            article.slug = url_path[-1]
            if not request.user.is_anonymous():
                article.created_by = request.user
            article.title = f.cleaned_data.get('title')
            if path != []:
                article.parent = path[-1]
            a = article.save()
            new_revision = f.save(commit=False)
            if not request.user.is_anonymous():
                new_revision.revision_user = request.user
            new_revision.article = article
            new_revision.save()
            import django.db as db
            return HttpResponseRedirect(reverse('wiki_view', args=(article.get_url(),)))
    else:
        f = CreateArticleForm(initial={'title':request.GET.get('wiki_article_name', url_path[-1]),
                                       'contents':_('Headline\n===\n\n')})
        
    c = RequestContext(request, {'wiki_form': f,
                                 'wiki_write': True,
                                 'slug': request.GET.get('wiki_article_name', url_path[-1]),
                                 'view': 'create',
                                 })

    return render_to_response('simplewiki/simplewiki_create.html', c)

@login_required
def edit(request, wiki_url):

    (article, path, err) = fetch_from_url(request, wiki_url)
    if err:
        return err

    # Check write permissions
    perm_err = check_permissions(request, article, check_write=True, check_locked=True)
    if perm_err:
        return perm_err

    if WIKI_ALLOW_TITLE_EDIT:
        EditForm = RevisionFormWithTitle
    else:
        EditForm = RevisionForm
    
    if request.method == 'POST':
        f = EditForm(request.POST)
        if f.is_valid():
            new_revision = f.save(commit=False)
            new_revision.article = article
            # Check that something has actually been changed...
            if not new_revision.get_diff():
                return (None, HttpResponseRedirect(reverse('wiki_view', args=(article.get_url(),))))
            if not request.user.is_anonymous():
                new_revision.revision_user = request.user
            new_revision.save()
            if WIKI_ALLOW_TITLE_EDIT:
                new_revision.article.title = f.cleaned_data['title']
                new_revision.article.save()
            return HttpResponseRedirect(reverse('wiki_view', args=(article.get_url(),)))
    else:
        f = EditForm({'contents': article.current_revision.contents, 'title': article.title})
    c = RequestContext(request, {'wiki_form': f,
                                 'wiki_write': True,
                                 'wiki_article': article,
                                 'wiki_attachments_write': article.can_attach(request.user),
                                 'view': 'edit',
                                 })

    return render_to_response('simplewiki/simplewiki_edit.html', c)

@login_required
def history(request, wiki_url, page=1):

    (article, path, err) = fetch_from_url(request, wiki_url)
    if err:
        return err

    perm_err = check_permissions(request, article, check_read=True)
    if perm_err:
        return perm_err

    page_size = 10
    
    try:
        p = int(page)
    except ValueError:
        p = 1
   
    history = Revision.objects.filter(article__exact = article).order_by('-counter')
    
    if request.method == 'POST':
        if request.POST.__contains__('revision'):
            perm_err = check_permissions(request, article, check_write=True, check_locked=True)
            if perm_err:
                return perm_err
            try:
                r = int(request.POST['revision'])
                article.current_revision = Revision.objects.get(id=r)
                article.save()
            except:
                pass
            finally:
                return HttpResponseRedirect(reverse('wiki_view', args=(article.get_url(),)))
    
    page_count = (history.count()+(page_size-1)) / page_size
    if p > page_count:
        p = 1
    beginItem = (p-1) * page_size
    
    next_page = p + 1 if page_count > p else None
    prev_page = p - 1 if p > 1 else None
    
    c = RequestContext(request, {'wiki_page': p,
                                 'wiki_next_page': next_page,
                                 'wiki_prev_page': prev_page,
                                 'wiki_write': article.can_write_l(request.user),
                                 'wiki_attachments_write': article.can_attach(request.user),
                                 'wiki_article': article,
                                 'wiki_history': history[beginItem:beginItem+page_size],
                                 'view': 'history',
                                 })
                                 

    return render_to_response('simplewiki/simplewiki_history.html', c)

@login_required
def search_articles(request, wiki_url):
    if request.method == 'POST':
        querystring = request.POST['value'].strip()
        results = [x for x in Article.objects.filter(slug__icontains=querystring)];
        results += [x for x in Article.objects.filter(current_revision__contents__icontains=querystring) if x not in results];
        if querystring.startswith("#"):
            results += [x for x in Article.objects.filter(slug__icontains=querystring[1:])]
        results = [x for x in results if not x == Article.get_root()]
        
        results_data = []
        text_radius = 50
        for result in results:
            if querystring.lower() in result.slug.lower():
                results_data.append((result, '', ''))
            elif querystring.lower() in result.current_revision.contents.lower():
                contents = result.current_revision.contents.lower().replace("\#", "#")
                index = contents.index(querystring.lower())
                lowIndex = max(0, index - text_radius)
                highIndex = min(len(contents), index + len(querystring) + text_radius)
                before = contents[lowIndex: index]
                after = contents[index + len(querystring): highIndex]
                results_data.append((result, before, after))
        c = RequestContext(request, {'wiki_search_results': results,
                                     'wiki_search_query': querystring,
                                     'results_data': results_data,
                                     })
        return render_to_response('simplewiki/simplewiki_searchresults.html', c)
    return view(request, wiki_url)

@login_required
def search_add_related(request, wiki_url):

    (article, path, err) = fetch_from_url(request, wiki_url)
    if err:
        return err

    perm_err = check_permissions(request, article, check_read=True)
    if perm_err:
        return perm_err

    search_string = request.GET.get('query', None)
    self_pk = request.GET.get('self', None)
    if search_string:
        results = []
        related = Article.objects.filter(title__istartswith = search_string)
        others = article.related.all()
        if self_pk:
            related = related.exclude(pk=self_pk)
        if others:
            related = related.exclude(related__in = others)
        related = related.order_by('title')[:10]
        for item in related:
            results.append({'id': str(item.id),
                            'value': item.title,
                            'info': item.get_url()})
    else:
        results = []
    
    json = simplejson.dumps({'results': results})
    return HttpResponse(json, mimetype='application/json')

@login_required
def add_related(request, wiki_url):

    (article, path, err) = fetch_from_url(request, wiki_url)
    if err:
        return err
    
    perm_err = check_permissions(request, article, check_write=True, check_locked=True)
    if perm_err:
        return perm_err
    
    try:
        related_id = request.POST['id']
        rel = Article.objects.get(id=related_id)
        has_already = article.related.filter(id=related_id).count()
        if has_already == 0 and not rel == article:
            article.related.add(rel)
            article.save()
    except:
        pass
    finally:
        return HttpResponseRedirect(reverse('wiki_view', args=(article.get_url(),)))

def remove_related(request, wiki_url, related_id):

    (article, path, err) = fetch_from_url(request, wiki_url)
    if err:
        return err

    perm_err = check_permissions(request, article, check_write=True, check_locked=True)
    if perm_err:
        return perm_err

    try:
        rel_id = int(related_id)
        rel = Article.objects.get(id=rel_id)
        article.related.remove(rel)
        article.save()
    except:
        pass
    finally:
        return HttpResponseRedirect(reverse('wiki_view', args=(article.get_url(),)))

@login_required
def random_article(request, wiki_url):
    from random import randint
    num_arts = Article.objects.count()
    article = Article.objects.all()[randint(0, num_arts-1)]
    return HttpResponseRedirect(reverse('wiki_view', args=(article.get_url(),)))

@login_required
def encode_err(request, url):
    return render_to_response('simplewiki/simplewiki_error.html',
                              RequestContext(request, {'wiki_err_encode': True}))

@login_required   
def not_found(request, wiki_url):
    """Generate a NOT FOUND message for some URL"""
    return render_to_response('simplewiki/simplewiki_error.html',
                              RequestContext(request, {'wiki_err_notfound': True,
                                                       'wiki_url': wiki_url}))

def get_url_path(url):
    """Return a list of all actual elements of a url, safely ignoring
    double-slashes (//) """
    return filter(lambda x: x!='', url.split('/'))

def fetch_from_url(request, url):
    """Analyze URL, returning the article and the articles in its path
    If something goes wrong, return an error HTTP response"""

    err = None
    article = None
    path = None
    
    url_path = get_url_path(url)

    try:
        root = Article.get_root()
    except:
        err = not_found(request, '')
        return (article, path, err)

    if url_path and root.slug == url_path[0]:
        url_path = url_path[1:]

    path = Article.get_url_reverse(url_path, root)
    if not path:
        err = not_found(request, '/' + '/'.join(url_path))
    else:
        article = path[-1]
    return (article, path, err)


def check_permissions(request, article, check_read=False, check_write=False, check_locked=False):
    read_err = check_read and not article.can_read(request.user)
    write_err = check_write and not article.can_write(request.user)
    locked_err = check_locked and article.locked

    if read_err or write_err or locked_err:
        c = RequestContext(request, {'wiki_article': article,
                                     'wiki_err_noread': read_err,
                                     'wiki_err_nowrite': write_err,
                                     'wiki_err_locked': locked_err,})
        # TODO: Make this a little less jarring by just displaying an error
        #       on the current page? (no such redirect happens for an anon upload yet)
        # benjaoming: I think this is the nicest way of displaying an error, but
        # these errors shouldn't occur, but rather be prevented on the other pages.
        return render_to_response('simplewiki/simplewiki_error.html', c)
    else:
        return None

####################
# LOGIN PROTECTION #
####################

if WIKI_REQUIRE_LOGIN_VIEW:
    view            = login_required(view)
    history         = login_required(history)
    search_related  = login_required(search_related)
    wiki_encode_err = login_required(wiki_encode_err)
    
if WIKI_REQUIRE_LOGIN_EDIT:
    create          = login_required(create)
    edit            = login_required(edit)
    add_related     = login_required(add_related)
    remove_related  = login_required(remove_related)

if WIKI_CONTEXT_PREPROCESSORS:
    settings.TEMPLATE_CONTEXT_PROCESSORS = settings.TEMPLATE_CONTEXT_PROCESSORS + WIKI_CONTEXT_PREPROCESSORS
