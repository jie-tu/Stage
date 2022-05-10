from qgis.core import QgsProject
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


path_to_routes_layer = "E:/DS/up/cs/resume/504/BDTOPO_3-0_TOUSTHEMES_SHP_LAMB93_D075_2022-03-15/BDTOPO_3-0_TOUSTHEMES_SHP_LAMB93_D075_2022-03-15/BDTOPO/1_DONNEES_LIVRAISON_2022-03-00081/BDT_3-0_SHP_LAMB93_D075-ED2022-03-15/TRANSPORT/TRONCON_DE_ROUTE.shp"
layer (path_to_routes_layer,"routes_layer")

path_to_batiment_layer = "E:/DS/up/cs/resume/504/BDTOPO_3-0_TOUSTHEMES_SHP_LAMB93_D075_2022-03-15/BDTOPO_3-0_TOUSTHEMES_SHP_LAMB93_D075_2022-03-15/BDTOPO/1_DONNEES_LIVRAISON_2022-03-00081/BDT_3-0_SHP_LAMB93_D075-ED2022-03-15/BATI/BATIMENT.shp"
layer (path_to_batiment_layer,"batiment_layer")
