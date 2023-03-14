#%%
import pandas as pd
import geopandas as gpd
import libpysal
import xarray as xr
import rioxarray as rxr
import numpy as np
from rasterstats import zonal_stats

yr0 = 1991
yr1 = 2021


#%%
# Create empty geopandas dataframe ----
target_srs = 4326 # UTM zone 22N
all_shp = gpd.GeoDataFrame(columns = ['geometry', 'DN', 'index', 'year'], geometry = 'geometry', crs = 'EPSG:' + str(target_srs))


#%%
# Loop over each file ----
for yr in range(yr0, yr1 + 1):
    #open file
    vect_in_path = '/maps/epr26/jrc_dist_shp/jrc_dist_poly_' + str(yr) + '.shp'
    in_shp = gpd.read_file(vect_in_path)

    #transform CRS
    source_srs = in_shp.crs.srs
    if source_srs != 'EPSG:' + str(target_srs):
        in_shp = in_shp.to_crs(target_srs)

    #combine adjacent polygons
    W = libpysal.weights.Queen.from_dataframe(in_shp, silence_warnings = True)
    components = W.component_labels
    in_shp.assign(components = components)
    combined_shp = in_shp.dissolve(by = components)
    combined_shp = combined_shp.assign(index = range(len(combined_shp)))
    combined_shp = combined_shp.assign(year = yr)

    #save output
    vect_out_path = '/maps/epr26/jrc_dist_shp/jrc_dist_patch_' + str(yr) + '.shp'
    combined_shp.to_file(vect_out_path, 'ESRI Shapefile')

    #reclassify transition layer into degradation or deforestation
    rast_in_path = '/maps/epr26/jrc_dist/jrc_trans_' + str(yr) + '.tif'
    rast_out_path = '/maps/epr26/jrc_dist/jrc_reclass_' + str(yr) + '.tif'
    with rxr.open_rasterio(rast_in_path) as in_rast:
        in_rast_array = in_rast.data
        
        value_map = {12: 1, 42: 1, 13: 2, 15: 2, 23: 2, 25: 2, 26: 2, 43: 2}
        #12, 42: new degradation
        #13, 15, 23, 25, 26, 43, 45: new deforestation
        
        #create an empty array shaped like in_rast_array and filled with zeros
        reclass_array = np.zeros_like(in_rast_array, dtype = np.uint8)

        # Loop over the keys and values in the value_map dictionary
        for key, value in value_map.items():
        # Set the reclassified values for pixels with the original value
            reclass_array[in_rast_array == key] = value

        # Set all remaining pixel values to the default value (zero)
        #reclass_array[~np.isin(in_rast_array, list(value_map.keys()))] = 0

        # Replace NaN values with zero
        #reclass_array = np.nan_to_num(reclass_array, nan=0)
    
        # Set the reclassified array as a DataArray with the same coordinates and attributes as the original raster
        reclass_rast = xr.DataArray(reclass_array, coords = in_rast.coords, attrs = in_rast.attrs)
        reclass_rast.attrs['_FillValue'] = 0
        
        reclass_rast.rio.write_crs(in_rast.rio.crs)
        reclass_rast.rio.write_transform(in_rast.rio.transform())
        reclass_rast.rio.to_raster(rast_out_path)

    #calculate zonal statistics
    stats = zonal_stats(vect_out_path, rast_out_path, stats = ['sum', 'count'], geojson_out = True)
    combined_shp_stat = gpd.GeoDataFrame.from_features(stats)
    combined_shp_stat['count'] = combined_shp_stat['count'].astype(float)
    combined_shp_stat['prop'] = combined_shp_stat['sum'] / (combined_shp_stat['count'] * 2)
    combined_shp_stat = combined_shp_stat.set_crs(crs = in_shp.crs)

    # Save the dataframe as a shapefile
    combined_shp_stat.to_file('/maps/epr26/jrc_dist_shp/jrc_dist_patch_stat_' + str(yr) + '.shp', driver = 'ESRI Shapefile')
    
    #merge layers from different years
    all_shp = gpd.GeoDataFrame(pd.concat([all_shp, combined_shp_stat]))

#%%
# Save merged shapefile to file ----
out_path = '/maps/epr26/jrc_dist_shp/jrc_dist_patch_all.shp'
out_driver = 'ESRI Shapefile'
all_shp.to_file(out_path, out_driver)

# %%
