library(terra)

args = commandArgs(TRUE)
rast_length = as.numeric(args[1])
cat("rast_length is: ", rast_length, "\n")
check_freq = as.logical(args[2])
cat("check_freq is: ", check_freq, "\n")
inpath = as.character(args[3])
cat("inpath is: ", inpath, "\n")

aa = 12

infile = list.files(path = inpath, pattern = ".tif$", all.files = T, full.names = T)
rast_list = terra::rast(infile)
rast_trans = vector("list", length = rast_length)
rast_dist = vector("list", length = rast_length)

#create transition rasters for each year
for (i in seq_along(rast_trans)) {
  a = Sys.time()
  rast_trans[[i]] = rast_list[[i]] * 10 + rast_list[[i + 1]]
  #12, 42: new degradation
  #13, 15, 23, 25, 26, 43, 45: new deforestation
  #14, 24, 34, 51, 52, 54, 64: regrowth
  b = Sys.time()
  print(b - a)
}

if (check_freq) {
  #create transition tables for each year
  freqtab = vector("list", length = (nlyr(rast_list) - 1))
  for (i in seq_along(rast_trans)) {
    freqtab[[i]] = terra::freq(rast_trans[[i]])
  }

  #check if a transition type is existent
  for (i in seq_along(rast_trans)) {
    print(as.vector(freqtab[[i]][freqtab[[i]]$value == 32, ])[[3]])
  }
}

dist_class = c(12, 42, 13, 15, 23, 25, 26, 43, 45) # nolint: assignment_linter.
for (i in seq_along(rast_trans)) {
  a = Sys.time()
  rast_dist[[i]] = terra::app(rast_trans[[i]], fun = function(x) ifelse(x %in% dist_class, 1, NA))
  b = Sys.time()
  print(b - a)
  #1.6 min
}

rast_trans = terra::rast(rast_trans)
rast_dist = terra::rast(rast_dist)

outpath_trans = "/maps/epr26/jrc_dist/jrc_trans.tif"
outpath_dist = "/maps/epr26/jrc_dist/jrc_dist.tif"
terra::writeRaster(rast_trans, filename = outpath_trans, overwrite = T)
terra::writeRaster(rast_dist, filename = outpath_dist, overwrite = T)