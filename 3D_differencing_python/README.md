Measuring change at the Earth’s surface: On-Demand vertical and 3D topographic differencing implemented in OpenTopography

Chelsea Scott: cpscott1@asu.edu(corresponding author)

Minh Phan, Viswanath Nandigam, Christopher Crosby, Ramon Arrowsmith

This code performs 3D ICP differencing. It calculates the displacement and rotation required to align windowed subsets of point cloud topography.

This code has been applied to calculate 3D displacement during the M7 Kumamoto, Japan, earthquake. The data is available here from OpenTopography:

Pre earthquake topography:
https://portal.opentopography.org/lidarDataset?opentopoID=OTLAS.052018.2444.2

Post earthquake topography:
https://portal.opentopography.org/lidarDataset?opentopoID=OTLAS.052018.2444.1


Instructions:

1) Place the compare.las (pre-event) and reference.las (post-event) in the directory las_diff

2) Download lastools: https://rapidlasso.com/lastools/
Then run lastile to tile the datasets. Specify tilesize. For this example, the tile size is 51 m.

lastile -i compare.las -tile_size 51 -o las_diff/compare
lastile -i reference.las -tile_size 51 -buffer 15 -o las_diff/reference


3) make_list_tiles.y: This script creates tiles.txt which has x, y coordinates of the tiles in common to both datasets.


4) Download and complile  LASTools - https://rapidlasso.com/lastools/
The lasreader from laslib is called in the libICP scripts.

LibICP was written by Andreas Geiger (https://github.com/symao/libicp)

We updated demo.cpp and CMakeLists.txt files. OpenTopography's fork of the libicp repo with updates files is here: https://github.com/OpenTopography/libicp

5) Postprocessing: post_processing.py
This file reads the disp.txt and outputs geotifs and pngs of the 3D displacements and rotations.
 
