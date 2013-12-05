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

def dot_products():
	f = open("results.txt")
	exec(f)
	master = []
	for i in range(4):
		for pkg in results[i][1]:
			if pkg not in master:
				master.append[pkg]
		
