from qgis.core import QgsProject
project = QgsProject.instance()
print(project.fileName())

def layer(path_to_layer,name_layer):
    vlayer = QgsVectorLayer(path_to_layer,name_layer,"ogr")
    QgsProject.instance().addMapLayer(vlayer)
    return vlayer


path_to_route_layer = "G:/525/clip/route_clip.shp"
route_layer = layer (path_to_route_layer,"route_layer")


list=[]
features = route_layer.getFeatures()
for feature in features:
    attrs = feature.attributes()
    if 'Libre' not in attrs[27] :
        list.append(feature.id())

caps = route_layer.dataProvider().capabilities()
if caps & QgsVectorDataProvider.DeleteFeatures:
    res = route_layer.dataProvider().deleteFeatures(list)

if iface.mapCanvas().isCachingEnabled():
    route_layer.triggerRepaint()
else:
    iface.mapCanvas().refresh()

path_to_Hub_distance = "G:/525/clip/Hub_distance.shp"
Hub_distance = layer (path_to_Hub_distance,'Hub_distance')
print('Hub_distance')

path_to_intersection_routier = "G:/525/intersection/intersection_routier.shp"
processing.run("qgis:lineintersections", {'INPUT':Hub_distance, 'INTERSECT':route_layer, 'INPUT_FIELDS': ['ID','angle', 'HubName','HubDist'],'INTERSECT_FIELDS' : ['ID','NATURE','IMPORTANCE','NB_VOIES','LARGEUR','SENS','CYCLABLE','BUS','URBAIN','VIT_MOY_VL','ACCES_VL','ACCES_PED','C_POSTAL_G'], 'OUTPUT': path_to_intersection_routier})
intersection_routier = layer (path_to_intersection_routier,'intersection_routier')
print('intersection_routier')


path_to_bus_clip = "G:/525/clip/bus_clip.shp"
bus_clip = layer (path_to_bus_clip,'bus_clip')
print('bus_clip')

path_to_intersection_bus = "G:/525/intersection/intersection_bus.shp"
processing.run("qgis:lineintersections", {'INPUT':Hub_distance, 'INTERSECT':bus_clip, 'INPUT_FIELDS': ['ID','angle', 'HubName','HubDist'],'INTERSECT_FIELDS' : None, 'OUTPUT': path_to_intersection_bus})
intersection_bus = layer (path_to_intersection_bus,'intersection_bus')
print('intersection_bus')

path_to_velo_clip = "G:/525/clip/velo_clip.shp"
velo_clip = layer (path_to_velo_clip,'velo_clip')
print('velo_clip')

path_to_intersection_velo = "G:/525/intersection/intersection_velo.shp"
processing.run("qgis:lineintersections", {'INPUT':Hub_distance, 'INTERSECT':velo_clip, 'INPUT_FIELDS': ['ID','angle', 'HubName','HubDist'],'INTERSECT_FIELDS' : None, 'OUTPUT': path_to_intersection_velo})
intersection_velo = layer (path_to_intersection_velo,'intersection_velo')
print('intersection_velo')
