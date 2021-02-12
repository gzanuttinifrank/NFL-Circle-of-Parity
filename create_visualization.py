import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def create_circle_viz(final_path, score_graph, year, save):

	# Create list of edges from the path (circle) returned by the solver, for both the inner and outer circle
	final_path_edges = []
	score_labels = {}
	for i in range(len(final_path)-1):
	    new_edge = (final_path[i],final_path[i+1])
	    final_path_edges.append(new_edge)
	    score_labels[new_edge] = score_graph[new_edge][1] + '\n' + score_graph[new_edge][0]

	final_path_reversed = final_path[::-1]

	# Add nodes and edges to the outer graph, along with the team logos as node images
	G = nx.DiGraph()
	for tm in final_path_reversed[:-1]:
	    img = mpimg.imread('team_logos/'+'_'.join(tm.lower().split(' '))+'.png')
	    G.add_node(tm, image = img)
	G.add_edges_from(final_path_edges)

	fig = plt.figure(figsize=(20,20))
	pos = nx.circular_layout(G)
	ax = plt.subplot(111)
	ax.set_aspect('equal')

	# Draw inner circle with score results as edge labels with no nodes
	pos_scores = nx.circular_layout(G, scale=0.85)
	nx.draw_networkx_edge_labels(G, pos_scores, edge_labels=score_labels, font_color='blue', font_size=14, rotate=False)

	plt.xlim(-1.3,1.3)
	plt.ylim(-1.3,1.3)

	trans = ax.transData.transform
	trans2 = fig.transFigure.inverted().transform

	# Draw outer circle with team logos as nodes
	# https://stackoverflow.com/questions/53967392/creating-a-graph-with-images-as-nodes
	piesize = 0.05 # this is the image size
	p2 = piesize/2
	for n in G:
	    xx, yy = trans(pos[n]) # figure coordinates
	    xa, ya = trans2((xx,yy)) # axes coordinates
	    a = plt.axes([xa-p2,ya-p2, piesize, piesize])
	    a.set_aspect('equal')
	    a.imshow(G.nodes[n]['image'])
	    a.axis('off')
	    
	# Add images and writing inside of the cirlces
	arrow_img = mpimg.imread('team_logos/circular_arrows.png')
	arrow_size = 0.43
	a = plt.axes([0.3, 0.3, arrow_size, arrow_size])
	a.set_aspect('equal')
	a.imshow(arrow_img)
	a.axis('off')

	nfl_img = mpimg.imread('team_logos/nfl_logo.png')
	nfl_size = 0.27
	a = plt.axes([0.38, 0.32, nfl_size, nfl_size])
	a.set_aspect('equal')
	a.imshow(nfl_img)
	a.text(0, -250, 'NFL Circle of Parity', fontsize=30)
	a.text(425, -50, str(year), fontsize=30)
	a.axis('off')

	ax.axis('off')

	if save:
		plt.savefig(str(year)+'_Circle_of_Parity.png')
		
	plt.show()

