f = open("results.txt")
exec(f)
for name,stats in results:
	statfile = open("stats/"+name+".txt", 'w')
	statfile.write("{\"name\":\""+name+"\", \"children\":[")
	for m in stats:
		statfile.write("{\"name\":\""+m+"top"+"\", \"children\":[{\"name\": \""+ m+"\", \"size\":"+str(stats[m])+"}]},")
	statfile.write("]}")