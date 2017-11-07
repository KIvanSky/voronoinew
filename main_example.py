#! /usr/local/bin/python

import sys
import voronoi_poly
import pandas as pd

#Run this using the pipe: "cat sample_city_data.cat | python main_example.py"
if __name__=="__main__":

  #Creating the PointsMap from the input data
  PointsMap = {}
  data = pd.read_csv('sample_city_data.csv')

  for i in range(0, len(data)):
    list_index = list(data.index)

    PointsMap[list_index[i]] = (float(data.iloc[i].x), float(data.iloc[i].y))
  '''PointsMap={}
  for line in sys.stdin:
    data=line.strip().split(",")
    try:
      PointsMap[data[0]]=(float(data[1]),float(data[2]))
    except:
      sys.stderr.write( "(warning) Invalid Input Line: "+line)'''

  #1. Stations, Lines and edges
  #vl=voronoi_poly.VoronoiLineEdges(PointsMap)

  #print vl

  #2. Polygons
  #vl=voronoi_poly.VoronoiPolygons(PointsMap, BoundingBox="W", PlotMap=False)
  #print vl
  #from shapely.geometry import Polygon

  #print list(polygon_data.exterior.coords)

  #3. Quadkey-based Grids on Polygons
  vl = voronoi_poly.VoronoiPolygons(PointsMap, BoundingBox="W", PlotMap=True)
  voronoi_poly.GridVoronoi(vl, zl=1, PlotMap=True)

  #4. GeoJson Polygons
  #voronoi_poly.VoronoiGeoJson_Polygons(PointsMap, BoundingBox="W", PlotMap=False)

  #5. GeoJson MultiPolygons
  #voronoi_poly.VoronoiGeoJson_MultiPolygons(PointsMap, BoundingBox="W", PlotMap=False)

  
  
