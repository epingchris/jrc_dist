# jrc_dist
JRC-TMF disturbance detection

1. Execute jrc_dist.sh, which calls jrc_dist.r and create transition rasters from pairs of annual map rasters

1-a. For simple execution, use the following syntax: ./jrc_dist.sh F --year 1991
1-b. If using littlejohn, use the following syntax: littlejohn -j 8 -c years.csv ./jrc_dist.sh -- F

In both cases, the three argument read into the shell script are:
    1. The boolean variable which determines whether to check the transition table, which is read into jrc_dist.r
    2. The "--year" tag, which is not read into jrc_dist.r
    3. The year, which is read into jrc_dist.r


2. Execute reproj_polyg.sh, which transforms the rasters from geodetic to projected reference system and polygonises them

This step could potentially be skipped in the future as there is also a part of code in reproj_buffer.py which does the reprojection, but the polygonisation part hasn't worked yet in python (attempt in polyg.py)


3. Execute reproj_merge.py, which transforms the rasters from geodetic to projected reference system (if not already done by reproj_polyg), and merges adjacent polygons (with 8-connectedness), and merge back to one shapefile with the polygons of all years