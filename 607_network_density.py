from qgis.core import QgsProject
from qgis.PyQt.QtCore import QVariant
import processing

#load projet
project = QgsProject.instance()
print(project.fileName())

def layer(path_to_layer,name_layer):
    vlayer = QgsVectorLayer(path_to_layer,name_layer,"ogr")
    QgsProject.instance().addMapLayer(vlayer)
    return vlayer

##########################################################
#load road network
#random two points
#caculate distance
#caculate shortest path
#return Detour index


#load road network
path_to_route_layer  = "G:/607/route_clip.shp"
route_layer = layer (path_to_route_layer,"route_layer")

#random two points
path_to_two_points  = "G:/607/two_points.shp"
processing.run("qgis:randompointsalongline", {'INPUT': route_layer,'POINTS_NUMBER':2,'OUTPUT':path_to_two_points })
two_points = layer (path_to_two_points,"two_points")

features = two_points.getFeatures()
points =[]
for feature in features:
    geom = feature.geometry()
    geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
    if geom.type() == QgsWkbTypes.PointGeometry:
        # the geometry type can be of single or multi type
        if geomSingleType:
            x = geom.asPoint()
            points.append(x)
        else:
            x = geom.asMultiPoint()
            points.append(x)

#caculate distance
Straight_dist = points[0].distance(points[1])

#caculate shortest path
path_to_shortest_path = "G:/607/shortest_path.shp"
processing.run("native:shortestpathpointtopoint", {'INPUT':route_layer,'STRATEGY':0,'START_POINT':points[0],'END_POINT' : points[1], 'OUTPUT': path_to_shortest_path})
shortest_path = layer (path_to_shortest_path,"shortest_path")
features = shortest_path.getFeatures()

network_dist=0
for feature in features:
    geom = feature.geometry()
    geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
    if geom.type() == QgsWkbTypes.LineGeometry:
        if geomSingleType:
            network_dist=geom.length()
        else:
            network_dist=geom.length()

#return Detour index
Detour_index = Straight_dist / network_dist
print ('Straight_dist: ', Straight_dist)
print ('network_dist: ', network_dist)
print ('Detour_index: ', Detour_index)
print ('#######################')

################################################################################
#load route layer
#count length of links
#count surface of layer


#load route layer
#count length of links
features = route_layer.getFeatures()
links_length = 0
nb_links = 0
for feature in features:
    # fetch geometry
    # show some information about the feature geometry
    geom = feature.geometry()
    geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
    if geom.type() == QgsWkbTypes.LineGeometry:
        if geomSingleType:
            links_length = links_length + geom.length()
            nb_links = nb_links + 1
        else:
            links_length = links_length + geom.length()
            nb_links = nb_links + 1
            #nb_links = nb_links + len (geom.asMultiPolyline()[0])-1
#count surface of layer
path_to_min_boundary_geom = "G:/607/min_boundary_geom.shp"
processing.run("qgis:minimumboundinggeometry", {'INPUT':route_layer, 'TYPE':3, 'OUTPUT': path_to_min_boundary_geom})
min_boundary_geom = layer (path_to_min_boundary_geom,"min_boundary_geom")

surface = 0
features = min_boundary_geom.getFeatures()
for feature in features:
    geom = feature.geometry()
    geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
    if geom.type() == QgsWkbTypes.PolygonGeometry:
        if geomSingleType:
            surface = geom.area()
        else:
            surface = geom.area()
links_length = links_length / 1000
surface = surface / 1000000
print ('links_length: ', links_length  )
print ('surface', surface  )
print ('Network Density', links_length / surface )
