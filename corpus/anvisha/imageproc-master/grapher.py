import matplotlib.pyplot as plt 

#plots bar graphs with multiple y input lists
def bar_graph(x_values, list_of_y_values, colors=['r', 'y', 'b', 'g', 'c'], x_label="", y_label=""):

	fig = plt.figure()
	ax = fig.add_subplot(111)
	width = 1/(1.5*len(list_of_y_values))
	for i in range(len(val_lists)):
		ax.bar([x+i*width for x in x_values], list_of_y_values[i], width, color=colors[i%4])
	ax.set_ylabel(y_label)
	ax.set_xlabel(x_label)
	plt.show()

	return plt