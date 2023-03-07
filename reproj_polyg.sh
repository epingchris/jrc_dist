#!/bin/bash

#reproject from global to local CRS; subsequently integrated into patch.py
for i in {1991..2021}
do
  gdalwarp -s_srs EPSG:4326 -t_srs EPSG:32622 -r bilinear /maps/epr26/jrc_dist/jrc_dist_$i.tif /maps/epr26/jrc_dist/jrc_dist_prj_$i.tif
done

#polygonize; not yet integrated into patch.py
for i in {1991..2021}
do
  gdal_polygonize.py -8 /maps/epr26/jrc_dist/jrc_dist_prj_$i.tif -f "ESRI Shapefile" /maps/epr26/jrc_dist_shp/jrc_dist_poly_$i.shp
done
