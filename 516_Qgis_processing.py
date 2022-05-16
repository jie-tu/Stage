from qgis.core import QgsProject
project = QgsProject.instance()
print(project.fileName())



def layer(path_to_layer,name_layer):
    #print(path_to_layer,name_layer)
    vlayer = QgsVectorLayer(path_to_layer,name_layer,"ogr")
    QgsProject.instance().addMapLayer(vlayer)
    #if not vlayer.isValid():
    #    print("Layer failed to load!")
    #else:
    #    QgsProject.instance().addMapLayer(vlayer)

    if (False):
        print("#########################")
        print(vlayer.displayField())
        print("#########################")
        for field in vlayer.fields():
            print(field.name(), field.typeName())

        print("#########################")
        # "layer" is a QgsVectorLayer instance
        #layer = iface.activeLayer()
        layer = vlayer
        features = layer.getFeatures()
        for feature in features:
            # retrieve every feature with its geometry and attributes
            print("Feature ID: ", feature.id())
            # fetch geometry
            # show some information about the feature geometry
            geom = feature.geometry()
            geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
            if geom.type() == QgsWkbTypes.PointGeometry:
                # the geometry type can be of single or multi type
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
            # fetch attributes
            attrs = feature.attributes()
            # attrs is a list. It contains all the attribute values of this feature
            print(attrs)
            # for this test only print the first feature
            print("#########################")
            break
    return vlayer


############################ batiment processing ###########################################

path_to_batiment_layer = "G:/515/batiment_clip.shp"
batiment_layer = layer (path_to_batiment_layer,"BATIMENT_layer")

path_to_batiment_single = "G:/515/path_to_batiment_single.shp"
processing.run("native:multiparttosingleparts", {'INPUT':batiment_layer , 'OUTPUT': path_to_batiment_single})
batiment_single =layer (path_to_batiment_single,"batiment_single")


path_to_batiment_dissolve  = "G:/515/batiment_dissolve.shp"
processing.run("native:dissolve", {'INPUT': batiment_single ,'FIELD': [], 'OUTPUT': path_to_batiment_dissolve})
batiment_dissolve = layer (path_to_batiment_dissolve, "batiment_dissolve")



path_to_batiment_single2 =  "G:/515/batiment_fix2.shp"
processing.run("native:multiparttosingleparts", {'INPUT':batiment_dissolve , 'OUTPUT' : path_to_batiment_single2 })
batiment_single2 = layer (path_to_batiment_single2, "batiment_single2")



path_to_batiment_dissolve2 = "G:/515/batiment_dissolve2.shp"
processing.run("native:dissolve", {'INPUT': batiment_single2 , 'FIELD': [], 'OUTPUT' : path_to_batiment_dissolve2})
batiment_dissolve2 = layer (path_to_batiment_dissolve2, "batiment_dissolve2")



path_to_batiment_cleaned = "G:/515/batiment_cleaned.shp"
processing.run("native:deleteholes", {'INPUT': batiment_dissolve2 , 'MIN_AREA' : 10000, 'OUTPUT' : path_to_batiment_cleaned})
batiment_cleaned = layer (path_to_batiment_cleaned, "batiment_cleaned")

###################################################################################

path_to_batiment_boundary = "G:/515/batiment_boundary.shp"
processing.run("native:boundary", {'INPUT':batiment_cleaned , 'OUTPUT': path_to_batiment_boundary})
batiment_boundary = layer (path_to_batiment_boundary, "batiment_boundary")
print("batiment_boundary")

path_to_batiment_densified = "G:/515/batiment_densified.shp"
processing.run("native:densifygeometriesgivenaninterval", {'INPUT':batiment_boundary, 'OUTPUT':path_to_batiment_densified})
batiment_densified = layer (path_to_batiment_densified,"batiment_densified")
print("batiment_densified")

path_to_batiment_converted = "G:/515/batiment_converted.shp"
processing.run("native:extractvertices", {'INPUT': batiment_densified, 'OUTPUT':path_to_batiment_converted})
batiment_converted = layer (path_to_batiment_converted,"batiment_converted")
print("batiment_converted")

path_to_batiment_single_parts = "G:/515/batiment_single_parts.shp"
processing.run("native:multiparttosingleparts", {'INPUT':batiment_converted, 'OUTPUT': path_to_batiment_single_parts})
batiment_single_parts = layer (path_to_batiment_single_parts,"batiment_single_parts")
print ("batiment_single_parts")


############################# route processing ##########################################

path_to_route_layer = "G:/515/route_clip.shp"
route_layer = layer (path_to_route_layer,"ROUTE_layer")

path_to_route_explode = "G:/515/route_explode.shp"
processing.run("native:explodelines", {'INPUT' : route_layer, 'OUTPUT': path_to_route_explode})
route_explode =  layer (path_to_route_explode, "route_explode")

path_to_route_centroid = "G:/515/route_centroid.shp"
processing.run("native:centroids", {'INPUT' : route_explode, 'ALL_PARTS': False , 'OUTPUT': path_to_route_centroid })
route_centroid =  layer (path_to_route_centroid, "route_centroid")
print ("route_centroid")



########################### distance ############################################
path_to_distance_route_bati = "G:/515/distance_route_bati.shp"
processing.run("qgis:distancetonearesthublinetohub", {'INPUT' : route_centroid,'HUBS' : batiment_single_parts, 'FIELD' : "ID", 'UNIT': 0 , 'OUTPUT' : path_to_distance_route_bati})
distance_route_bati = layer (path_to_distance_route_bati, "distance_route_bati")
print ("distance_route_bati")


########################### intersection for transportation modes ############################################
path_to_intersection = "G:/515/intersection.shp"
processing.run("qgis:lineintersections", {'INPUT':distance_route_bati , 'INTERSECT': route_layer, 'INPUT_FIELDS' : None, 'INTERSECT_FIELDS': None, 'OUTPUT': path_to_intersection  })
intersection = layer (path_to_intersection, "intersection")
print ("intersection ")
