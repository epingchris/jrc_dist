#receive year argument from shell script to calculate transition between a pair of annual JRC-TMF maps

library(terra)

#get arguments
args = commandArgs(TRUE)
check_freq = as.logical(args[1])
cat("\ncheck_freq is: ", check_freq)
year1 = as.character(args[2])
year0 = as.character(as.numeric(year1) - 1)
cat("\nyear1 is: ", year1)
cat("\nyear0 is: ", year0)

rast_trans = terra::rast(paste0("/maps/epr26/jrc_dist/jrc_trans_", year1, ".tif"))

regrowth_class = c(14, 24, 34, 51, 52, 54, 64)
rast_regrowth = terra::app(rast_trans, fun = function(x) ifelse(x %in% regrowth_class, 1, NA))

#save output
outpath_regrowth = paste0("/maps/epr26/jrc_dist/jrc_regrowth_", year1, ".tif")
terra::writeRaster(rast_regrowth, filename = outpath_regrowth, overwrite = T)
