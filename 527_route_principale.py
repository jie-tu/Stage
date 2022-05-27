from qgis.core import QgsProject
from qgis.PyQt.QtCore import QVariant

project = QgsProject.instance()
print(project.fileName())

def layer(path_to_layer,name_layer):
    vlayer = QgsVectorLayer(path_to_layer,name_layer,"ogr")
    QgsProject.instance().addMapLayer(vlayer)
    return vlayer

##########################################################
#load route layer
path_to_route_layer = "G:/527/src/route_clip.shp"
route_layer = layer (path_to_route_layer,"route_layer")

#load  layer intersection entre batiment et route
path_to_intersection_routier = "G:/527/src/intersection_routier.shp"
intersection_routier = layer (path_to_intersection_routier,"intersection_routier")

# pour chaque intersection
#   trouver une liste de routes entre les deux batiment
#   retouner la route qui a plus petit de nombre de importance,
dic = {}
features = intersection_routier.getFeatures()
for feature in features:
    attrs = feature.attributes()
    #mettre dic comme { (bati1, bati2): { route1 : importance} }
    if (attrs[0],attrs[2]) not in dic.keys():
        dict_route = {}
        dict_route [attrs[4]] = attrs[6]
        dic [(attrs[0],attrs[2])] = dict_route
    else:
        dic [(attrs[0],attrs[2])] [attrs[4]] = attrs[6]

#print (dic.items())

# garder route importance=4,
# ajouter les informations de route importance=5 à route importance=4
# supprimer route importance=5

for dict_route in dic.items():
    dict_route_sorted  = sorted (dict_route[1].items(), key=lambda x: x[1] ,reverse = False)
    #print (dict_route[0],dict_route_sorted)


dict_route_to_id= {}
features = route_layer.getFeatures()
for feature in features:
    attrs = feature.attributes()
    dict_route_to_id [attrs[0]] = feature.id()


#creer un layer route principale à route secondaire
fields = QgsFields()
fields.append(QgsField("ID_route_principale", QVariant.String))
fields.append(QgsField("nature_principale", QVariant.String))
fields.append(QgsField("ID_nature_secondaire", QVariant.String))
fields.append(QgsField("nature_secondaire", QVariant.String))


crs = QgsProject.instance().crs()
transform_context = QgsProject.instance().transformContext()
save_options = QgsVectorFileWriter.SaveVectorOptions()
save_options.driverName = "ESRI Shapefile"
save_options.fileEncoding = "UTF-8"

writer = QgsVectorFileWriter.create(
  "G:/527/src/route_principale.shp",
  fields,
  QgsWkbTypes.MultiLineStringZ,
  crs,
  transform_context,
  save_options
)

if writer.hasError() != QgsVectorFileWriter.NoError:
    print("Error when creating shapefile: ",  writer.errorMessage())


for dict_route in dic.items():
    id_route_principale = ""
    id_route_secondaire = ""
    c=0
    for k in dict_route[1].keys():
        if c == 0 :
            id_route_principale = k
        else:
            id_route_secondaire = k
        c=c+1

        route_id = dict_route_to_id [id_route_principale]

        fet = QgsFeature()
        fet.setGeometry(route_layer.getGeometry(route_id))
        fet.setAttributes([id_route_principale,"car",id_route_secondaire,"car"])
        writer.addFeature(fet)
del writer
