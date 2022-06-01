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
#load layer intersection route
#get dict { (bati1 , bati 2 ) : {route : id} }
#load layer intersecion bus
#get dict { (bati1 , bati 2 ) : {bus : id } }
#retouner { route : [bus] }

#load  layer intersection entre batiment et route
path_to_intersection_route = "G:/530/src/intersection_route.shp"
intersection_route = layer (path_to_intersection_route,"intersection_route")

dict_bati_route ={}
features = intersection_route.getFeatures()
for feature in features:
    attrs = feature.attributes()

    if (attrs[0],attrs[2]) not in dict_bati_route.keys():
        dict_route = {}
        dict_route [attrs[4]] = feature.id()
        dict_bati_route [(attrs[0],attrs[2])] = dict_route
    else:
        dict_bati_route [(attrs[0],attrs[2])] [attrs[4]] = feature.id()

#load  layer intersection entre batiment et bus
path_to_intersection_bus = "G:/530/src/intersection_bus.shp"
intersection_bus = layer (path_to_intersection_bus,"intersection_bus")

dict_bati_bus ={}
features = intersection_bus.getFeatures()
for feature in features:
    attrs = feature.attributes()

    if (attrs[0],attrs[2]) not in dict_bati_bus.keys():
        dict_bus = {}
        dict_bus [attrs[4]] = feature.id()
        dict_bati_bus [(attrs[0],attrs[2])] = dict_bus
    else:
        dict_bati_bus [(attrs[0],attrs[2])] [attrs[4]] = feature.id()

#retouner { route : [bus] }
dict_route_bus = {}
for dict_bus in dict_bati_bus.items():
    batis = dict_bus[0]
    list_bus = [*dict_bus[1]]
    if batis in dict_bati_route.keys():
        list_route = dict_bati_route [batis].keys()
        for route in list_route :
            if route in dict_route_bus.keys():
                dict_route_bus[route].extend(list_bus)
            else:
                dict_route_bus[route]= list_bus
    elif (batis[1],batis[0]) in dict_bati_route.keys():
        list_route = [ * dict_bati_route [(batis[1],batis[0])] ]
        for route in list_route :
            if route in dict_route_bus.keys():
                dict_route_bus[route].extend(list_bus)
            else:
                dict_route_bus[route]= list_bus
for key, value in dict_route_bus.items():
    dict_route_bus[key] = [ * set(value)]
#print(dict_route_bus)



##########################################################
print ("##########################################################")
#load layer intersecion velo
#get dict { (bati1 , bati 2 ) : {velo : id } }
#retouner { route : [velo] }


#load  layer intersection entre batiment et velo
path_to_intersection_velo = "G:/530/src/intersection_velo.shp"
intersection_velo = layer (path_to_intersection_velo,"intersection_velo")

dict_bati_velo ={}
features = intersection_velo.getFeatures()
for feature in features:
    attrs = feature.attributes()

    if (attrs[0],attrs[2]) not in dict_bati_velo.keys():
        dict_velo = {}
        dict_velo [attrs[4]] = feature.id()
        dict_bati_velo [(attrs[0],attrs[2])] = dict_velo
    else:
        dict_bati_velo [(attrs[0],attrs[2])] [attrs[4]] = feature.id()

#retouner { route : [velo] }
dict_route_velo = {}
for dict_velo in dict_bati_velo.items():
    batis = dict_velo[0]
    list_velo = [*dict_velo[1].keys()]
    #print (dict_bati_route [batis])
    if batis in dict_bati_route.keys():
        list_route = [*dict_bati_route [batis].keys()]
        for route in list_route :
            if route in dict_route_velo.keys():
                dict_route_velo[route].extend(list_velo)
            else:
                dict_route_velo[route]= list_velo
    elif (batis[1],batis[0]) in dict_bati_route.keys():
        list_route = [*dict_bati_route [(batis[1],batis[0])].keys()]
        for route in list_route :
            if route in dict_route_velo.keys():
                dict_route_velo[route].extend(list_velo)
            else:
                dict_route_velo[route]= list_velo

for key, value in dict_route_velo.items():
    dict_route_velo[key] = [*set(value)]
#print(dict_route_velo)


################################################################################
#load layer distance_metro_bati
#get gares_id, bati id
#get route from bati id

#load layer distance_metro_bati
path_to_distance_metro_bati = "G:/530/src/distance_metro_bati.shp"
distance_metro_bati = layer (path_to_distance_metro_bati,"distance_metro_bati")

#get route from bati id
#return {route : [gares_id]}
dict_route_metro= {}
features = distance_metro_bati.getFeatures()
for feature in features:
    attrs = feature.attributes()
    gares_id = attrs [0]
    bati_id = attrs [38]

    for key, value in dict_bati_route.items():
        if (bati_id in key[0]) or  (bati_id in key[1]):
            for val in value.keys():
                if val in dict_route_metro.keys():
                    dict_route_metro[val].append(gares_id)
                else:
                    dict_route_metro[val] = [gares_id]

for key, value in dict_route_metro.items():
    dict_route_metro[key] = [*set(value)]
#print(dict_route_metro)

################################################################################
#load route layer
#get geom from route layer by route feature id
#create layer {route : bus/velo/metro}


#load route layer
path_to_route_layer = "G:/530/src/route_clip.shp"
route_layer = layer (path_to_route_layer,"route_layer")

dict_route = {}
features = route_layer.getFeatures()
for feature in features:
    attrs = feature.attributes()
    dict_route [attrs[0]] = feature.geometry()

#print (dict_route)
#create layer {route : bus/velo}
# define fields for feature attributes. A QgsFields object is needed
fields = QgsFields()
fields.append(QgsField("route1", QVariant.String))
fields.append(QgsField("route1_type", QVariant.String))
fields.append(QgsField("route2", QVariant.String))
fields.append(QgsField("route2_type", QVariant.String))

crs = QgsProject.instance().crs()
transform_context = QgsProject.instance().transformContext()
save_options = QgsVectorFileWriter.SaveVectorOptions()
save_options.driverName = "ESRI Shapefile"
save_options.fileEncoding = "UTF-8"

writer = QgsVectorFileWriter.create(
  "G:/530/src/modes.shp",
  fields,
  QgsWkbTypes.MultiLineStringZ,
  crs,
  transform_context,
  save_options
)

if writer.hasError() != QgsVectorFileWriter.NoError:
    print("Error when creating shapefile: ",  writer.errorMessage())


#add feature from dict_route_bus
for key, value in dict_route_bus.items():
    for val in value :
        # add a feature
        fet = QgsFeature()
        fet.setGeometry(dict_route[key])
        fet.setAttributes([key,"vehicule", val,"bus"])
        writer.addFeature(fet)

for key, value in dict_route_velo.items():
    for val in value :
        # add a feature
        fet = QgsFeature()
        fet.setGeometry(dict_route[key])
        fet.setAttributes([key,"vehicule", val,"velo"])
        writer.addFeature(fet)

for key, value in dict_route_metro.items():
    for val in value :
        # add a feature
        fet = QgsFeature()
        fet.setGeometry(dict_route[key])
        fet.setAttributes([key,"vehicule", str(val),"metro"])
        writer.addFeature(fet)
# delete the writer to flush features to disk
del writer

#load modes
path_to_modes = "G:/530/src/modes.shp"
modes = layer (path_to_modes,"modes")

features = route_layer.getFeatures()
for feature in features:
    print (feature.attributes()[0],feature.geometry())
    break

print ("#################################################")
features = modes.getFeatures()
for feature in features:
    if "TRONROUT0000002202568601" in feature.attributes()[0]:
        print (feature.attributes()[0],feature.geometry())
