import processing
#building clip (cleaned)
processing.run("native:clip", { 'INPUT' : 'C:/stage/paris3/voronoi/batiment_single_polygon.shp', 'OUTPUT' : 'G:/805/batiment_single_polygon_clip.shp', 'OVERLAY' : 'G:/629/eqasim-java/gis/paris.shp' })
#filter osm shp with "drive"
processing.run("native:extractbyexpression", { 'EXPRESSION' : '"fclass" NOT LIKE \'cycleway\'\nAND "fclass" NOT LIKE \'footway\'\nAND "fclass" NOT LIKE \'path\'\nAND "fclass" NOT LIKE \'pedestrian\'\nAND "fclass" NOT LIKE \'service\'\nAND "fclass" NOT LIKE \'steps\'\nAND "fclass" NOT LIKE \'track\'\n', 'INPUT' : 'G:/805/paris_osm.shp', 'OUTPUT' : 'G:/805/paris_osm_filter.shp' })
#add index to building
processing.run("native:fieldcaculator", { 'FIELD_LENGTH' : 10, 'FIELD_NAME' : 'id', 'FIELD_PRECISION' : 3, 'FIELD_TYPE' : 1, 'FORMULA' : '@row_number', 'INPUT' : 'G:/805/batiment_single_polygon_clip.shp', 'OUTPUT' : 'G:/805/batiment_single_polygon_clip_index.shp' })
#convert buildings to points
processing.run("native:boundary", { 'INPUT' : 'G:/805/batiment_single_polygon_clip_index.shp', 'OUTPUT' : 'G:/805/batiment_single_polygon_clip_index_boundary.shp' })
processing.run("native:densifygeometriesgivenaninterval", { 'INPUT' : 'G:/805/batiment_single_polygon_clip_index_boundary.shp', 'INTERVAL' : 3, 'OUTPUT' : 'G:/805/batiment_single_polygon_clip_index_boundary_densify.shp' })
processing.run("native:extractvertices", { 'INPUT' : 'G:/805/batiment_single_polygon_clip_index_boundary_densify.shp', 'OUTPUT' : 'G:/805/batiment_single_polygon_clip_index_boundary_densify3_point.shp' })
#get distance line (with centerline and buildings)
processing.run("native:clip", { 'INPUT' : 'G:/805/linestrings_single.shp', 'OUTPUT' : 'G:/805/linestrings_single_clip.shp', 'OVERLAY' : 'G:/629/eqasim-java/gis/paris.shp' })
processing.run("native:extractvertices", { 'INPUT' : 'G:/805/linestrings_single_clip.shp', 'OUTPUT' : 'G:/805/linestrings_single_clip_point.shp' })
processing.run("qgis:distancetonearesthublinetohub", { 'FIELD' : 'id', 'HUBS' : 'G:/805/batiment_single_polygon_clip_index_boundary_densify3_point.shp', 'INPUT' : 'G:/805/linestrings_single_clip_point.shp', 'OUTPUT' : 'G:/805/linestrings_buildings.shp', 'UNIT' : 0 })
#get intersection points (distance line and osm network)
processing.run("native:lineintersections", { 'INPUT' : 'G:/805/linestrings_buildings.shp', 'INPUT_FIELDS' : ['FID','vertex_ind','HubName',’HubDist’], 'INTERSECT' : 'G:/805/paris_osm_filter.shp', 'INTERSECT_FIELDS' : ['osm_id'], 'INTERSECT_FIELDS_PREFIX' : '', 'OUTPUT' : 'G:/805/linestrings_buildings-intersection-paris_osm_filter.shp' })
