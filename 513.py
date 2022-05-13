from qgis.core import QgsProject
from qgis.PyQt.QtCore import QVariant

project = QgsProject.instance()
################################## fonction ####################################
def layer(path_to_layer,name_layer):
    print(path_to_layer,name_layer)
    vlayer = QgsVectorLayer(path_to_layer,name_layer,"ogr")
    QgsProject.instance().addMapLayer(vlayer)

    return vlayer

def new_layer (path_to_new_layer):
    fields = QgsFields()
    fields.append(QgsField("ID", QVariant.String)) #0
    fields.append(QgsField("nature", QVariant.String)) #1
    fields.append(QgsField("importance", QVariant.Int)) #2
    fields.append(QgsField("nb_voies", QVariant.Int)) #3
    fields.append(QgsField("largeur", QVariant.Double)) #4
    fields.append(QgsField("sens", QVariant.String)) #5
    fields.append(QgsField("urban", QVariant.String)) #6
    fields.append(QgsField("vit_moy_vl", QVariant.Int)) #7
    fields.append(QgsField("acces_vl", QVariant.String)) #8
    fields.append(QgsField("acces_pied", QVariant.String)) #9
    fields.append(QgsField("c_postal_g", QVariant.Int)) #10

    fields.append(QgsField("hubDist", QVariant.Double)) #11

    fields.append(QgsField("inter_ID", QVariant.String))
    # if != ID, intersection for different modes #12



    crs = QgsProject.instance().crs()
    transform_context = QgsProject.instance().transformContext()
    save_options = QgsVectorFileWriter.SaveVectorOptions()
    save_options.driverName = "ESRI Shapefile"
    save_options.fileEncoding = "UTF-8"



    writer = QgsVectorFileWriter.create(
      path_to_new_layer,
      fields,
      QgsWkbTypes.LineString,
      crs,
      transform_context,
      save_options
    )

    if writer.hasError() != QgsVectorFileWriter.NoError:
        print("Error when creating shapefile: ",  writer.errorMessage())

    return writer



path_to_new_layer = "G:/513data/new_route.shp"
writer = new_layer (path_to_new_layer)


Dict = {}
# dict from attribute ID to field id, eg {'TRONROUT0000002202568601' : 0 }

################################################################################

print ('###### route features #####')
path_to_route_layer = "E:/DS/up/cs/resume/512/route_clip.shp"
route_layer = layer (path_to_route_layer,"route_layer")
features = route_layer.getFeatures()

#init dict


for feature in features:
     # retrieve every feature with its geometry and attributes
    print("Feature ID: ", feature.id())
    # fetch geometry
    # show some information about the feature geometry
    geom = feature.geometry()
    geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
    if geom.type() == QgsWkbTypes.LineGeometry:
        if geomSingleType:
            x = geom.asPolyline()
            print("Line: ", x, "length: ", geom.length())
        else:
            x = geom.asMultiPolyline()
            print("MultiLine: ", x, "length: ", geom.length())
    else:
        print("Unknown or invalid geometry")
    # fetch attributes
    attrs = feature.attributes()
    # attrs is a list. It contains all the attribute values of this feature
    print(attrs[0])#ID
    print(attrs[1])#nature
    print(attrs[6])#importance
    print(attrs[18])#nb_voies
    print(attrs[19])#largeur
    print(attrs[22])#sens
    print(attrs[25])#urban
    print(attrs[26])#vit_moy_vl
    print(attrs[27])#acces_vl
    print(attrs[28])#acces_pied
    print(attrs[46])#c_postal_g

    #set attribute
    fet = QgsFeature()
    #fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(10,10)))
    fet.setGeometry(geom)
    fet.setAttributes([attrs[0],attrs[1],attrs[6],attrs[18],attrs[19],attrs[22],attrs[25],attrs[26],attrs[27],attrs[28],attrs[46]])
    writer.addFeature(fet)

    #set dict
    Dict[attrs[0]] = feature.id()

    # for this test only print the first feature
    break


new_layer = layer (path_to_new_layer, "new_layer")
del writer

################################################################################
print ('###### distance ######')

path_to_distance_route_bati = "G:/512data/distance_route_bati.shp"
distance_route_bati = layer (path_to_distance_route_bati, "distance_route_bati")

################################################################################
print ('####### intersection features for modes #######')

path_to_intersection = "G:/512data/intersection.shp"
intersection = layer (path_to_intersection, "intersection")
features = intersection.getFeatures()

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
    else:
        print("Unknown or invalid geometry")
    # fetch attributes
    attrs = feature.attributes()
    # attrs is a list. It contains all the attribute values of this feature
    print(attrs[0])#ID
    print(attrs[63])#hubDist
    print(attrs[64])#intersection point, if

    # from id, get field id
    feature_id = Dict[attrs[0]]
    # from field id, set attrs
    caps = new_layer.dataProvider().capabilities()
    if caps & QgsVectorDataProvider.ChangeAttributeValues:
        attrs_change = { 11: attrs[63],12: attrs[64] }
        new_layer.dataProvider().changeAttributeValues({ feature_id : attrs_change })

    if iface.mapCanvas().isCachingEnabled():
        new_layer.triggerRepaint()
    else:
        iface.mapCanvas().refresh()
    # for this test only print the first feature
    break
