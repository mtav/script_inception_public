%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% parameters

clear all;

% filenames
outfile_1 = 'sphere_1.gwl';
outfile_2 = 'sphere_2.gwl';

% writing format
format1 = '%.3f %.3f %.3f %.3f\n';
format3 = 'Write\n';

%power compensation L = (1+k*z)*L0
k = 0.0076*2; % laserpower compensation slope
L0 = 50; % laserpower

co = 0.6 % make ellipsoid (radius in the Z direction is multiplied by c0: rz = c0*r0)

d = 5; % diameter
r0 = d/2; % radius
wall_thickness = 1; % wall thickness

voxelX = 0.25; % horizontal voxel size
voxelZ = 4*voxelX; % vertical voxel size
overlap = 0.5; % voxel overlap

deltaX = voxelX*(1-overlap); % delta X
deltaR = 0.2; % delta radius
deltaP = 6 ; % delta phi

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% top half
fileID = fopen(outfile_1, 'w');

% starting rz
r = r0;

% loop through the hulls, each with a different radius

for i = 3/4*(r0/deltaR+1):r0/deltaR+1

  phi = 0;
  theta = 0;
  % deltaT = deltaX/r/(360/deltaP);
  deltaT = asin(deltaX/r)/(360/deltaP)
  % (pi/2/deltaT+1)
  
  % create the x,y,z lists for one hull
  for j = 1:(pi/2/deltaT+1)
    x(j) = r*sin(theta)*cos(phi*2*pi/360);
    y(j) = r*sin(theta)*sin(phi*2*pi/360);
    z(j) = r*cos(theta);
    phi = phi + deltaP;
    theta = theta + deltaT;
  end

  % write the x,y,z lists for one hull
  for j = 1:2:length(x)-2
    L1 = (1+k*(z(j)+d/2)*co)*L0;
    L2 = (1+k*(z(j+1)+d/2)*co)*L0; 
    line = [x(j) y(j) (z(j)+d/2)*co L1; x(j+1) y(j+1) (z(j+1)+d/2)*co L2];
    fprintf(fileID,format1,line');
  end
  fprintf(fileID,format3);
  
  clear('x', 'y', 'z');
  r = r - deltaR;
  % deltaT = deltaT + 0.1;
end

fclose(fileID);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% bottom half
fileID = fopen(outfile_2, 'w');

r = 0;
for i = 1:r0/deltaR+1
  phi = 0;
  theta = pi/2;
  deltaT = asin(deltaX/r)/(360/deltaP);
  for j = 1:(pi/2/deltaT+1)
    x(j) = r*sin(theta)*cos(phi*2*pi/360);
    y(j) = r*sin(theta)*sin(phi*2*pi/360);
    z(j) = r*cos(theta);
    phi = phi + deltaP;
    theta = theta + deltaT;
  end
  for j = 1:2:length(x)-2
    L1 = (1+k*(z(j)+d/2)*co)*L0;
    L2 = (1+k*(z(j+1)+d/2)*co)*L0;
    line = [x(j) y(j) (z(j)+d/2)*co L1; x(j+1) y(j+1) (z(j+1)+d/2)*co L2];
    fprintf(fileID, format1, line');
  end
  fprintf(fileID, format3);
  clear('x', 'y', 'z');
  r = r + deltaR;
  %     deltaT=deltaT+0.1;
end

fclose(fileID);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% view output
system(['import_GWL.sh ', outfile_1, ' ', outfile_2]);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
