
% Measuring change at the Earth�s surface: On-Demand vertical and 3D topographic differencing implemented in OpenTopography
%
% Chelsea Scott: cpscott1@asu.edu(corresponding author)
% Minh Phan, Viswanath Nandigam, Christopher Crosby, Ramon Arrowsmith

% %Copyright (c) 2007 The Regents of the University of California

%Permission to use, copy, modify, and distribute this software and its documentation for educational, research and non-profit purposes, without fee, and without a written agreement is hereby granted, provided that the above copyright notice, this paragraph and the following three paragraphs appear in all copies.

% Permission to make commercial use of this software may be obtained
% by contacting:
% Technology Transfer Office
% 9500 Gilman Drive, Mail Code 0910
% University of California
% La Jolla, CA 92093-0910
% (858) 534-5815
% invent@ucsd.edu

%THIS SOFTWARE IS PROVIDED BY THE REGENTS OF THE UNIVERSITY OF CALIFORNIA AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

%These files must be downloaded from Matlab:

%Matlab ICP File Exchange (Jacob Wilm):
%https://www.mathworks.com/matlabcentral/fileexchange/27804-iterative-closest-point

%Lasdata File Exchange (Teemu Kumpum�ki):
%https://www.mathworks.com/matlabcentral/fileexchange/48073-lasdata

clear all;close all
addpath('lasdata')

%Edit the first 5 lines
pre_dir='compare.las';%Pre-earthquake las file
post_dir='reference.las';%Post-earthquake las file
sz=51;%Differencing window size
grd=51;%Grid spacing; make equal to sz if time allows
margn=10;%Additional dimension of post-earthquake window. Must be larger than the expect surface displacement

pre=lasdata(pre_dir);%Read the pre-earthquake las file
pre_x=pre.x;pre_y=pre.y;pre_z=pre.z;%Extract terms from the Matlab structure

post=lasdata(post_dir);%Read the post-earthquake las file
post_x=post.x;post_y=post.y;post_z=post.z;%Extract terms from the Matlab structure

%Construct a core point grid for differencing
[core_x,core_y]=meshgrid([min(pre_x):grd:max(pre_x)],[min(pre_y):grd:max(pre_y)]);
core_x=core_x(:);core_y=core_y(:);

%ICP for loop
for i=1:length(core_x)
clear q* p p_*
m=core_x(i);n=core_y(i);

% Select points surrounding core point
a=find(pre_x>m-sz/2&pre_x<m+sz/2&pre_y>n-sz/2&pre_y<n+sz/2);
tz=sz+2*margn;
b=find(post_x>m-tz/2&post_x<m+tz/2&post_y>n-tz/2&post_y<n+tz/2);

%shift (0,0,0) to lie at the center of the grid
q1=mean(pre_x(a));q2=mean(pre_y(a));q3=mean(pre_z(a));
q_trans(1,:)=pre_x(a)-q1;q_trans(2,:)=pre_y(a)-q2;q_trans(3,:)=pre_z(a)-q3;
p_trans(1,:)=post_x(b)-q1;p_trans(2,:)=post_y(b)-q2;p_trans(3,:)=post_z(b)-q3;

%Perform ICP point-to-plane differencing
% Minimize point-to-plane error
%Output:
%TR:Rotation
%TT:Displacement
%ER:RMS error after each rotation
%t: Calculations time per interation
[TR, TT, ER, t] = icp(p_trans,q_trans,'Minimize','plane');

results(i,:) =[core_x(i) core_y(i) TT'];
end

%plot differencing results
figure
quiver(results(:,1)/1e3,results(:,2)/1e3,results(:,3),results(:,4),'.k','ShowArrowHead','on','LineWidth',3);hold on
scatter(results(:,1)/1e3,results(:,2)/1e3,45,results(:,5),'filled');
set(gca,'fontsize',14);xlabel('East (km)');ylabel('North (km)');title('ICP displacements');colorbar;colormap(jet)
