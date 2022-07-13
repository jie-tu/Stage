def layer(path_to_layer,name_layer):
    vlayer = QgsVectorLayer(path_to_layer,name_layer,"ogr")
    QgsProject.instance().addMapLayer(vlayer)
    return vlayer

path_to_linestrings_simplify = "C:/stage/paris3/simple/linestrings_simplify100.shp"
linestrings_simplify = layer (path_to_linestrings_simplify,"linestrings_simplify")

features = linestrings_simplify.getFeatures()

point_to_line = {}
for feature in features:
    geom = feature.geometry()
    geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
    if geom.type() == QgsWkbTypes.LineGeometry:
        if geomSingleType:
            x = geom.asPolyline()
            if x[0] not in point_to_line.keys():
                point_to_line [x[0]] = [feature.id()]
            else:
                point_to_line [x[0]].append(feature.id())

            if x[1] not in point_to_line.keys():
                point_to_line [x[1]] = [feature.id()]
            else:
                point_to_line [x[1]].append(feature.id())
        else:
            x = geom.asMultiPolyline()

            if x[0][0] not in point_to_line.keys():
                point_to_line [x[0][0]] = [feature.id()]
            else:
                point_to_line [x[0][0]].append(feature.id())

            if x[0][1] not in point_to_line.keys():
                point_to_line [x[0][1]] = [feature.id()]
            else:
                point_to_line [x[0][1]].append(feature.id())

    else:
        print("Unknown or invalid geometry")
    #break
#print (point_to_line)

caps = linestrings_simplify.dataProvider().capabilities()

features = linestrings_simplify.getFeatures()

new_line ={}
for feature in features:
    geom = feature.geometry()
    geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
    if geom.type() == QgsWkbTypes.LineGeometry:

        if geomSingleType:
            x = geom.asPolyline()
            print("Line: ", x[0], "length: ", geom.length())
        else:
            x = geom.asMultiPolyline()

            if (geom.length()<30):

                x0 = x[0][0].x()
                y0 = x[0][0].y()
                x1 = x[0][1].x()
                y1 = x[0][1].y()
                #get center
                new_x = ( x0 + x1 ) / 2
                new_y = ( y0 + y1 ) / 2
                #get list line
                list1 = point_to_line [x[0][0]]
                list2 = point_to_line [x[0][1]]
                list1.extend(list2)

                for line_fid in list1:
                    voisin = linestrings_simplify.getFeature(line_fid)
                    voisin_geom = voisin.geometry()
                    voisin_line = voisin_geom.asMultiPolyline()
                    x2 = voisin_line[0][0].x()
                    y2 = voisin_line[0][0].y()
                    x3 = voisin_line[0][1].x()
                    y3 = voisin_line[0][1].y()

                    if line_fid in new_line:
                        voisin_geom = new_line[line_fid]
                        voisin_line = voisin_geom.asMultiPolyline()
                        x2 = voisin_line[0][0].x()
                        y2 = voisin_line[0][0].y()
                        x3 = voisin_line[0][1].x()
                        y3 = voisin_line[0][1].y()

                    if ( x0 == x2 and y0 == y2) :
                        new_geom = QgsGeometry.fromMultiPolylineXY([[QgsPointXY(new_x,new_y),QgsPointXY(x3,y3)]])
                        new_line[line_fid] = new_geom
                    if ( x0 == x3 and y0 == y3) :
                        new_geom = QgsGeometry.fromMultiPolylineXY([[QgsPointXY(new_x,new_y),QgsPointXY(x2,y2)]])
                        new_line[line_fid] = new_geom
                    if ( x1 == x2 and y1 == y2) :
                        new_geom = QgsGeometry.fromMultiPolylineXY([[QgsPointXY(new_x,new_y),QgsPointXY(x3,y3)]])
                        new_line[line_fid] = new_geom
                    if ( x1 == x3 and y1 == y3) :
                        new_geom = QgsGeometry.fromMultiPolylineXY([[QgsPointXY(new_x,new_y),QgsPointXY(x2,y2)]])
                        new_line[line_fid] = new_geom
    else:
        print("Unknown or invalid geometry")

for key, value in new_line.items():
    #linestrings_simplify.ChangeGeometry (key,value)
    if caps & QgsVectorDataProvider.ChangeGeometries:
        linestrings_simplify.dataProvider().changeGeometryValues({ key : value })

if iface.mapCanvas().isCachingEnabled():
    linestrings_simplify.triggerRepaint()
else:
    iface.mapCanvas().refresh()

print("done")
