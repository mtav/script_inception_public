close all;
clear all;

lambda_mum=0.670;
m=1;
n=1;
ff=0.3;
Nrings = 1;
phi = linspace(0,Nrings*2*pi,1000);
rlist = linspace(-ff/2, ff/2, 10);
dwell=800; % Dwell time (us).
mag=100000; % Magnification.
rep=10; % Repetitions.

rin=(n-ff/2+m*phi/(2*pi))*lambda_mum;
rout=(n+ff/2+m*phi/(2*pi))*lambda_mum;
rcen=(n+m*phi/(2*pi))*lambda_mum;

close all;
figure;
hold on;

polar(phi,rin,'r-');
polar(phi,rcen,'g-');
polar(phi,rout,'b-');

for idx = 1:length(rlist)
  r = (n + rlist(idx) + m*phi/(2*pi))*lambda_mum;
  polar(phi, r, 'k-');
end

%%%%%%%%PARAMTERS%%%%%%%%%%%%%%%%%%%%%%%%%%%
%r=2;  % Width of the square (um).
%N=15;  % Number of rotations of the spiral
% numPoints=10000; %  METHOD 0: total number of pixels to be etched.
%c=14;  % METHOD 1: A constant defining number of points of the smallest circle.
% % e=1.7;   % Ellipticity.  Measure of how elliptical the feture is.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

[res, HFW] = getResolution(mag);
if (r>HFW/2)
  'Feature is too big for this magnification level..' 
  return;
end
%R = r/res; % Radius in pixels.
lambda_pxl = lambda_mum/res
%numPoints = 2*pi*R*N;

%t = [];
%METHOD 0
  %t=linspace(0,2*N*pi,numPoints);
%METHOD 1
 %for i=1:N
     %t=[t,2*pi*linspace(i-1,i,i*c)];
 %end
%METHOD 2
 %v=fliplr(10-logspace(log10(1),1,260))/9;
 %t=2*N*pi*v;
%%%%%%%%%%%%%%%%%%%%%%%%%%%

total_coordinates = [];

%rlist = [0]

Xoffset_pxl = 2048;
Yoffset_pxl = 2048+280;

for idx = 1:length(rlist)
  %maxt = max(t);
  %radius = R*t/maxt;
  radius = (n + rlist(idx) + m*phi/(2*pi))*lambda_pxl;
  x = round(radius.*cos(phi));
  y = round(radius.*sin(phi));

  %x = x-min(x)-round(0.5*(min(x)+max(x))) +2048;
  %y = y-min(y)-round(0.5*(min(y)+max(y))) +280+2048;

  x = x + Xoffset_pxl;
  y = y + Yoffset_pxl;

  c = [x',y'];
  [mixed,k] = unique(c,'rows');
  kk = sort(k);
  coordinates = c(kk,:)';
  size(coordinates)
  total_coordinates = [total_coordinates, coordinates];
  
  phi = fliplr(phi);
end

size(total_coordinates)

writeStrFile('spiral_grating.str', total_coordinates(1,:), total_coordinates(2,:), dwell*ones(size(total_coordinates(1,:))), rep);
readStrFile('spiral_grating.str',mag);

figure(2);
subplot(1,2,2);
hold on;


plot(rin.*cos(phi) + Xoffset_pxl*res, rin.*sin(phi) + Yoffset_pxl*res, 'k-o');
plot(rcen.*cos(phi) + Xoffset_pxl*res, rcen.*sin(phi) + Yoffset_pxl*res, 'm-o');
plot(rout.*cos(phi) + Xoffset_pxl*res, rout.*sin(phi) + Yoffset_pxl*res, 'k-o');

%polar(phi,rin,'r-');
%polar(phi,r,'g-');
%polar(phi,rout,'b-');
%for idx = 1:length(rlist)
  %r = (n + rlist(idx) + m*phi/(2*pi))*lambda_mum;
  %polar(phi, r, 'k-');
%end
