# Measuring change at the Earth’s surface: On-Demand vertical and 3D topographic differencing implemented in OpenTopography
#  
# Chelsea Scotta: cpscott1@asu.edu(corresponding author)
# Minh Phan, Viswanath Nandigam, Christopher Crosby, Ramon Arrowsmith



Instructions: 

1) Place the compare.las and reference.las in the directory las_diff

2) Download lastools: https://rapidlasso.com/lastools/
Then run lastile to tile the datasets. Specify tilesize. For this example, the tile size is 51 m. 

lastile -i compare.las -tile_size 51 -o las_diff/compare 
lastile -i reference.las -tile_size 51 -buffer 15 -o las_diff/reference 


3) make_list_tiles.y: This script creates tiles.txt which has x, y coordinates of the tiles in common to both datasets. 


4) Download and complile on c++: 
laslib : https://github.com/LAStools/LAStools/tree/master/LASli
The lasreader from laslib is called to do the ICP. 

LibICP: https://github.com/symao/libicp

LibICP is written by Andreas Geiger and is made available under the General Public License. 
We have edited the demo.cpp script to perform windowed ICP. 
Replace the libicp-master\src\demo.cpp with the demo.cpp included here. 

Here are the directions to run the ICP. 
a) Move to libicp root directory
b) Type 'cmake .'
c) Type 'make'
d) Run './icp' (demo program)

This will generate a text file disp.txt with the results of the ICP.

5) Postprocessing: post_processing.py
This file reads the disp.txt and outputs geotifs and pngs of the 3D displacements and rotations. 
 








