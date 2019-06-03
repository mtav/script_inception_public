%%%%%%%%PARAMETERS%%%%%%%%%%%%%%%%%%%%%%%%%%%
dwell=800; % Dwell time (us).
mag=200000; % Magnification.
rep=1; % Repetitions.

r=0.02;  % Width of the square (um).
writeToFile=1;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

[res, HFW] = getResolution(mag);
if (r/1e3>HFW/2)
  'Feature is too big for this magnification level..' 
  return;
end

R=r/res; % Radius in pixels.

numPoints=2*pi*R^2;

t = [];

t=linspace(0,2*R*pi,numPoints);

x = round(1/2/pi*t.*cos(t));
y = round(1/2/pi*t.*sin(t));

x=x-min(x)+2048-round(R);
y=y-min(y)+280+2048-round(R);

c=[x',y'];
[mixed,k]=unique(c,'rows');
kk=sort(k);
coordinates=c(kk,:)';
% lineLength(coordinates)
x=coordinates(1,:);
y=coordinates(2,:);

x=x+2048-round((min(x)+max(x))/2);
y=y+1980-round((min(y)+max(y))/2);


figure(2)
plot(x,y)
title([num2str(size(coordinates,2)),' Points']);
axis tight;

axis equal

if writeToFile
  % Write to file.
  folder=uigetdir();
  fid=fopen([folder,'\holeSp_mag',num2str(mag),'_r',num2str(r),'um.str'],'w+');
  fprintf(fid,'s\r\n%i\r\n%i\r\n',rep,length(x));
  fprintf(fid,[num2str(dwell),' %i %i\r\n'],[x;y]);
  fclose(fid);
end
