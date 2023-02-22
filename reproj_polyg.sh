#!/bin/bash

for i in {1995..2021}
do
  gdalwarp -s_srs EPSG:4326 -t_srs EPSG:32622 -r bilinear /maps/epr26/jrc_dist/jrc_dist_cropped_$i.tif /maps/epr26/jrc_dist/jrc_dist_prj_$i.tif
done

gdal_polygonize.py /maps/epr26/jrc_dist/jrc_dist_prj_1991.tif -f "ESRI Shapefile" jrc_dist_poly_1991_test.shp
