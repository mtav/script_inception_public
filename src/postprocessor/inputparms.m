function Inp = inputparms(inpfile)
  %% Read in input file
  tab = readtextfile(inpfile);
  dim = size(tab);
  ii=1;
  FrSnaps = 0; Snaps = 0; Mesh = 0; Inp.SnapsTot = 0; Inp.FrSnapsTot = 0;
  
  %% Create structures for excitations, snapshots and boundaries
  while ii <= dim(1)
      if strcmp(tab(ii,1:34),'EXCITATION **EXCITATION DEFINITION')
          ii=ii+3;
          Inp.Excitation.PosXl = str2double(tab(ii,1:13));ii=ii+1;
          Inp.Excitation.PosYl = str2double(tab(ii,1:13));ii=ii+1;
          Inp.Excitation.PosZl = str2double(tab(ii,1:13));ii=ii+1;
          Inp.Excitation.PosXu = str2double(tab(ii,1:13));ii=ii+1;
          Inp.Excitation.PosYu = str2double(tab(ii,1:13));ii=ii+1;
          Inp.Excitation.PosZu = str2double(tab(ii,1:13));
      end
      if strcmp(tab(ii,1:40),'FREQUENCY_SNAPSHOT **SNAPSHOT DEFINITION')
          FrSnaps = FrSnaps+1;
          ii=ii+8;
          Inp.FreqSnap(FrSnaps).Plane = str2double(tab(ii));ii=ii+1;
              if Inp.FreqSnap(FrSnaps).Plane == 0
                  Inp.FrSnapsTot = Inp.FrSnapsTot+6;
              else
                  Inp.FrSnapsTot = Inp.FrSnapsTot+1;
              end
          Inp.FreqSnap(FrSnaps).BoundXl = str2double(tab(ii,1:13));ii=ii+1;
          Inp.FreqSnap(FrSnaps).BoundYl = str2double(tab(ii,1:13));ii=ii+1;
          Inp.FreqSnap(FrSnaps).BoundZl = str2double(tab(ii,1:13));ii=ii+1;
          Inp.FreqSnap(FrSnaps).BoundXu = str2double(tab(ii,1:13));ii=ii+1;
          Inp.FreqSnap(FrSnaps).BoundYu = str2double(tab(ii,1:13));ii=ii+1;
          Inp.FreqSnap(FrSnaps).BoundZu = str2double(tab(ii,1:13));
      end
      if strcmp(tab(ii,1:30),'SNAPSHOT **SNAPSHOT DEFINITION')
          Snaps = Snaps+1;
          ii=ii+4;
          Inp.Snap(Snaps).Plane = str2double(tab(ii));
              if Inp.Snap(Snaps).Plane == 0
                  Inp.SnapsTot = Inp.SnapsTot+6;
              else
                  Inp.SnapsTot = Inp.SnapsTot+1;
              end
          Inp.Snap(Snaps).BoundXl = str2double(tab(ii,1:13));ii=ii+1;
          Inp.Snap(Snaps).BoundYl = str2double(tab(ii,1:13));ii=ii+1;
          Inp.Snap(Snaps).BoundZl = str2double(tab(ii,1:13));ii=ii+1;
          Inp.Snap(Snaps).BoundXu = str2double(tab(ii,1:13));ii=ii+1;
          Inp.Snap(Snaps).BoundYu = str2double(tab(ii,1:13));ii=ii+1;
          Inp.Snap(Snaps).BoundZu = str2double(tab(ii,1:13));
      end
      if strcmp(tab(ii,1:8),'BOUNDARY')
          ii=ii+2;
          Inp.Boundary.Xl = str2double(tab(ii,1:2));ii=ii+1;
          Inp.Boundary.Yl = str2double(tab(ii,1:2));ii=ii+1;
          Inp.Boundary.Zl = str2double(tab(ii,1:2));ii=ii+1;
          Inp.Boundary.Xu = str2double(tab(ii,1:2));ii=ii+1;
          Inp.Boundary.Yu = str2double(tab(ii,1:2));ii=ii+1;
          Inp.Boundary.Zu = str2double(tab(ii,1:2));
      end
      if strcmp(tab(ii,1:5),'nodes')
          ii=ii+2;
          Inp.Mesh.X = str2double(tab(ii,1:2));ii=ii+1;
          Inp.Mesh.Y = str2double(tab(ii,1:2));ii=ii+1;
          Inp.Mesh.Z = str2double(tab(ii,1:2));
      end
      if strcmp(tab(ii,1:24), 'XMESH **XMESH DEFINITION')
          ii=ii+2;
          while tab(ii,1) ~= '}'
              Mesh = Mesh+1;
              ii=ii+1;
          end
          Inp.Mesh.X = Mesh;
          Mesh = 0;
      end
      if strcmp(tab(ii,1:24), 'YMESH **YMESH DEFINITION')
          ii=ii+2;
          while tab(ii,1) ~= '}'
              Mesh = Mesh+1;
              ii=ii+1;
          end
          Inp.Mesh.Y = Mesh;
          Mesh = 0;
      end
      if strcmp(tab(ii,1:24), 'ZMESH **ZMESH DEFINITION')
          ii=ii+2;
          while tab(ii,1) ~= '}'
              Mesh = Mesh+1;
              ii=ii+1;
          end
          Inp.Mesh.Z = Mesh;
          Mesh = 0;
      end
      ii=ii+1;
  end
end
