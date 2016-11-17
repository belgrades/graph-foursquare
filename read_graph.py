import foursquare
import networkx as nx
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt
import json

with open('graph.json') as data_file:    
    data = json.load(data_file)

places = json_graph.node_link_graph(data)

plt.clf()
nx.draw_networkx_nodes(places, nx.get_node_attributes(places, 'pos'))
nx.draw_networkx_edges(places, nx.get_node_attributes(places, 'pos'), width=0.2, alpha=0.5)
plt.show()



