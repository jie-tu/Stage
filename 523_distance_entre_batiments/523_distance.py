from qgis.core import QgsProject
project = QgsProject.instance()
print(project.fileName())

def layer(path_to_layer,name_layer):
    vlayer = QgsVectorLayer(path_to_layer,name_layer,"ogr")
    QgsProject.instance().addMapLayer(vlayer)
    return vlayer

########################### distance ############################################
path_to_distance_route_bati = "G:/523/distance_route_bati.shp"
distance_route_bati = layer (path_to_distance_route_bati, "distance_route_bati")
print ("distance_route_bati")

dict = {}
features = distance_route_bati.getFeatures()
for feature in features:
    geom = feature.geometry()
    geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())

     # fetch attributes
    attrs = feature.attributes()
    # attrs is a list. It contains all the attribute values of this feature
    print(attrs)
    # for this test only print the first feature
    break
