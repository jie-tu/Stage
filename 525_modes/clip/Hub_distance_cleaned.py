from qgis.core import QgsProject
project = QgsProject.instance()
print(project.fileName())

def layer(path_to_layer,name_layer):
    vlayer = QgsVectorLayer(path_to_layer,name_layer,"ogr")
    QgsProject.instance().addMapLayer(vlayer)
    return vlayer

#load distance layer
path_to_Hub_distance = "G:/525/clip/Hub_distance.shp"
Hub_distance = layer (path_to_Hub_distance,'Hub_distance')
print('Hub_distance')

# delete some features
list=[]
dic={}
features = Hub_distance.getFeatures()
for feature in features:
    attrs = feature.attributes()
    if attrs[0] in attrs[6] :
        list.append(feature.id())
    else:
        if (attrs[0],attrs[6]) not in dic.keys():
            dic [(attrs[0],attrs[6])] = [0.0]*7
        else:

            ls = dic[(attrs[0],attrs[6])]
            #nb
            ls[0]= ls[0]+1

            #min angle
            if ls[1] == 0:
                ls [1] = attrs[5]
            elif attrs[5] < ls [1]:
                ls [1] = attrs[5]

            #max angle
            if ls[2] == 0:
                ls [2] = attrs[5]
            elif attrs[5] > ls [2]:
                ls [2] = attrs[5]
            #moy angle
            ls[3] = ((ls[3] * (ls[0]-1)) + attrs[5] ) /ls[0]

            dist = attrs[7]*2
            #min distance
            if ls[4] == 0:
                ls [4] = dist
            elif dist < ls [4]:
                ls [4] = dist

            #max distance
            if ls[5] == 0:
                ls [5] = dist
            elif dist > ls [5]:
                ls [5] = dist
            #moy distance
            ls[6] = ((ls[6] * (ls[0]-1)) + dist ) /ls[0]

caps = Hub_distance.dataProvider().capabilities()
if caps & QgsVectorDataProvider.DeleteFeatures:
    res = Hub_distance.dataProvider().deleteFeatures(list)

if iface.mapCanvas().isCachingEnabled():
    Hub_distance.triggerRepaint()
else:
    iface.mapCanvas().refresh()


print (dic.items())
