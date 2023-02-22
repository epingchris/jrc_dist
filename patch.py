#%%
from osgeo import ogr, osr

for year in range(1991, 2022):
    # Open the input shapefile ----
    in_path = '/maps/epr26/jrc_dist_shp/jrc_dist_poly_' + str(year) + '.shp'
    in_driver = ogr.GetDriverByName('ESRI Shapefile')
    in_shp = in_driver.Open(in_path, 0)
    in_layer = in_shp.GetLayer()

    # Transform CRS ----
    #Get input layer's source coordinate system
    source_crs = in_layer.GetSpatialRef()
    target_crs = 'EPSG:32622' # UTM zone 22N
    target_srs = osr.SpatialReference()
    target_srs.SetFromUserInput(target_crs)

    #Create a transformation object from source to target CRS
    if source_crs != target_crs:
        transform = osr.CoordinateTransformation(source_crs, target_srs)

#%%
    # Define output buffer shapefile and layer ----
    out_path = '/maps/epr26/jrc_dist_shp/jrc_dist_patch_' + str(year) + '.shp'
    out_driver = ogr.GetDriverByName('ESRI Shapefile')
    out_shp = out_driver.CreateDataSource(out_path)
    out_layer = out_shp.CreateLayer('output_buffer', target_srs, geom_type = ogr.wkbPolygon)

#%%
    # add very small buffer to remove holes ----
    for in_feature in in_layer:
    
        # Get the geometry of the feature
        geometry = in_feature.GetGeometryRef()

        # Create a buffer around the geometry with a very small distance
        bufferGeometry = geometry.Buffer(0.000001) # in the units of the input geometry's coordinate reference system

        # Add the buffer geometry to the output layer
        out_feature = ogr.Feature(out_layer.GetLayerDefn())
        out_feature.SetGeometry(bufferGeometry)
        out_layer.CreateFeature(out_feature)

        # Clean up
        out_feature = None

    in_shp = None
    out_shp = None