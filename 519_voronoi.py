from qgis.core import QgsProject
from qgis.PyQt.QtCore import QVariant

project = QgsProject.instance()
################################## fonction ####################################
def layer(path_to_layer,name_layer):
    vlayer = QgsVectorLayer(path_to_layer,name_layer,"ogr")
    QgsProject.instance().addMapLayer(vlayer)
    return vlayer

################################## processing ##################################
path_to_batiment_clip = "G:/518/bati_clip.shp"
batiment_clip = layer (path_to_batiment_clip,"batiment_layer")

path_to_batiment_single_polygon = "G:/519/batiment_single_polygon.shp"
processing.run("native:multiparttosingleparts", {'INPUT':batiment_clip, 'OUTPUT': path_to_batiment_single_polygon})
batiment_single_polygon = layer (path_to_batiment_single_polygon,"batiment_single_polygon")
print ("batiment_single_parts")

list=[]
features = batiment_single_polygon.getFeatures()
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

caps = batiment_single_polygon.dataProvider().capabilities()
if caps & QgsVectorDataProvider.DeleteFeatures:
    res = batiment_single_polygon.dataProvider().deleteFeatures(list)

if iface.mapCanvas().isCachingEnabled():
    batiment_single_polygon.triggerRepaint()
else:
    iface.mapCanvas().refresh()
######

path_to_batiment_boundary = "G:/519/batiment_boundary.shp"
processing.run("native:boundary", {'INPUT':batiment_single_polygon , 'OUTPUT': path_to_batiment_boundary})
batiment_boundary = layer (path_to_batiment_boundary, "batiment_boundary")
print("batiment_boundary")

path_to_batiment_densified = "G:/519/batiment_densified.shp"
processing.run("native:densifygeometriesgivenaninterval", {'INPUT':batiment_boundary, 'OUTPUT':path_to_batiment_densified})
batiment_densified = layer (path_to_batiment_densified,"batiment_densified")
print("batiment_densified")

path_to_batiment_converted = "G:/519/batiment_converted.shp"
processing.run("native:extractvertices", {'INPUT': batiment_densified, 'OUTPUT':path_to_batiment_converted})
batiment_converted = layer (path_to_batiment_converted,"batiment_converted")
print("batiment_converted")

path_to_batiment_single_parts = "G:/519/batiment_single_parts.shp"
processing.run("native:multiparttosingleparts", {'INPUT':batiment_converted, 'OUTPUT': path_to_batiment_single_parts})
batiment_single_parts = layer (path_to_batiment_single_parts,"batiment_single_parts")
print ("batiment_single_parts")

path_to_voronoi =  "G:/519/voronoi.shp"
processing.run("qgis:voronoipolygons", {'INPUT':batiment_single_parts, 'BUFFER': 0.0, 'OUTPUT': path_to_voronoi})
voronoi = layer (path_to_voronoi,"voronoi")
print("voronoi")

path_to_voronoi_to_line =  "G:/519/voronoi_to_line.shp"
processing.run("native:polygonstolines", {'INPUT':voronoi,'OUTPUT': path_to_voronoi_to_line})
voronoi_to_line = layer (path_to_voronoi_to_line,"voronoi_to_line")
print("voronoi_to_line")

path_to_line_explode = "G:/519/line_explode.shp"
processing.run("native:explodelines", {'INPUT':voronoi_to_line,'OUTPUT': path_to_line_explode})
line_explode = layer (path_to_line_explode, "line_explode")
print ("line_explode")

path_to_extracted = "G:/519/extracted.shp"
processing.run("qgis:extractbylocation", {'INPUT': line_explode,'PREDICATE': 2,'INTERSECT':batiment_clip, 'OUTPUT': path_to_extracted})
extracted = layer (path_to_extracted, 'extracted')
print("extracted")

path_to_dissolve = "G:/519/dissolve.shp"
processing.run("native:dissolve", {'INPUT':extracted, 'OUTPUT':path_to_dissolve })
dissolve = layer (path_to_dissolve,'dissolve')
print('dissolve')

path_to_dissolve_single = "G:/519/dissolve_single.shp"
processing.run("native:multiparttosingleparts", {'INPUT':dissolve, 'OUTPUT':path_to_dissolve_single })
dissolve_single = layer (path_to_dissolve_single,'dissolve_single')
print('dissolve_single')

path_to_intersection = "G:/519/intersection.shp"
processing.run("qgis:lineintersections", {'INPUT': dissolve_single , 'INTERSECT' :dissolve_single, 'OUTPUT':path_to_intersection })
intersection = layer (path_to_intersection, 'intersection')
print ('intersection')
