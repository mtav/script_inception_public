function Geo = geometryparms(geofile)
  %% Read in Geometry files
  %geofile
  tab = readtextfile(geofile);
  dim = size(tab);
  ii=1;
  Blocks = 0; Cyls = 0; Spheres = 0;
  
  %% Create structures for objects defined within geometry file
  while ii <= dim(1)
      if strcmp(tab(ii,1:5),'BLOCK')
          Blocks = Blocks+1; ii=ii+2;
          Geo.Block(Blocks).Xl = str2double(tab(ii,1:13));ii=ii+1;
          Geo.Block(Blocks).Yl = str2double(tab(ii,1:13));ii=ii+1;
          Geo.Block(Blocks).Zl = str2double(tab(ii,1:13));ii=ii+1;
          Geo.Block(Blocks).Xu = str2double(tab(ii,1:13));ii=ii+1;
          Geo.Block(Blocks).Yu = str2double(tab(ii,1:13));ii=ii+1;
          Geo.Block(Blocks).Zu = str2double(tab(ii,1:13));
      end
      if strcmp(tab(ii,1:8),'CYLINDER')
          Cyls = Cyls+1; ii=ii+2;
          Geo.Cylinder(Cyls).X = str2double(tab(ii,1:13));ii=ii+1;
          Geo.Cylinder(Cyls).Y = str2double(tab(ii,1:13));ii=ii+1;
          Geo.Cylinder(Cyls).Z = str2double(tab(ii,1:13));ii=ii+1;
          Geo.Cylinder(Cyls).Rad1 = str2double(tab(ii,1:13));ii=ii+1;
          Geo.Cylinder(Cyls).Rad2 = str2double(tab(ii,1:13));ii=ii+1;
          Geo.Cylinder(Cyls).H = str2double(tab(ii,1:13));
      end
      if strcmp(tab(ii,1:3),'BOX')
          ii=ii+2;
          Geo.Box.Xl = str2double(tab(ii,1:13));
          ii=ii+1;
          Geo.Box.Yl = str2double(tab(ii,1:13));
          ii=ii+1;
          Geo.Box.Zl = str2double(tab(ii,1:13));
          ii=ii+1;
          Geo.Box.Xu = str2double(tab(ii,1:13));
          ii=ii+1;
          Geo.Box.Yu = str2double(tab(ii,1:13));
          ii=ii+1;
          Geo.Box.Zu = str2double(tab(ii,1:13));
          
          %Geo.Box.Xl
          %Geo.Box.Yl
          %Geo.Box.Zl
          %Geo.Box.Xu
          %Geo.Box.Yu
          %Geo.Box.Zu
          
      end
      if strcmp(tab(ii,1:6),'SPHERE')
          Spheres = Spheres+1; ii=ii+2;
          Geo.Sphere(Spheres).X = str2double(tab(ii,1:13));ii=ii+1;
          Geo.Sphere(Spheres).Y = str2double(tab(ii,1:13));ii=ii+1;
          Geo.Sphere(Spheres).Z = str2double(tab(ii,1:13));ii=ii+1;
          Geo.Sphere(Spheres).Rad1 = str2double(tab(ii,1:13));ii=ii+1;
          Geo.Sphere(Spheres).Rad2 = str2double(tab(ii,1:13));
      end
      ii=ii+1;
  end
  Geo.Blks = Blocks;
  Geo.Cyls = Cyls;
end
