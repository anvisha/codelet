$(function() {
var make_tweet = function(event, ui) {
    var goalname = $('#goalname').val();
    var hashtag = $('#hashtag').val();

    //set values of stuff in the hidden div here

    var tweet_text = "I'm trying to form a habit with @habitbot. My goal is to "+goalname+". "+hashtag;
    $('.modal-body #firsttweet').val(tweet_text);
}

var send_and_save = function(event, ui) {
    $('#firsttweet').val($('#tweet').val());
    $('#creategoal').submit();
}

console.log("using maketweet")
$('.inline').click(make_tweet);
$('.sendnsave').click(send_and_save);


})
 