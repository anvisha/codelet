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

