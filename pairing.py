import operator

def top_modules():
	f = open("results.txt")
	exec(f)
	master = {}
	for name,stats in results:
		for m in stats:
			if m not in master:
				master[m] = stats[m]
			else:
				master[m] += stats[m]
	master = sorted(master.iteritems(), key=operator.itemgetter(1), reverse=True)
	lookup_dict = {}
	for i in range(15):
		lookup_dict[master[i][0]] = i

	print lookup_dict
	master_names = [(entry[0], [0]*15) for entry in results]
	for pkg in lookup_dict:
		for i in range(4):
			name = results[i][0]
			stats = results[i][1]
			if pkg in stats:
				master_names[i][1][lookup_dict[pkg]]= stats[pkg]
	return master_names

def vectors():
	vector = {'db': 0,
	'models': 1,
	'util': 2,
	'os': 3,
	're': 4,
	'httplib2': 5,
	'socket': 6,
	'config': 7,
	'urllib': 8,
	'simplejson': 9,
	'numpy': 10,
	'oauth2client':11,
	'json': 12,
	'logging': 13,
	'random': 14}

