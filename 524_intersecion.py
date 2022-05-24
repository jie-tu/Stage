from qgis.core import QgsProject
project = QgsProject.instance()
print(project.fileName())

def layer(path_to_layer,name_layer):
    vlayer = QgsVectorLayer(path_to_layer,name_layer,"ogr")
    QgsProject.instance().addMapLayer(vlayer)
    return vlayer

path_to_batiment_single_parts = "G:/523/batiment_single_parts.shp"
batiment_single_parts = layer (path_to_batiment_single_parts,"batiment_single_parts")
print ("batiment_single_parts")

path_to_ligne_mediane_vertices = "G:/523/ligne_mediane_vertices.shp"
ligne_mediane_vertices = layer (path_to_ligne_mediane_vertices,'ligne_mediane_vertices')
print ('ligne_mediane_vertices')

path_to_Hub_distance = "G:/524/Hub_distance.shp"
processing.run("qgis:distancetonearesthublinetohub", {'INPUT':ligne_mediane_vertices , 'HUBS': batiment_single_parts,'FIELD':'ID','UNIT':0,'OUTPUT': path_to_Hub_distance})
Hub_distance = layer (path_to_Hub_distance,'Hub_distance')
print('Hub_distance')


path_to_route_layer = "G:/523/route_clip.shp"
route_layer = layer (path_to_route_layer,"route_layer")

path_to_intersection = "G:/524/intersection.shp"
processing.run("qgis:lineintersections", {'INPUT':Hub_distance, 'INTERSECT':route_layer, 'INPUT_FIELDS': ['ID','angle', 'HubName','HubDist'],'INTERSECT_FIELDS' : ['ID','NATURE','IMPORTANCE','NB_VOIES','LARGEUR','SENS','CYCLABLE','BUS','URBAIN','VIT_MOY_VL','ACCES_VL','ACCES_PED','C_POSTAL_G'], 'OUTPUT': path_to_intersection})
intersection = layer (path_to_intersection,'intersection')
print('intersection')
