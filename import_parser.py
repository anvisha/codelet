from modulefinder import ModuleFinder
import re
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
	pkgs = []
	#import x
	for m in re.finditer("from (\w+) import (\w+)|(\*)|import (\w+)", text):
		if(m.group(1) != None):
			if(m.group(2) != None):
				pkgs.append(m.group(1)+"."+m.group(2))
			elif(m.group(3)!=None):
				pkgs.append(m.group(1))
		#from \w+ import *
		elif(m.group(4)!= None):
			pkgs.append(m.group(4))
	return pkgs

