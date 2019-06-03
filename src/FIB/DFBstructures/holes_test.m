function filename_cellarray_all = holes_test(fileBaseName,type,mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,customconfig)
% Usage:
%  filename_cellarray = holes_test(fileBaseName,type,mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,customconfig)
%
%  type = loncar,DFBrectSpiral,DFBrectRaster,DFBtriangle
%
% ex:
%  a=holes_test('loncar.str','loncar');readStrFile(a);
%  a=holes_test('DFBrectSpiral.str','DFBrectSpiral');readStrFile(a);
%  a=holes_test('DFBrectRaster.str','DFBrectRaster');readStrFile(a);
%  a=holes_test('DFBtriangle.str','DFBtriangle');readStrFile(a);
%  a=holes_test('loncar','loncar',30000,3*2400,11);readStrFile(a);
%  a=holes_test('DFBrectSpiral','DFBrectSpiral',30000,3*2400,11);readStrFile(a);
%  a=holes_test('DFBrectRaster','DFBrectRaster',30000,3*2400,11);readStrFile(a);
%  a=holes_test('DFBtriangle','DFBtriangle',30000,3*2400,11);readStrFile(a);

  switch type
    case 'loncar'
      % loncar
      holeType_left = 0;
      holeType_center = 0;
      holeType_right = 0;
      left = 0;
      center = 1;
      right = 0;
    case 'DFBrectSpiral'
      % DFB rect spiral
      holeType_left = 1;
      holeType_center = 0;
      holeType_right = 1;
      left = 1;
      center = 0;
      right = 1;
    case 'DFBrectRaster'
      % DFB rect raster
      holeType_left = 2;
      holeType_center = 0;
      holeType_right = 2;
      left = 1;
      center = 0;
      right = 1;
    case 'DFBtriangle'
      % DFB triangles
      holeType_left = 6;
      holeType_center = 0;
      holeType_right = 5;
      left = 1;
      center = 0;
      right = 1;
    otherwise
      if exist('customconfig','var')==0
        error('Unexpected type. No streamfile created.');
      else
        holeType_left = customconfig(1);
        holeType_center = customconfig(2);
        holeType_right = customconfig(3);
        left = customconfig(4);
        center = customconfig(5);
        right = customconfig(6);
      end
  end
  
  if exist('mag','var')==0;mag = 34000;end;
  if exist('dwell','var')==0;dwell = 3*2400;end; %unit: 0.1us
  if exist('radius_mum','var')==0;radius_mum = 1;end; %0.500;%0.450+0.065;
  if exist('Ntop','var')==0; Ntop = 10;end; %8;
  if exist('Nbottom','var')==0; Nbottom = 20;end; %18;%40;
  if exist('size_x_mum','var')==0; size_x_mum = 2*0.066; end;
  if exist('size_y_mum','var')==0; size_y_mum = 0.200; end;
  if exist('rep','var')==0; rep = 2; end;
  
  delta_x_mum = size_x_mum + 2*0.078;
  cavity_x_mum = 2*0.145;
  
  % show Ntop/Nbottom suggestions to fit specified height_mum (use them directly instead of Ntop/Nbottom?)
  height_mum = 9
  N_suggested = (height_mum - cavity_x_mum )/delta_x_mum
  Ntop_suggested = 1/3*(height_mum - cavity_x_mum )/delta_x_mum
  Nbottom_suggested = 2/3*(height_mum - cavity_x_mum )/delta_x_mum
  
  height_mum = Nbottom*delta_x_mum + cavity_x_mum + Ntop*delta_x_mum;
  disp(['height_mum = ',num2str(height_mum)]);
  
  [res, HFW] = getResolution(mag);
  disp(['Resolution = ',num2str(res),' mum/pxl'])
  
  if height_mum>HFW
    height_mum
    HFW
    error('pillar too big for this magnification');
  end
  
  x_current = -0.5*height_mum;
  holes_X_bottom = [];
  holes_Y_bottom = [];
  holes_Type_bottom = [];
  
  holes_Y_position_factor = 1
  for i = 1:Nbottom
    if left
      holes_X_bottom = [ holes_X_bottom, x_current ];
      holes_Y_bottom = [ holes_Y_bottom, holes_Y_position_factor*radius_mum ];
      holes_Type_bottom = [ holes_Type_bottom, holeType_left ];
    end
    if center
      holes_X_bottom = [ holes_X_bottom, x_current ];
      holes_Y_bottom = [ holes_Y_bottom, 0 ];
      holes_Type_bottom = [ holes_Type_bottom, holeType_center ];
    end
    if right
      holes_X_bottom = [ holes_X_bottom, x_current ];
      holes_Y_bottom = [ holes_Y_bottom, -holes_Y_position_factor*radius_mum ];
      holes_Type_bottom = [ holes_Type_bottom, holeType_right ];
    end
    x_current = x_current + delta_x_mum;
  end
  
  x_current = x_current + cavity_x_mum + size_x_mum;

  holes_X_top = [];
  holes_Y_top = [];
  holes_Type_top = [];
  for i = 1:Ntop
    if left
      holes_X_top = [ holes_X_top, x_current ];
      holes_Y_top = [ holes_Y_top, holes_Y_position_factor*radius_mum ];
      holes_Type_top = [ holes_Type_top, holeType_left ];
    end
    if center
      holes_X_top = [ holes_X_top, x_current ];
      holes_Y_top = [ holes_Y_top, 0 ];
      holes_Type_top = [ holes_Type_top, holeType_center ];
    end
    if right
      holes_X_top = [ holes_X_top, x_current ];
      holes_Y_top = [ holes_Y_top, -holes_Y_position_factor*radius_mum ];
      holes_Type_top = [ holes_Type_top, holeType_right ];
    end
    x_current = x_current + delta_x_mum;
  end
  
  holes_Size_X_bottom = size_x_mum*ones(1,length(holes_X_bottom));
  holes_Size_Y_bottom = size_y_mum*ones(1,length(holes_Y_bottom));
  holes_Size_X_top = size_x_mum*ones(1,length(holes_X_top));
  holes_Size_Y_top = size_y_mum*ones(1,length(holes_Y_top));
  
  holes_X_all = [ holes_X_bottom, holes_X_top ];
  holes_Y_all = [ holes_Y_bottom, holes_Y_top ];
  holes_Size_X_all = [ holes_Size_X_bottom, holes_Size_X_top ];
  holes_Size_Y_all = [ holes_Size_Y_bottom, holes_Size_Y_top ];
  holes_Type_all = [ holes_Type_bottom, holes_Type_top ];
  
  separate_files = 0;

  fileBaseName3 = [dirname(fileBaseName), filesep, basename(fileBaseName,'.str')];
  infoString = ['.mag_',num2str(mag),'.dwell_',num2str(dwell),'.beamCurrent_',num2str(beamCurrent),'.radius_',num2str(radius_mum),'.Nbottom_',num2str(Nbottom),'.Ntop_',num2str(Ntop),'.rep_',num2str(rep),'.hry_',num2str(size_y_mum)];
  
  %disp('JOJO')
  %disp(holes_Size_Y_bottom(1:10))
  %disp(holes_Type_bottom)
  
  filename_cellarray_bottom1 = holes([fileBaseName3,'.bottom1',infoString],mag,dwell,rep,holes_X_bottom(1:10),holes_Y_bottom(1:10),holes_Size_X_bottom(1:10),holes_Size_Y_bottom(1:10),holes_Type_bottom(1:10),separate_files);
  filename_cellarray_bottom2 = holes([fileBaseName3,'.bottom2',infoString],mag,dwell,rep,holes_X_bottom(10:20),holes_Y_bottom(10:20),holes_Size_X_bottom(10:20),holes_Size_Y_bottom(10:20),holes_Type_bottom(10:20),separate_files);
  
  filename_cellarray_top = holes([fileBaseName3,'.top',infoString],mag,dwell,rep,holes_X_top,holes_Y_top,holes_Size_X_top,holes_Size_Y_top,holes_Type_top,separate_files);
  %filename_cellarray_all = holes([fileBaseName3,'.all',infoString],mag,dwell,rep,holes_X_all,holes_Y_all,holes_Size_X_all,holes_Size_Y_all,holes_Type_all,separate_files);
  filename_cellarray_all = {filename_cellarray_bottom1{:}, filename_cellarray_bottom2{:}, filename_cellarray_top{:}}
end
