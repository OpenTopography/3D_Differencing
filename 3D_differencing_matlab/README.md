Measuring change at the Earth’s surface: On-Demand vertical and 3D topographic differencing implemented in OpenTopography
  
Chelsea Scott: cpscott1@asu.edu(corresponding author)

Minh Phan, Viswanath Nandigam, Christopher Crosby, Ramon Arrowsmith

This code performs 3D differencing on Matlab. This script will calculate the displacement and rotation required to align windowed subsets of point cloud topography. 

This code has been applied to calculate 3D displacement during the M7 Kumamoto, Japan, earthquake. The data is available here from OpenTopography: 

Pre earthquake topography:
https://portal.opentopography.org/lidarDataset?opentopoID=OTLAS.052018.2444.2

Post earthquake topography:
https://portal.opentopography.org/lidarDataset?opentopoID=OTLAS.052018.2444.1


These scripts must be downloaded from Matlab: 

Matlab ICP File Exchange (Jacob Wilm): 
https://www.mathworks.com/matlabcentral/fileexchange/27804-iterative-closest-point

Lasdata File Exchange (Teemu Kumpumäki):
https://www.mathworks.com/matlabcentral/fileexchange/48073-lasdata

The input files are: 
compare.las: pre-event las point cloud file
reference.las: post-event las point cloud file
