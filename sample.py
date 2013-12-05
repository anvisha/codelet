import re

def find_hello(text):
	for m in re.finditer("hello", text):
		print "Found instance of hello in text"