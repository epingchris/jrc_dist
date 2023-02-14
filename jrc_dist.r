library(terra)

args = commandArgs(TRUE)
check_freq = as.logical(args[1])
cat("\ncheck_freq is: ", check_freq)
year1 = as.character(args[2])
year0 = as.character(as.numeric(year1) - 1)
cat("\nyear1 is: ", year1)
cat("\nyear0 is: ", year0)

inpath0 = paste0("/maps/epr26/JRC_TMF_60W_10N/JRC_TMF_AnnualChange_v2_", year0, "_SAM_ID49_N10_W60.tif")
inpath1 = paste0("/maps/epr26/JRC_TMF_60W_10N/JRC_TMF_AnnualChange_v2_", year1, "_SAM_ID49_N10_W60.tif")

rast_jrc0 = terra::rast(inpath0)
rast_jrc1 = terra::rast(inpath1)

#create transition raster
rast_trans = rast_jrc0 * 10 + rast_jrc1
#12, 42: new degradation
#13, 15, 23, 25, 26, 43, 45: new deforestation
#14, 24, 34, 51, 52, 54, 64: regrowth

if (check_freq) {
  #create transition tables for each year
  freqtab = terra::freq(rast_trans)

  #check if a transition type is existent
  print(as.vector(freqtab[freqtab$value == 32, ])[[3]])
}

dist_class = c(12, 42, 13, 15, 23, 25, 26, 43, 45) # nolint: assignment_linter.
rast_dist = terra::app(rast_trans, fun = function(x) ifelse(x %in% dist_class, 1, NA))

outpath_trans = paste0("/maps/epr26/jrc_dist/jrc_trans_", year1, ".tif")
outpath_dist = paste0("/maps/epr26/jrc_dist/jrc_dist_", year1, ".tif")
terra::writeRaster(rast_trans, filename = outpath_trans, overwrite = T)
terra::writeRaster(rast_dist, filename = outpath_dist, overwrite = T)

#check results ----
aaa = terra::rast("/maps/epr26/jrc_dist/jrc_trans_1993.tif")
bbb = terra::rast("/maps/epr26/jrc_dist/jrc_dist_1993.tif")
(dffreq = as.data.frame(terra::freq(aaa)))
sum(dffreq[dffreq$value %in% dist_class, ]$count)
terra::freq(bbb)