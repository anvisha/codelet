
f = open('results_new.txt')
exec(f)
package_set = []

for (name, imports) in results:
	for m in imports.keys():
		package_set.append(m)

package_set = set(package_set)

g = open('packages.txt', 'w')

g.write(str(package_set))

# f= open('colors.txt')
# g = open('colors_edited.txt', 'w')
# text = f.read()

# colors = text.split()

# for i in colors:
# 	g.write("\""+str(i)+"\""+",")


