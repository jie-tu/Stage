from qgis.core import QgsProject
import processing

project = QgsProject.instance()
print(project.fileName())


def layer(path_to_layer,name_layer):
    print(path_to_layer,name_layer)
    vlayer = QgsVectorLayer(path_to_layer,name_layer,"ogr")
    QgsProject.instance().addMapLayer(vlayer)
    if not vlayer.isValid():
        print("Layer failed to load!")
    else:
        QgsProject.instance().addMapLayer(vlayer)

    if (False) :
        print("#########################")
        print(vlayer.displayField())
        print("#########################")
        for field in vlayer.fields():
            print(field.name(), field.typeName())

        print("#########################")

        layer = vlayer
        features = layer.getFeatures()
        for feature in features:
            print("Feature ID: ", feature.id())
            geom = feature.geometry()
            geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
            if geom.type() == QgsWkbTypes.PointGeometry:
                if geomSingleType:
                    x = geom.asPoint()
                    print("Point: ", x)
                else:
                    x = geom.asMultiPoint()
                    print("MultiPoint: ", x)
            elif geom.type() == QgsWkbTypes.LineGeometry:
                if geomSingleType:
                    x = geom.asPolyline()
                    print("Line: ", x, "length: ", geom.length())
                else:
                    x = geom.asMultiPolyline()
                    print("MultiLine: ", x, "length: ", geom.length())
            elif geom.type() == QgsWkbTypes.PolygonGeometry:
                if geomSingleType:
                    x = geom.asPolygon()
                    print("Polygon: ", x, "Area: ", geom.area())
                else:
                    x = geom.asMultiPolygon()
                    print("MultiPolygon: ", x, "Area: ", geom.area())
            else:
                print("Unknown or invalid geometry")

            attrs = feature.attributes()
            print(attrs)

            print("#########################")
            break


    return vlayer

############################# route processing ##########################################
path_to_route_layer = "E:/DS/up/cs/resume/504/BDTOPO_3-0_TOUSTHEMES_SHP_LAMB93_D075_2022-03-15/BDTOPO_3-0_TOUSTHEMES_SHP_LAMB93_D075_2022-03-15/BDTOPO/1_DONNEES_LIVRAISON_2022-03-00081/BDT_3-0_SHP_LAMB93_D075-ED2022-03-15/TRANSPORT/TRONCON_DE_ROUTE.shp"
route_layer = layer (path_to_route_layer,"route_layer")

path_to_route_centroid = "E:/DS/up/cs/resume/511/route_centroid.shp"
processing.run("native:centroids", {'INPUT' : route_layer, 'ALL_PARTS': False , 'OUTPUT': path_to_route_centroid })
route_centroid =  layer (path_to_route_centroid, "route_centroid")
print ("route_centroid")
############################ batiment processing ###########################################
path_to_batiment_layer = "E:/DS/up/cs/resume/504/BDTOPO_3-0_TOUSTHEMES_SHP_LAMB93_D075_2022-03-15/BDTOPO_3-0_TOUSTHEMES_SHP_LAMB93_D075_2022-03-15/BDTOPO/1_DONNEES_LIVRAISON_2022-03-00081/BDT_3-0_SHP_LAMB93_D075-ED2022-03-15/BATI/BATIMENT.shp"
batiment_layer = layer (path_to_batiment_layer,"batiment_layer")


path_to_batiment_boundary = "E:/DS/up/cs/resume/511/path_to_batiment_boundary.shp"
processing.run("native:boundary", {'INPUT': path_to_batiment_layer , 'OUTPUT': path_to_batiment_boundary})
batiment_boundary = layer (path_to_batiment_boundary, "batiment_boundary")
print("batiment_boundary")


path_to_batiment_densified = "E:/DS/up/cs/resume/511/batiment_densified.shp"
processing.run("native:densifygeometriesgivenaninterval", {'INPUT':batiment_boundary, 'OUTPUT':path_to_batiment_densified})
batiment_densified = layer (path_to_batiment_densified,"batiment_densified")
print("batiment_densified")


path_to_batiment_converted = "E:/DS/up/cs/resume/511/batiment_converted.shp"
processing.run("qgis:convertgeometrytype", {'INPUT': batiment_densified, 'TYPE': 1, 'OUTPUT':path_to_batiment_converted})
batiment_converted = layer (path_to_batiment_converted,"batiment_converted")
print("batiment_converted")


path_to_batiment_single_parts = "E:/DS/up/cs/resume/511/batiment_single_parts.shp"
processing.run("native:multiparttosingleparts", {'INPUT':batiment_converted, 'OUTPUT': path_to_batiment_single_parts})
batiment_single_parts = layer (path_to_batiment_single_parts,"batiment_single_parts")
print ("batiment_single_parts")
########################### diatance ############################################
path_to_distance_route_bati = "E:/DS/up/cs/resume/511/distance_route_bati.shp"
processing.run("qgis:distancetonearesthublinetohub", {'INPUT' : route_centroid,'HUBS' : batiment_single_parts, 'FIELD' : "ID", 'UNIT': 0 , 'OUTPUT' : path_to_distance_route_bati})
distance_route_bati = layer (path_to_distance_route_bati, "distance_route_bati")
print ("distance_route_bati")
