%This file creates a .geo file with cylinder holes.

%x centre
%y centre
%z centre
%radius 1
%radius 2
%height
%permittivity
%conductivity
 
xoffset = sqrt(3)*0.24341044; % sqrt(3)*a: x distance between holes in alternate rows originaly 0.840000
zoffset = 0.24341044; % a: (pitch)ez distance between holes in alternate rows originaly 0.480000

xstart = 0+(2.750000E+00-(-2.107996E+00)); %x position of top left hole 
zstart = 0+(3.750000E+00-2.920925E+00)%0.64+zoffset*0.75; %z position of top left hole

xstart2 = (xstart-(xoffset/2));
zstart2 = (zstart+(zoffset/2));

fid = fopen('out_tri_PhC.geo','wt')
%fprintf(fid,dummy);

'Saving data...'

     fprintf(fid,'BLOCK\n{\n');
     fprintf(fid,'%f\n',0.000000E+00);
     fprintf(fid,'%f\n',1.276814E+00);
     fprintf(fid,'%f\n',0.000000E+00);
     fprintf(fid,'%f\n',5.500000E+00);
     fprintf(fid,'%f\n',1.503186E+00);    
     fprintf(fid,'%f\n',7.500000E+00);
     fprintf(fid,'%f\n',5.760000E+00);       %n2=2.4
     fprintf(fid,'%f\n',0.000000E+00);
     fprintf(fid,'}\n');

for i=0:10 %x
   for j=0:24 %z
      fprintf(fid,'CYLINDER\n{\n');
      fprintf(fid,'%f\n',(xstart-xoffset*i));
      fprintf(fid,'%f\n',1.390000E+00);
      fprintf(fid,'%f\n',(zstart+zoffset*j));
      fprintf(fid,'%f\n',0.000000);
      fprintf(fid,'%f\n',0.0705890276);              %radius
      fprintf(fid,'%f\n',2.263717092E-01);       %h = 0.93a= 226.3717092 nm
      fprintf(fid,'%f\n',1.000000);
      fprintf(fid,'%f\n',0.000000);
      fprintf(fid,'}\n');
  end
end

for i=0:9
   for j=0:24
      fprintf(fid,'CYLINDER\n{\n');
      fprintf(fid,'%f\n',(xstart2-xoffset*i));
      fprintf(fid,'%f\n',1.390000E+00);
      fprintf(fid,'%f\n',(zstart2+zoffset*j));
      fprintf(fid,'%f\n',0.000000);
      fprintf(fid,'%f\n',0.0705890276);              %radius
      fprintf(fid,'%f\n',2.263717092E-01);       %h = 0.93a= 226.3717092 nm
      fprintf(fid,'%f\n',1.000000);
      fprintf(fid,'%f\n',0.000000);
      fprintf(fid,'}\n');
  end
end

fprintf(fid,'BOX\n{\n');
fprintf(fid,'%f\n',0.000000);
fprintf(fid,'%f\n',0.000000);
fprintf(fid,'%f\n',0.000000);
fprintf(fid,'%f\n',2.750000E+00);
fprintf(fid,'%f\n',2.780000E+00);
fprintf(fid,'%f\n',7.500000E+00);
fprintf(fid,'}\n');


fprintf(fid,'end'); %end the file

'...done'
fclose(fid)



