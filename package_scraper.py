import re

def package_scraper(filename):
	f = open(filename)
	text= f.read()
	regex_string = ">(\w+)&nbsp;(.+)</a></td>"
	list_of_packages=[]
	#regex_string = "<td><a \w+>(\w+)&nbsp;(\w+)</a></td>"

	for m in re.finditer(regex_string, text):
		list_of_packages.append(m.group(1))

	return list_of_packages

def generate_standard_library():
	import distutils.sysconfig as sysconfig
	import os
	list_of_packages = []
	std_lib = sysconfig.get_python_lib(standard_lib=True)
	for top, dirs, files in os.walk(std_lib):
		for nm in files:
			if nm != '__init__.py' and nm[-3:] == '.py':
				print nm
				list_of_packages.append(os.path.join(top, nm)[len(std_lib)+1:-3].replace('\\','.'))
	return list_of_packages