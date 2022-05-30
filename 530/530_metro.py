from qgis.core import QgsProject
from qgis.PyQt.QtCore import QVariant
#load projet
project = QgsProject.instance()
print(project.fileName())

def layer(path_to_layer,name_layer):
    vlayer = QgsVectorLayer(path_to_layer,name_layer,"ogr")
    QgsProject.instance().addMapLayer(vlayer)
    return vlayer

##########################################################
#load layer bati vertices(point with bati id)
#load layer station metro
#get le bati plus proche que station metro
#get route from bati
#add metro to route

#load layer bati vertices(point with bati id)
path_to_batiment_single_parts = "G:/530/src/batiment_single_parts.shp"
batiment_single_parts = layer (path_to_batiment_single_parts,"batiment_single_parts")

#load layer station metro
path_to_station_clip = "G:/530/src/station_clip.shp"
station_clip = layer (path_to_station_clip,"station_clip")

#get le bati plus proche que station metro
path_to_distance_metro_bati = "G:/530/src/distance_metro_bati.shp"
processing.run("qgis:distancetonearesthublinetohub", {'INPUT': station_clip, 'HUBS':batiment_single_parts, 'FIELD': 'ID','UNIT':0, 'OUTPUT': path_to_distance_metro_bati})
distance_metro_bati = layer (path_to_distance_metro_bati,"distance_metro_bati")
