# jrc_dist
JRC-TMF disturbance detection

1. Execute jrc_dist.sh, which calls jrc_dist.r and create transition rasters from pairs of annual map rasters (remember to chmod 755 first)

1-a. For simple execution, use the following syntax: ./jrc_dist.sh F --year 1991
1-b. If using littlejohn, use the following syntax: littlejohn -j 8 -c years.csv ./jrc_dist.sh -- F

In both cases, the three argument read into the shell script are:
    1. The boolean variable which determines whether to check the transition table, which is read into jrc_dist.r
    2. The "--year" tag, which is not read into jrc_dist.r
    3. The year, which is read into jrc_dist.r


2. Execute polyg.sh, which polygonises the patches in the raster files

We do not project them because the transition matrix values will be destroyed by interpolation. This step could potentially be skipped in the future once polygonization can be successfully done in python (unsuccessful attempt in polyg.py)


3. Execute merge_stat.py, which merges adjacent polygons (with 8-connectedness), and adds zonal statistics of number of pixels with degradation/deforestation. The shapefile of each year is then merged back to one shapefile with the polygons of all years