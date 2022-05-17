from qgis.core import QgsProject
from qgis.PyQt.QtCore import QVariant

project = QgsProject.instance()
################################## fonction ####################################
def layer(path_to_layer,name_layer):
    #print(path_to_layer,name_layer)
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

    #fields.append(QgsField("inter_ID", QVariant.String))
    # if != ID, intersection for different modes #12
    fields.append(QgsField("modes", QVariant.Int))



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

def get_mode (attrs):
    a = 1
    b = 1
    c = 1
    if (attrs[3] == 0 ) or (attrs[4] == 0 ) or ("0" in attrs[5]  ) or (attrs[7] == 0 ) or ("0" in attrs[8]) :
        a = 0 # vehicule
    if "4" not in attrs[1] :
        b = 0 # velo
    if ( "0" in attrs[9]  ) or (( (2 * attrs[11] )- attrs[4]) <4.0 ) :
        c = 0

    return a * 100 + b * 10 + c


path_to_new_layer = "G:/515/new_route.shp"
writer = new_layer (path_to_new_layer)


Dict = {}
# dict from attribute ID to field id, eg {'TRONROUT0000002202568601' : 0 }

################################################################################

print ('###### route features #####')
path_to_route_layer = "G:/515/route_clip.shp"
route_layer = layer (path_to_route_layer,"route_layer")
features = route_layer.getFeatures()

#init dict


for feature in features:
     # retrieve every feature with its geometry and attributes
    #print("Feature ID: ", feature.id())
    # fetch geometry
    # show some information about the feature geometry
    geom = feature.geometry()
    geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
    if geom.type() == QgsWkbTypes.LineGeometry:
        if geomSingleType:
            x = geom.asPolyline()
            #print("Line: ", x, "length: ", geom.length())
        else:
            x = geom.asMultiPolyline()
            #print("MultiLine: ", x, "length: ", geom.length())
    else:
        print("Unknown or invalid geometry")
    # fetch attributes
    attrs = feature.attributes()
    # attrs is a list. It contains all the attribute values of this feature
    #print(attrs[0])#ID
    #print(attrs[1])#nature
    #print(attrs[6])#importance
    #print(attrs[18])#nb_voies
    #print(attrs[19])#largeur
    #print(attrs[22])#sens
    #print(attrs[25])#urban
    #print(attrs[26])#vit_moy_vl
    #print(attrs[27])#acces_vl
    #print(attrs[28])#acces_pied
    #print(attrs[46])#c_postal_g
    #1
    #2
    nature = attrs[1]
    if "Bretelle"    in nature : nature = "1"
    elif "Chemin"      in nature : nature = "2"
    elif "Escalier"    in nature : nature = "3"
    elif "cyclable"    in nature : nature = "4"
    elif "Rond"        in nature : nature = "5"
    elif "chaussée"    in nature : nature = "6"
    elif "empierrée"   in nature : nature = "7"
    elif "Sentier"     in nature : nature = "8"
    elif "autoroutier" in nature : nature = "9"
    else: nature = "0"
    #3
    nb_voies = attrs[18]
    if nb_voies == None:
        nb_voies =0
    #4
    largeur = attrs[19]
    if largeur == None:
        largeur =0
    #5
    sens = attrs[22]
    if "Double"  in sens : sens = "3"
    elif "inverse" in sens : sens = "2"
    elif "direct"  in sens : sens = "1"
    else: sens = "0"
    #6
    urban = attrs[25]
    if "Oui" in urban : urban = "1"
    else : urban = "0"
    #7
    #8
    acces_vl = attrs[27]
    if "Libre" in acces_vl: acces_vl = "1"
    else : acces_vl = "0"
    #9
    acces_pied = attrs[28]
    if acces_pied ==None:
        if "9" in attrs[1] : #autoroutier
            acces_pied = "0" #
        elif "1" in attrs[1]:#Bretelle
            acces_pied = "0"
        else : # on verifie pas ici , mais verifie apres dans get_mode
            acces_pied = "1" # libre
    elif "Libre" in acces_pied : acces_pied = "1"
    else: acces_pied = "0"
    #10
    #11
    #set attribute
    fet = QgsFeature()
    #fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(10,10)))
    fet.setGeometry(geom)
    fet.setAttributes([attrs[0],nature,attrs[6],nb_voies,largeur,sens,urban,attrs[26],acces_vl,acces_pied,attrs[46]])
    writer.addFeature(fet)

    #set dict
    Dict[attrs[0]] = feature.id()

    # for this test only #print the first feature
    #break


new_layer = layer (path_to_new_layer, "new_layer")
del writer

################################################################################
#print ('###### distance ######')

path_to_distance_route_bati = "G:/515/distance_route_bati.shp"
distance_route_bati = layer (path_to_distance_route_bati, "distance_route_bati")
features = distance_route_bati.getFeatures()

for feature in features:
    attrs = feature.attributes()

    feature_id = Dict[attrs[0]]





    # from field id, set attrs
    caps = new_layer.dataProvider().capabilities()
    if caps & QgsVectorDataProvider.ChangeAttributeValues:
        attrs_change = { 11: attrs[63]}
        new_layer.dataProvider().changeAttributeValues({ feature_id : attrs_change })

        mon_feature = new_layer.getFeature(feature_id)
        mode = get_mode (mon_feature.attributes())

        attrs_change = { 12: mode }
        new_layer.dataProvider().changeAttributeValues({ feature_id : attrs_change })


    if iface.mapCanvas().isCachingEnabled():
        new_layer.triggerRepaint()
    else:
        iface.mapCanvas().refresh()

################################################################################
print ('####### intersection features for modes #######')

path_to_intersection = "G:/515/intersection.shp"
intersection = layer (path_to_intersection, "intersection")
features = intersection.getFeatures()

for feature in features:
     # retrieve every feature with its geometry and attributes
    #print("Feature ID: ", feature.id())
    # fetch geometry
    # show some information about the feature geometry
    geom = feature.geometry()
    geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
    if geom.type() == QgsWkbTypes.PointGeometry:
        # the geometry type can be of single or multi type
        if geomSingleType:
            x = geom.asPoint()
            #print("Point: ", x)
        else:
            x = geom.asMultiPoint()
            #print("MultiPoint: ", x)
    else:
        print("Unknown or invalid geometry")
    # fetch attributes
    attrs = feature.attributes()
    # attrs is a list. It contains all the attribute values of this feature
    #print(attrs[0])#ID
    #print(attrs[63])#hubDist
    #print(attrs[64])#intersection point, if

    inter_ID = attrs[64]
    if (inter_ID != None) and (inter_ID not in attrs[0]) :
        mon_id = Dict[attrs[0]]
        mon_feature = new_layer.getFeature(mon_id)
        mode1 = get_mode(mon_feature.attributes())

        voisin_id = Dict[inter_ID]
        voisin_feature = new_layer.getFeature(voisin_id)
        mode2 = get_mode(voisin_feature.attributes())

        #mode = mode1 + mode2

        a1 = mode1 % 10
        a2 = (mode1 // 10) % 10
        a3 = (mode1 // 100)

        b1 = mode2 % 10
        b2 = (mode2 // 10) % 10
        b3 = (mode2 // 100)

        mode = (max (a3,b3) ) * 100 + (max (a2,b2) ) * 10 + (max (a1,b1) )

        # from id, get field id
        feature_id = Dict[attrs[0]]
        # from field id, set attrs
        caps = new_layer.dataProvider().capabilities()
        if caps & QgsVectorDataProvider.ChangeAttributeValues:
            attrs_change = {12:mode }
            new_layer.dataProvider().changeAttributeValues({ feature_id : attrs_change })

        if iface.mapCanvas().isCachingEnabled():
            new_layer.triggerRepaint()
        else:
            iface.mapCanvas().refresh()


    # for this test only #print the first feature
    #break
