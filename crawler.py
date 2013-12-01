import os
import import_parser as ip

def crawl_dir(dirname):
	babies = []
	for root, dirs, files in os.walk(dirname):
		for f in files:
			if f[-2:]=="py":
				babies.append((root, f))
	return babies

def get_metrics(dirname):
	package_file = open('pypi_list.txt')
	exec(package_file) #package_list is name of the master list of public python modules
	std_package_file = open('std_packages.txt')
	exec(std_package_file) #std_package_list
	babies = crawl_dir(dirname) 
	filenames = []
	excluded=[]
	all_imports = {}
	for (root,f) in babies:
		imports = ip.parse(root+"/"+f)
		filenames.append(f[:-3])
		for m in imports:
			if m in package_list or m in std_package_list:
				if m in all_imports:
					all_imports[m] += 1
				else:
					all_imports[m] = 1
			else:
				excluded.append(m)
	print excluded
	return all_imports

def write_metrics():
	f = open('results.txt','w')
	p = open('intersects.txt', 'w')
	path = '/Users/anvisha/corpus/'
	names = ['anvisha', 'danielle', 'rob', 'philip']
	metrics = [(name,get_metrics(name)) for name in names]
	for name in names:
		metrics = get_metrics(path+name)
		f.write(name+'\n')
		f.write(str(metrics))
	print metrics
	#for i in range(4):
	#	for j in range(i+1,4):
	#		inter_set = set(metrics[i][1]) & set(metrics[j][1])
	#		p.write(metrics[i][0]+" "+metrics[j][0]+"\n\n")
	#		p.write(str(inter_set))