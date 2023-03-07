#%%
from osgeo import gdal, ogr, osr

#%%
#read raster
in_path = '/maps/epr26/jrc_dist/jrc_dist_cropped_1991.tif'
in_rast = gdal.Open(in_path)
in_band = in_rast.GetRasterBand(1)

#Get input layer's source coordinate system
source_crs = in_band.GetSpatialRef()

#Create a transformation object from source to target CRS
target_crs = osr.SpatialReference()
target_crs.SetFromUserInput('EPSG:32622') # UTM zone 22N
if source_crs != target_crs:
    transform = osr.CoordinateTransformation(source_crs, target_crs)

#create output file attributes
driver = ogr.GetDriverByName('ESRI Shapefile')
out_path = '/maps/epr26/jrc_dist_shp/jrc_dist_patch_1991_new.shp'
out_shp = driver.CreateDataSource(out_path)

out_layername = 'dist_1991'
out_layer = out_shp.CreateLayer(out_layername, srs = target_crs)

fld = ogr.FieldDefn('patch', ogr.OFTInteger)
out_layer.CreateField(fld)
out_field = out_layer.GetLayerDefn().GetFieldIndex('patch')

gdal.Polygonize(in_band, None, out_layer, [8CONNECTED = 8], callback = None)
gdal.Polygonize(in_band, None, out_layer, 8CONNECTED = 8, callback = None)

gdal.Polygonize(in_band, None, out_layer, out_field, [], callback = None)

del in_rast, out_shp