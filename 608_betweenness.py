from qgis.core import QgsProject
from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsTracer
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
#caculate shortest path
#caaculate betweenness


#load road network
path_to_route_layer  = "G:/607/route_clip.shp"
route_layer = layer (path_to_route_layer,"route_layer")


nb_points = 1000
#random points
path_to_points_layer  = "G:/608/points_layer.shp"
processing.run("qgis:randompointsalongline", {'INPUT': route_layer,'POINTS_NUMBER':nb_points,'OUTPUT':path_to_points_layer })
points_layer = layer (path_to_points_layer,"points_layer")

features = points_layer.getFeatures()
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

# create layer
vl = QgsVectorLayer("MultiLineString", "temporary_points", "memory")
pr = vl.dataProvider()

# add fields
pr.addAttributes([QgsField("name", QVariant.Int)])
vl.updateFields() # tell the vector layer to fetch changes from the provider

def pluscourtchemin(point_a, point_b):
    tr = QgsTracer()
    tr.setLayers([route_layer])
    geo,err = tr.findShortestPath(point_a,point_b)
    #print (geo)

    # add a feature
    fet = QgsFeature()
    fet.setGeometry(QgsGeometry.fromPolylineXY(geo))
    fet.setAttributes([i])
    pr.addFeatures([fet])

    # update layer's extent when new features have been added
    # because change of extent in provider is not propagated to the layer
    vl.updateExtents()

for i in range (nb_points-1):
    pluscourtchemin(points[i], points[i+1])

QgsProject.instance().addMapLayer(vl)
