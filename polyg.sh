#!/bin/bash

#polygonize
for i in {1991..2021}
do
  gdal_polygonize.py -8 /maps/epr26/jrc_dist/jrc_dist_$i.tif -f "ESRI Shapefile" /maps/epr26/jrc_dist_shp/jrc_dist_poly_$i.shp
  gdal_polygonize.py -8 /maps/epr26/jrc_dist/jrc_dist_prj_$i.tif -f "ESRI Shapefile" /maps/epr26/jrc_dist_shp/jrc_dist_poly_prj_$i.shp
done
