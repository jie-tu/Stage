from qgis.core import QgsProject
project = QgsProject.instance()
print(project.fileName())

def layer(path_to_layer,name_layer):
    vlayer = QgsVectorLayer(path_to_layer,name_layer,"ogr")
    QgsProject.instance().addMapLayer(vlayer)
    return vlayer

############################ batiment processing ###########################################

path_to_batiment_layer = "G:/523/bati_clip.shp"
batiment_layer = layer (path_to_batiment_layer,"BATIMENT_layer")

list=[]
features = batiment_layer.getFeatures()
for feature in features:
    geom = feature.geometry()
    geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
    if geom.type() == QgsWkbTypes.PolygonGeometry:
        if geomSingleType:
            if geom.area() < 28:
                list.append(feature.id())
        else:
            if geom.area() < 28:
                list.append(feature.id())
    else:
        print("Unknown or invalid geometry")

caps = batiment_layer.dataProvider().capabilities()
if caps & QgsVectorDataProvider.DeleteFeatures:
    res = batiment_layer.dataProvider().deleteFeatures(list)

if iface.mapCanvas().isCachingEnabled():
    batiment_layer.triggerRepaint()
else:
    iface.mapCanvas().refresh()


path_to_batiment_boundary = "G:/523/batiment_boundary.shp"
processing.run("native:boundary", {'INPUT':batiment_layer , 'OUTPUT': path_to_batiment_boundary})
batiment_boundary = layer (path_to_batiment_boundary, "batiment_boundary")
print("batiment_boundary")

path_to_batiment_densified = "G:/523/batiment_densified.shp"
processing.run("native:densifygeometriesgivenaninterval", {'INPUT':batiment_boundary, 'OUTPUT':path_to_batiment_densified})
batiment_densified = layer (path_to_batiment_densified,"batiment_densified")
print("batiment_densified")

path_to_batiment_converted = "G:/523/batiment_converted.shp"
processing.run("native:extractvertices", {'INPUT': batiment_densified, 'OUTPUT':path_to_batiment_converted})
batiment_converted = layer (path_to_batiment_converted,"batiment_converted")
print("batiment_converted")

path_to_batiment_single_parts = "G:/523/batiment_single_parts.shp"
processing.run("native:multiparttosingleparts", {'INPUT':batiment_converted, 'OUTPUT': path_to_batiment_single_parts})
batiment_single_parts = layer (path_to_batiment_single_parts,"batiment_single_parts")
print ("batiment_single_parts")



############################# route processing ##########################################

path_to_ligne_mediane = "G:/523/extracted.shp"
ligne_mediane = layer (path_to_ligne_mediane,"ligne_mediane")
print ('ligne_mediane')

path_to_ligne_mediane_vertices = "G:/523/ligne_mediane_vertices.shp"
processing.run("native:extractvertices", {'INPUT':ligne_mediane, 'OUTPUT': path_to_ligne_mediane_vertices })
ligne_mediane_vertices = layer (path_to_ligne_mediane_vertices,'ligne_mediane_vertices')
print ('ligne_mediane_vertices')


########################### distance ############################################
path_to_distance_route_bati = "G:/523/distance_route_bati.shp"
processing.run("qgis:distancematrix", {'INPUT' : path_to_ligne_mediane_vertices,'INPUT_FIELD': 'ID', 'TARGET' : batiment_single_parts, 'TARGET_FIELD' : "ID", 'MATRIX_TYPE': 0 ,'NEAREST_POINTS': 2, 'OUTPUT' : path_to_distance_route_bati})
distance_route_bati = layer (path_to_distance_route_bati, "distance_route_bati")
print ("distance_route_bati")
