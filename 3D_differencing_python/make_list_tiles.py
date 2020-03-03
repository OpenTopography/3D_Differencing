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

#This script creates tiles.txt which has x, y coordinates of the tiles in common to both datasets. 
#the compare.las and reference.las must be in the directory las_diff



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: rockhopper
"""
import os 
import numpy as np
import os.path



window_compare=35;#option to user to be changes for every iteration 


#get the compare coordinates of the tiles
os.system('ls las_diff/compare*las >compare_las')
os.system('cut -d_ -f 3 compare_las >compare_x')
os.system('cut -d_ -f 4 compare_las >compare_y1')
os.system('cut -d. -f 1 compare_y1 >compare_y')

#get the reference coordinates of the tiles
os.system('ls las_diff/reference*las >reference_las')
os.system('cut -d_ -f 3 reference_las >reference_x')
os.system('cut -d_ -f 4 reference_las >reference_y1')
os.system('cut -d. -f 1 reference_y1 >reference_y')

#load in the x, y coordinates of the compare and reference datasets
a = open("compare_x", "r")
compare_x = a.read().splitlines()
a.close()
compare_x=[int(i) for i in compare_x]

a = open("compare_y", "r")
compare_y = a.read().splitlines()
a.close()
compare_y=[int(i) for i in compare_y]

a = open("reference_x", "r")
reference_x = a.read().splitlines()
a.close()
reference_x=[int(i) for i in reference_x]

a = open("reference_y", "r")
reference_y = a.read().splitlines()
a.close()
reference_y=[int(i) for i in reference_y]

# define the core points 
minx=min(compare_x+reference_x)
maxx=max(compare_x+reference_x)
miny=min(compare_y+reference_y)
maxy=max(compare_y+reference_y)

core_x=list(range(minx,maxx,window_compare));
core_y=list(range(maxy,miny,-window_compare));
icp_process1=[1];

#write a list of tiles common to both datasets
outF = open("tiles.txt", "w")

for i in range(1,len(compare_x)):
    compare_search_x = compare_x[i];
    compare_search_y = compare_y[i];
    
    same_x = np.where(reference_x== np.array(compare_search_x))[0];
    same_y = np.where(reference_y== np.array(compare_search_y))[0];
    same_element = 0;
    for p in same_x:
        pairs = np.where(p== same_y)[0];
        if len(pairs)>0:
            same_element=1
    if same_element ==1:
        icp_process1.append([compare_search_x, compare_search_y])
        outF.write(str([compare_search_x]).strip('[]'))
        outF.write(str(' '))
        outF.write(str([compare_search_y]).strip('[]'))
        outF.write("\n")
        
outF.close()  
