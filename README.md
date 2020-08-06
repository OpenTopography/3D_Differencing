[![NSF-1948997](https://img.shields.io/badge/NSF-1948997-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1948997) 
[![NSF-1948994](https://img.shields.io/badge/NSF-XXXXXXX-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1948994)
[![NSF-1948857](https://img.shields.io/badge/NSF-XXXXXXX-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1948857)



Measuring change at the Earth’s surface: On-Demand vertical and 3D topographic differencing implemented in OpenTopography

Chelsea Scott: cpscott1@asu.edu(corresponding author)

Minh Phan, Viswanath Nandigam, Christopher Crosby, Ramon Arrowsmith


A windowed implementation of the iterative closest point (ICP) algorithm is used to calculate displacement and rotation fields from topographic point clouds 
that span a geologic event of interest. This technique resolves surface deformation along and adjacent to active faults where other geodetic datasets commonly 
lack spatial resolution. 

We provide two sets of codes to perform 3D ICP differencing. 

https://github.com/OpenTopography/3D_Differencing/tree/master/3D_differencing_matlab
This option uses Matlab scripts. The Matlab script is relatively easy to set-up, although it will take a while to complete. 


https://github.com/OpenTopography/3D-Differencing/tree/master/3D_differencing_python
This option uses Python and c++ functions to perform ICP differencing. The set-up is more involved than for the Matlab option, but the scripts will run much faster.  


Pre- and post- earthquake topographic datasets for the M7 Kumamoto, Japan, earthquake are available here. 

Pre earthquake topography:
https://portal.opentopography.org/lidarDataset?opentopoID=OTLAS.052018.2444.2

Post earthquake topography:
https://portal.opentopography.org/lidarDataset?opentopoID=OTLAS.052018.2444.1


More information about ICP differencing applied to earthquakes is available in these publications: 
Scott, C. P., Arrowsmith, J. R., Nissen, E., Lajoie, L., Maruyama, T., & Chiba, T. (2018). 
The M7 2016 Kumamoto, Japan, Earthquake: 3-D Deformation Along the Fault and Within the Damage Zone Constrained From Differential Lidar Topography. Journal of Geophysical Research: 
Solid Earth. https://doi.org/10.1029/2018JB015581

Scott, C., Champenois, J., Klinger, Y., Nissen, E., Maruyama, T., Chiba, T., & Arrowsmith, R. (2019). 
2016 M7 Kumamoto, Japan, Earthquake Slip Field Derived From a Joint Inversion of Differential Lidar Topography, Optical Correlation, and InSAR Surface Displacements. 
Geophysical Research Letters. https://doi.org/10.1029/2019GL082202


