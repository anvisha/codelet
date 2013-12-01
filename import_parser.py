from modulefinder import ModuleFinder
import re
import inspect

def get_modules(filename):
	finder = ModuleFinder()
	finder.run_script(filename)

	list_modules = {}

	for name,mod in finder.modules.iteritems():
		print name,mod

	return list_modules

def parse(filename):
	f = open(filename)
	text=f.read()
	pkgs = {}
	#import [pkg] as [alias]
	for m in re.finditer("import (\w+) as (\w+)", text):
		pkg = m.group(1)
		alias = m.group(2)
		pkgs[pkg] = find_function_calls(alias, None, text)

	#import [pkg]
	for m in re.finditer("import (\w+)\n", text):
		pkg = m.group(1)
		pkgs[pkg] = find_function_calls(pkg, None, text)

	#from [pkg] import [sub,sub,sub...]
	for m in re.finditer("from (\w+) import (.+)", text):
		pkg = m.group(1)
		subs = m.group(2).split(",")
		total_count = 0
		for sub in subs:
			if sub!="*":
				total_count += find_function_calls(None, sub.strip(), text)
			else:
				total_count+=1
		pkgs[pkg] = total_count
	return pkgs

def find_function_calls(pkg, function, text):
	call_count = 0
	if function == None and pkg!="*":
		for calls in re.finditer(pkg, text):
			call_count +=1
		return max(0,call_count-1)
	elif pkg==None and function!="*":
		for calls in re.finditer(function, text):
			call_count+=1
		return max(0,call_count-1)
	else:
		return 1


def function_analysis(filename):
	pkgs = parse(filename)
	modules = [(x,0) for x in pkgs]
	modules = dict(modules)

	f = open(filename)
	text= f.read()

	#find all occurrences of functions
	for m in re.finditer("(\w+)\(", text):
		if(m.group()!=None):
			print inspect.getmodule(m.group())
			module = inspect.getmodule(m.group())[:-1]
			if module in modules:
				modules[module] = modules[module] + 1

	return modules

