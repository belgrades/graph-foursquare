import foursquare
import networkx as nx
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt
import json

CLIENT_ID = "MZEDB1RKLWFVBRYQSE5LFIB4N23J0Q41FIKLNLCHBGCNL2RK"
CLIENT_SECRET = "PY1KYPH030GLKG54OLO3ULB5BYYPE4CAV14S1IGU3FS2YKT1"

client = foursquare.Foursquare(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

res = client.venues("4c31a1e26f1fef3b440dec3d")

name = res["venue"]["name"]
hours = res["venue"]["hours"]
popular = res["venue"]["popular"]
lat = res["venue"]["location"]["lat"]
lng = res["venue"]["location"]["lng"]

print(name)
print(hours)
print(popular)
print(lat)
print(lng)

print("<<< {} >>>".format('search 1' ))

search = client.venues.explore(params={'ll':'41.89,12.50'})

for group in search['groups']:
    print(group["name"])
    for nv in group['items']:
        print(nv["venue"]["name"])

search = client.venues.explore(params={'near':'Rome, Italy'})

print("<<< {} >>>".format('search 2'))

for group in search['groups']:
    print(group["name"])
    for nv in group['items']:
        print(nv["venue"]["name"])

search = client.venues.explore(params={'near':'Rome, Italy','query':'transtevere'})

print("<<< {} >>>".format('search 3'))

for group in search['groups']:
    print(group["name"])
    for nv in group['items']:
        print(nv["venue"]["name"])

search = client.venues.explore(params={'near':'Rome, Italy','query':'joe\'s coffee'})

print("<<< {} >>>".format('Joes Coffee'))

nearest = ''
dist_min = 99999 

for group in search['groups']:
    print(group["name"])
    for nv in group['items']:
        print(nv["venue"]["name"])
        new_dist = (lat-nv["venue"]["location"]["lat"])**2 + (lng-nv["venue"]["location"]["lng"])**2 
        if new_dist < dist_min:
            dist_min = new_dist
            nearest = nv["venue"]["name"]

print("Nearest venue is {}".format(nearest))

'''
print("<<< {} >>>".format('Using next and sets'))

next_venues = client.venues.nextvenues("4c31a1e26f1fef3b440dec3d")

for nv in next_venues['nextVenues']['items']:
    print(nv["name"])

unexplored = set()
search = client.venues.explore(params={'near':'Rome, Italy'})

for item in search['venues']:
    unexplored.add(item["id"])

for node in unexplored:
    # lookup next venues
    unexplored.remove(node)
'''

print("<<< >>>")
print("<<< {} >>>".format('Creating graph'))

places = nx.DiGraph()
unexplored = set()

explore = client.venues.explore(params={'near':'Rome, Italy'})

for venue in explore["groups"][0]["items"]:
    item = venue["venue"]
    unexplored.add(item["id"])
    places.add_node(int(item["id"], 16), id=item["id"], name=item["name"], lat=item["location"]["lat"], long=item["location"]["lng"], tipCount=item["stats"]["tipCount"], checkinsCount=item["stats"]["checkinsCount"], usersCount=item["stats"]["usersCount"])
    print("unexplored: ", len(unexplored), " - total venues: ", len(places.nodes()), " - total links: ", len(places.edges()), "visiting: ", item["name"])

while unexplored:
    key = unexplored.pop()
    next_venues = client.venues.nextvenues(key)
    keyInt = int(key, 16)
    node = places.node[keyInt]
    print("unexplored: ", len(unexplored), " - total venues: ", len(places.nodes()), " - total links: ", len(places.edges()), "visiting: ", node["name"], "[new found: ", len(next_venues['nextVenues']['items']),"]")
    
    for item in next_venues['nextVenues']['items']:
        unexplored.add(item["id"])
        places.add_node(int(item["id"], 16), id=item["id"], name=item["name"], lat=item["location"]["lat"], long=item["location"]["lng"], tipCount=item["stats"]["tipCount"], checkinsCount=item["stats"]["checkinsCount"], usersCount=item["stats"]["usersCount"])

    places.add_edge(int(item["id"], 16), int(key, 16))
    
    
    print("\tunexplored: ", len(unexplored), " - total venues: ", len(places.nodes()), " - total links:", len(places.edges()), "visiting: ", item["name"])
    if len(places.nodes())>300:
        break

# Getting pos tuple
for node in places.nodes():
    places.node[node]['pos'] = (places.node[node]['long'], places.node[node]['lat'])

plt.clf()
nx.draw_networkx_nodes(places, nx.get_node_attributes(places, 'pos'))
nx.draw_networkx_edges(places, nx.get_node_attributes(places, 'pos'), width=0.2, alpha=0.5)
plt.show()

data = json_graph.node_link_data(places)

with open('graph.json', 'w') as outfile:
    json.dump(data, outfile)
