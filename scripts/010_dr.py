from compas.geometry import Point
from compas.geometry import Vector
from compas.artists import Artist
from compas.numerical import dr

from compas_ita21.datastructures import Cablenet

# ==============================================================================
# Make Network
# ==============================================================================

network = Cablenet()

a = network.add_node(x=0, y=0, z=0, is_anchor=True)
b = network.add_node(x=10, y=0, z=10, is_anchor=True)
c = network.add_node(x=10, y=10, z=0, is_anchor=True)
d = network.add_node(x=0, y=10, z=10, is_anchor=True)

e = network.add_node(x=5, y=5, z=0)

network.add_edge(a, e)
network.add_edge(b, e, qpre=1.0)
network.add_edge(c, e)
network.add_edge(d, e)

# ==============================================================================
# Dynamic Relaxation
# ==============================================================================

xyz = network.nodes_attributes(['x', 'y', 'z'])
edges = list(network.edges())
fixed = list(network.nodes_where({'is_anchor': True}))
loads = network.nodes_attributes(['px', 'py', 'pz'])
qpre = network.edges_attribute('qpre')
fpre = network.edges_attribute('fpre')

result = dr(xyz, edges, fixed, loads, qpre=qpre, fpre=fpre, kmax=100)

for node in network.nodes():
    network.node_attributes(node, ['x', 'y', 'z'], result[0][node])
    network.node_attribute(node, 'residual', Vector(* result[-1][node]))

# ==============================================================================
# Viz
# ==============================================================================

artist = Artist(network, layer="ITA21::L6::FormFinding")

nodecolor = {node: (255, 0, 0) for node in network.nodes_where({'is_anchor': True})}

artist.clear_layer()
artist.draw(nodecolor=nodecolor)

for node in network.nodes():
    point = Point(* network.node_coordinates(node))
    residual = network.node_attribute(node, 'residual')

    if residual.length < 0.01:
        continue

    if network.node_attribute(node, 'is_anchor'):
        artist = Artist(residual.scaled(-1), color=(0, 255, 0), layer="ITA21::L6::FormFinding")
    else:
        artist = Artist(residual, color=(0, 255, 255), layer="ITA21::L6::FormFinding")

    artist.draw(point=point)

# this is necessary to avoid that Rhino on Mac freezes up
# when you use the built-in editor to run this script
Artist.redraw()
