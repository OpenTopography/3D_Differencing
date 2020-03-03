# Measuring change at the Earth’s surface: On-Demand vertical and 3D topographic differencing implemented in OpenTopography
#  
# Chelsea Scotta: cpscott1@asu.edu(corresponding author)
# Minh Phan, Viswanath Nandigam, Christopher Crosby, Ramon Arrowsmith

# %Copyright (c) 2007 The Regents of the University of California

#Permission to use, copy, modify, and distribute this software and its documentation for educational, research and non-profit purposes, without fee, and without a written agreement is hereby granted, provided that the above copyright notice, this paragraph and the following three paragraphs appear in all copies.

# Permission to make commercial use of this software may be obtained
# by contacting:
# Technology Transfer Office
# 9500 Gilman Drive, Mail Code 0910
# University of California
# La Jolla, CA 92093-0910
# (858) 534-5815
# invent@ucsd.edu

#THIS SOFTWARE IS PROVIDED BY THE REGENTS OF THE UNIVERSITY OF CALIFORNIA AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: rockhopper
"""
import numpy as np 
import matplotlib.pyplot as plt 
import statistics
from scipy.interpolate import griddata
from scipy.spatial.transform import Rotation as R
from affine import Affine
import rasterio as rio
from rasterio.crs import CRS

window_compare=35 # THIS MUST BE DEFINED FROM BEFORE
epsg = 2444; # this needs to be set for individual datasets


no_data = -999 # no data value for creating the tiffs. 


def plot_range(data):
    color_range = abs(statistics.median(data)) + abs(1.5*np.percentile(data, 85))
    return color_range

def plot_png_3d_diff(grid_x, grid_y, points, data_to_grid,name):
    
    #grid the data. The linear grid help id nan's. 
    nan_grid = griddata(points, data_to_grid, (grid_x, grid_y), method='linear')
    data_grid = griddata(points, data_to_grid, (grid_x, grid_y), method='nearest')
    sum_data = np.sum([nan_grid*0,data_grid], axis=0)
    
    #determine the range for plotting 
    col_r = plot_range(data_to_grid)
    
    #make the plot
    fig1 = plt
    c1 = plt.pcolor(grid_x, grid_y, sum_data,vmin = -col_r, vmax = col_r, cmap = 'bwr_r')
    plt.colorbar(c1)
    plt.axis('equal')
    plt.title(name[0:len(name)-4])
    plt.xlabel("Easting")
    plt.ylabel("Northing")
    plt.savefig(name)
    plt.close()
    del fig1, c1
    
def prep_for_quiver(points,data,grid_x,grid_y,down_space):
    dx_grid = griddata(points, data, (grid_x, grid_y), method='nearest')
    dx_grid_small = dx_grid[0:-1:down_space,0:-1:down_space]
    dx_grid_small = dx_grid_small.flatten()
    return dx_grid_small    

def make_geotiff(grid_x, grid_y, points, data_to_grid,name,epsg_data,no_data):
    
    #grid the data. The linear grid help id nan's. 
    nan_grid = griddata(points, data_to_grid, (grid_x, grid_y), method='linear')
    data_grid = griddata(points, data_to_grid, (grid_x, grid_y), method='nearest')
    sum_data = np.sum([nan_grid*0,data_grid], axis=0)
    
    #set areas without data and with very large displacements to the no_data value
    a = np.isnan(sum_data)*no_data
    x_list = np.arange(0,sum_data.flatten().size,1)
    b1 = x_list[abs(sum_data.flatten()) > np.median(abs(data_to_grid))*5];
    b2 = x_list[a.flatten()==no_data];
    data_grid_flatten= data_grid.flatten()
    data_grid_flatten[b1]=no_data
    data_grid_flatten[b2]=no_data
    
    
    #reshape, as expected for geotiffs
    data_grid1= data_grid_flatten.reshape( data_grid.shape)
    data_grid1_ta=np.rot90(data_grid1)
    
    #create the affine transform 
    aff=Affine.translation(min(x)-window_compare/2, max(y)+window_compare/2)*Affine.scale(window_compare,-window_compare)

    #coordinate system for geotiffs 
    a,b=data_grid1.shape
    epsg_code = 'epsg:'+str(epsg_data)
    c=CRS.from_dict(init=epsg_code)

    d = {'driver' : 'GTiff','dtype' : 'float64','nodata': no_data, 'width': a+1, 'height' : b+1,'count':1,'crs':c,'transform':aff}

    with rio.open(name, 'w', **d) as outf:
        outf.write(data_grid1_ta, 1)
    return    
    
#load the ICP results, saved in disp.txt
disp=np.loadtxt('disp.txt',usecols=range(14))
x = disp[:,0]+window_compare/2
y = disp[:,1]+window_compare/2
dx = disp[:,2]
dy = disp[:,3]
dz = disp[:,4]
rxx = disp[:,5]
rxy = disp[:,6]
rxz = disp[:,7]
ryx = disp[:,8]
ryy = disp[:,9]
ryz = disp[:,10]
rzx = disp[:,11]
rzy = disp[:,12]
rzz = disp[:,13]

#make a grid of the x and y displacements
grid_x, grid_y = np.mgrid[min(x):max(x):window_compare, min(y):max(y):window_compare]
A = np.array([x,y])
points = np.transpose(A)

#transform the 3x3 rotation matrix to the rotation in x,y,z
x_rot = []
y_rot = [] 
z_rot = []

for i in range(len(x)):
    a = np.array([ [rxx[i], rxy[i], rxz[i]], [ryx[i], ryy[i], ryz[i]], [rzx[i], rzy[i], rzz[i]]])
    r = R.from_dcm(a)
    r1 = r.as_rotvec()
    x_rot.append(r1[0])
    y_rot.append(r1[1])
    z_rot.append(r1[2])
    
# make a quiver plot showing the displacements 
dx_grid_small = prep_for_quiver(points,dx,grid_x,grid_y,5)    
dy_grid_small = prep_for_quiver(points,dy,grid_x,grid_y,5)   
dz_grid_small = prep_for_quiver(points,dz,grid_x,grid_y,5)   

grid_x_small = grid_x[0:-1:5,0:-1:5]
grid_y_small = grid_y[0:-1:5,0:-1:5]
grid_x_small = grid_x_small.flatten()
grid_y_small = grid_y_small.flatten()

horizontal_disp = np.sqrt(dx_grid_small**2 + dy_grid_small**2)
x_list = np.arange(0,grid_x_small.size,1)
a = x_list[ horizontal_disp < np.median(horizontal_disp)*5 ];
    
fig=plt
q = plt.quiver(grid_x_small[a],grid_y_small[a],dx_grid_small[a],dy_grid_small[a])
plt.quiverkey(q, X=0.3, Y=1.1, U=10,label='Quiver key, length = 4', labelpos='E')
plt.scatter(grid_x_small[a], grid_y_small[a], np.pi*4, dz_grid_small[a] , alpha=0.5,cmap = 'bwr_r')
cbar=plt.colorbar()
cbar.set_label("Vertical Elevation Change")
plt.title("ICP displacements")
plt.xlabel("Easting")
plt.ylabel("Northing")
plt.savefig('3D_displacements')
plt.close()
     
#make the displacement plots  
plot_png_3d_diff(grid_x, grid_y, points,dx, "dx.png")
plot_png_3d_diff(grid_x, grid_y, points,dy, "dy.png")
plot_png_3d_diff(grid_x, grid_y, points,dz, "dz.png")    

#make the rotation plots
plot_png_3d_diff(grid_x, grid_y, points,np.array(x_rot), "x_rot.png")
plot_png_3d_diff(grid_x, grid_y, points,np.array(y_rot), "y_rot.png")
plot_png_3d_diff(grid_x, grid_y, points,np.array(z_rot), "z_rot.png") 

#make the geotiffs 
make_geotiff(grid_x, grid_y, points,dx, "dx.tif",epsg,no_data)
make_geotiff(grid_x, grid_y, points,dy, "dy.tif",epsg,no_data)
make_geotiff(grid_x, grid_y, points,dz, "dz.tif",epsg,no_data)
make_geotiff(grid_x, grid_y, points,np.array(x_rot), "rot_x.tif",epsg,no_data)
make_geotiff(grid_x, grid_y, points,np.array(y_rot), "rot_y.tif",epsg,no_data)
make_geotiff(grid_x, grid_y, points,np.array(z_rot), "rot_z.tif",epsg,no_data)

    
    
    
  
    
    
    
    
    
    