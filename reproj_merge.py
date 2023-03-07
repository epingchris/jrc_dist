#%%
import pandas as pd
import geopandas as gpd
import libpysal

yr0 = 1991
yr1 = 2021


#%%
# Create empty geopandas dataframe ----
all_shp = gpd.GeoDataFrame(columns = ['geometry', 'DN', 'index', 'year'], geometry = 'geometry', crs = 'EPSG:' + str(target_srs))


#%%
# Loop over each file ----
for yr in range(yr0, yr1 + 1):
    #open file
    in_path = '/maps/epr26/jrc_dist_shp/jrc_dist_poly_' + str(yr) + '.shp'
    in_shp = gpd.read_file(in_path)

    #transform CRS
    source_srs = in_shp.crs.srs
    target_srs = 32622 # UTM zone 22N
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
    out_path = '/maps/epr26/jrc_dist_shp/jrc_dist_patch_' + str(yr) + '.shp'
    out_driver = 'ESRI Shapefile'
    combined_shp.to_file(out_path, out_driver)
    
    #merge layers from different years
    all_shp = gpd.GeoDataFrame(pd.concat([all_shp, combined_shp]))

#%%
# Save merged shapefile to file ----
out_path = '/maps/epr26/jrc_dist_shp/jrc_dist_patch_all.shp'
out_driver = 'ESRI Shapefile'
all_shp.to_file(out_path, out_driver)

# %%
