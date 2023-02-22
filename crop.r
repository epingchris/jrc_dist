
for (i in 1991:2021) {
    dist = terra::rast(paste0("/maps/epr26/jrc_dist/jrc_dist_", i, ".tif"))
    gf_contour = terra::vect("./Disturbance/gadm41_GUF_0.shp")
    dist_cropped = terra::crop(dist, gf_contour)
    terra::writeRaster(dist_cropped, paste0("/maps/epr26/jrc_dist/jrc_dist_cropped_", i, ".tif"), overwrite = T)
    print(paste0(i, " done"))
}