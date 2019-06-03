function yagi_dome(BASENAME, DSTDIR, angle, pillar_radius, FREQUENCY)
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %description:
  % function yagi_dome(BASENAME, DSTDIR, angle, pillar_radius, FREQUENCY)
  % dome with pillar inside and air tubes penetrating from the side at an angle
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %arguments
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  disp('Reading input parameters...');

  if exist('BASENAME','var')==0
    disp('BASENAME not given');
      BASENAME = 'yagi_dome';
  end
  
  if exist('DSTDIR','var')==0
    error('DSTDIR not given');
%  	    DSTDIR = uigetdir('H:\DATA','DSTDIR');
  end
  if ~(exist(DSTDIR,'dir'))
    error([DSTDIR,' not found']);
  end
  mkdir([DSTDIR,filesep,BASENAME]);

  %wavelength
  lambda = 637*10^-3;%mum
  
  if exist('FREQUENCY','var')==0
    disp('FREQUENCY not given');
    FREQUENCY = get_c0()/lambda;
  end

  % pillar radius
  if exist('pillar_radius','var')==0
    disp('pillar_radius not given');
    pillar_radius = 0.5;%mum
  end
  
  if exist('angle','var')==0
    disp('angle not given');
    angle = -45;
  end
  
  HOLE_TYPE = 1; % 1,2,3 = circle, square, rectangle
  
  % refractive indices
  n_Diamond = 2.4;%no unit
  n_Air = 1;%no unit
  n_bottom_square = 2.4;%no unit
  % distance between holes
  d_holes = lambda/(4*n_Diamond)+lambda/(4*n_Air);%mum
  % hole radius
  hole_radius_y = (lambda/(4*n_Air))/2;%mum
  hole_radius_z = pillar_radius - (d_holes-2*hole_radius_y);%mum
  % number of holes on bottom
  bottom_N = 6; %no unit
  % number of holes on top
  top_N = 3; %no unit
  % distance between 2 holes around cavity
  d_holes_cavity = lambda/n_Diamond + 2*hole_radius_y;%mum
  Lcav = d_holes_cavity - d_holes; % mum
  % d_holes_cavity = Lcav + d_holes;
  % top box offset
  top_box_offset=1;%mum
  
  %bottom square thickness
  h_bottom_square=0.5;%mum
  
  % ITERATIONS = 261600;%no unit
  % ITERATIONS = 32000;%no unit
  ITERATIONS = 1;%no unit
  TIMESTEP = 0.9;%mus
  TIME_CONSTANT = 4.000000E-09;%mus
  AMPLITUDE = 1.000000E+01;%V/mum???
  TIME_OFFSET = 2.700000E-08;%mus
  
  SNAPSHOTS_ON = 0;
  PROBES_ON = 0;
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % additional calculations
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
  % max mesh intervals
  delta_bottom_square = lambda/(10*n_bottom_square);
  delta_hole = lambda/(10*n_Air);
  delta_diamond = lambda/(10*n_Diamond);
  delta_outside = lambda/(4*n_Air);
  delta_center = lambda/(15*n_Diamond);
  delta_boundary = delta_diamond;
  
  % center area where excitation takes place (for meshing)
  center_radius = 4*delta_center;

  % buffers (area outside pillar where mesh is fine)
  x_buffer = 4*delta_diamond;%mum
  y_buffer = 32*delta_diamond;%mum
  z_buffer = 4*delta_diamond;%mum

  pillar_height = (bottom_N+top_N)*d_holes + Lcav;
  dome_radius = pillar_height;

  % dimension and position parameters
  Xmax = 2*(dome_radius + 4*delta_diamond + 4*delta_outside);%mum
  Ymax = h_bottom_square + pillar_height + y_buffer + top_box_offset;%mum
  Zmax = Xmax;%mum
  
  center_sphere = [Xmax/2, h_bottom_square, Zmax/2];

  pillar_centre_X = Xmax/2;
  pillar_centre_Y = h_bottom_square + bottom_N*d_holes + Lcav/2;
  pillar_centre_Z = Zmax/2;

  % meshing parameters
  thicknessVector_Y = [ h_bottom_square ];
  max_delta_Vector_Y = [ delta_bottom_square ];
  for i=1:bottom_N
    thicknessVector_Y = [ thicknessVector_Y, d_holes/2 - hole_radius_y, 2*hole_radius_y, d_holes/2 - hole_radius_y ];
    max_delta_Vector_Y = [ max_delta_Vector_Y, delta_diamond, delta_hole, delta_diamond ];
  end
  thicknessVector_Y = [ thicknessVector_Y, Lcav/2-center_radius, 2*center_radius, Lcav/2-center_radius ];
  max_delta_Vector_Y = [ max_delta_Vector_Y, delta_diamond, delta_center, delta_diamond ];
  for i=1:top_N
    thicknessVector_Y = [ thicknessVector_Y, d_holes/2 - hole_radius_y, 2*hole_radius_y, d_holes/2 - hole_radius_y ];
    max_delta_Vector_Y = [ max_delta_Vector_Y, delta_diamond, delta_hole, delta_diamond ];
  end
  thicknessVector_Y = [ thicknessVector_Y, y_buffer, top_box_offset ];
  max_delta_Vector_Y = [ max_delta_Vector_Y, delta_boundary, delta_outside ];

  delta_min = min(max_delta_Vector_Y);

  thicknessVector_X = [ Xmax/2-pillar_radius-x_buffer, x_buffer, pillar_radius-center_radius, center_radius ];
  max_delta_Vector_X = [ delta_outside, delta_boundary, delta_diamond, delta_center ];

    if HOLE_TYPE == 1
    thicknessVector_Z_1 = [ Zmax/2-pillar_radius-z_buffer, z_buffer, pillar_radius-hole_radius_y, hole_radius_y-center_radius, center_radius ];
  elseif HOLE_TYPE == 2
    thicknessVector_Z_1 = [ Zmax/2-pillar_radius-z_buffer, z_buffer, pillar_radius-hole_radius_y, hole_radius_y-center_radius, center_radius ];
  else
    thicknessVector_Z_1 = [ Zmax/2-pillar_radius-z_buffer, z_buffer, pillar_radius-2*hole_radius_y, 2*hole_radius_y-center_radius, center_radius ];
  end

  thicknessVector_Z_2 = fliplr(thicknessVector_Z_1);
  thicknessVector_Z = [ thicknessVector_Z_1, thicknessVector_Z_2 ];
  max_delta_Vector_Z_1 = [ delta_outside, delta_boundary, delta_diamond, delta_hole, delta_center ];
  max_delta_Vector_Z_2 = fliplr(max_delta_Vector_Z_1);
  max_delta_Vector_Z = [ max_delta_Vector_Z_1, max_delta_Vector_Z_2 ];
  
  [ delta_X_vector, local_delta_X_vector ] = subGridMultiLayer(max_delta_Vector_X,thicknessVector_X);
  [ delta_Y_vector, local_delta_Y_vector ] = subGridMultiLayer(max_delta_Vector_Y,thicknessVector_Y);
  [ delta_Z_vector, local_delta_Z_vector ] = subGridMultiLayer(max_delta_Vector_Z,thicknessVector_Z);

  % regular grid of interval delta_regular
  delta_regular = delta_hole;
  % delta_regular = delta_min;
  delta_X_vector = subGridMultiLayer(delta_regular,[ Xmax/2 ]);
  delta_Y_vector = subGridMultiLayer(delta_regular,[ Ymax ]);
  delta_Z_vector = subGridMultiLayer(delta_regular,[ Zmax ]);
  
  % for the frequency snapshots
  Xplanes = [ 0,
  Xmax/2-pillar_radius-x_buffer,
  Xmax/2-pillar_radius,
  Xmax/2-2*delta_center,
  Xmax/2-delta_center,
  Xmax/2 ];
  
  Yplanes = [ 0,
  h_bottom_square,
  h_bottom_square + bottom_N/2*d_holes,
  pillar_centre_Y-delta_center,
  pillar_centre_Y,
  pillar_centre_Y+delta_center,
  h_bottom_square + bottom_N*d_holes + Lcav + top_N/2*d_holes,
  h_bottom_square + pillar_height,
  h_bottom_square + pillar_height+1*delta_boundary,
  h_bottom_square + pillar_height+8*delta_boundary,
  h_bottom_square + pillar_height+32*delta_boundary,
  Ymax ];
  
  Zplanes = [ 0,
  Zmax/2-pillar_radius-z_buffer,
  Zmax/2-pillar_radius,
  Zmax/2-hole_radius_y,
  Zmax/2-2*delta_center,
  Zmax/2-delta_center,
  Zmax/2,
  Zmax/2+delta_center,
  Zmax/2+2*delta_center,
  Zmax/2+hole_radius_y,
  Zmax/2+pillar_radius,
  Zmax/2+pillar_radius+z_buffer,
  Zmax ];
  
  % for probes
  probes_X_vector = Xplanes(2:4);
  probes_Y_vector = Yplanes(2:11);
  probes_Z_vector = Zplanes(2:8);
  
  probes_Y_vector_center = Yplanes(4:6);
  probes_Z_vector_center = [Zplanes(6),Zplanes(8)];
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % Files to generate:
  % .lst
  % .in
  % .sh
  % .cmd
  % .geo
  % .inp
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % .lst file
  copyfile(fullfile(getuserdir(),'MATLAB','entity.lst'),[DSTDIR,filesep,BASENAME]);
  % .in file
  GEOin([DSTDIR,filesep,BASENAME,filesep,BASENAME,'.in'], { [BASENAME,'.inp'],[BASENAME,'.geo'] });
  % .sh file
  %TODO: improve this
  % WORKDIR = ['$HOME/loncar_structure','/',BASENAME];
  GEOshellscript([DSTDIR,filesep,BASENAME,filesep,BASENAME,'.sh'], BASENAME);
  % .cmd file
  GEOcommand([DSTDIR,filesep,BASENAME,filesep,BASENAME], BASENAME);
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % .geo file
  disp('Writing GEO file...');

  % open file
  out = fopen([DSTDIR,filesep,BASENAME,filesep,BASENAME,'.geo'],'wt');

  % write header
  fprintf(out,'**GEOMETRY FILE\n');
  fprintf(out,'\n');

  % initialize current y
  y_current=0;

  % create bottom block
  L = [ 0, 0, 0 ];
  U = [ Xmax, y_current + h_bottom_square, Zmax ];
  GEOblock(out, L, U, n_Diamond^2, 0);
  y_current = y_current + h_bottom_square;
    
  % create main pillar
  L = [ Xmax/2 - pillar_radius, y_current, Zmax/2 - pillar_radius ];
  U = [ Xmax/2 + pillar_radius, y_current + pillar_height, Zmax/2 + pillar_radius ];
  GEOblock(out, L, U, n_Diamond^2, 0)
  % create dome
  GEOsphere(out, center_sphere, dome_radius, 0, n_Diamond^2, 0)
  
  y_current = y_current + d_holes/2;

  % hole settings
  permittivity = n_Air^2;
  conductivity = 0;
  
  % GEOcylinder(out, center_sphere, 0, dome_radius/4, dome_radius, permittivity, conductivity, angle);

  solid_center_radius = pillar_radius/2;
  hole_length = dome_radius;
  
  % create bottom holes
  for i=1:1 %bottom_N
    A = [ Xmax/2-solid_center_radius-hole_length/2, y_current, Zmax/2 ];
    B = A + [hole_length/2, -hole_radius_y, 0];
    Ap = B(:) + rotation_matrix(0,0,radians(angle))*(A(:)-B(:));
    center = Ap';
    if HOLE_TYPE == 1
    GEOcylinder(out, center, 0, hole_radius_y, hole_length, permittivity, conductivity, angle);
    elseif HOLE_TYPE == 2
    lower = [ Xmax/2 - pillar_radius, y_current - hole_radius_y, Zmax/2 - hole_radius_y];
    upper = [ Xmax/2 + pillar_radius, y_current + hole_radius_y, Zmax/2 + hole_radius_y];
    % GEOblock(out, lower, upper, permittivity, conductivity);
    else
    lower = [ Xmax/2 - pillar_radius, y_current - hole_radius_y, Zmax/2 - hole_radius_z];
    upper = [ Xmax/2 + pillar_radius, y_current + hole_radius_y, Zmax/2 + hole_radius_z];
    % GEOblock(out, lower, upper, permittivity, conductivity);
    end
    y_current = y_current + d_holes;
  end

  y_current = y_current - d_holes + d_holes_cavity;

  % create top holes
  for i=1:top_N
      A = [ Xmax/2-solid_center_radius-hole_length/2, y_current, Zmax/2 ];
    B = A + [hole_length/2, -hole_radius_y, 0];
    Ap = B(:) + rotation_matrix(0,0,radians(angle))*(A(:)-B(:));
    center = Ap';
    if HOLE_TYPE == 1
    GEOcylinder(out, center, 0, hole_radius_y, hole_length, permittivity, conductivity, angle);
    elseif HOLE_TYPE == 2
    lower = [ Xmax/2 - pillar_radius, y_current - hole_radius_y, Zmax/2 - hole_radius_y];
    upper = [ Xmax/2 + pillar_radius, y_current + hole_radius_y, Zmax/2 + hole_radius_y];
    % GEOblock(out, lower, upper, permittivity, conductivity);
    else
    lower = [ Xmax/2 - pillar_radius, y_current - hole_radius_y, Zmax/2 - hole_radius_z];
    upper = [ Xmax/2 + pillar_radius, y_current + hole_radius_y, Zmax/2 + hole_radius_z];
    % GEOblock(out, lower, upper, permittivity, conductivity);
    end
    y_current = y_current + d_holes;
  end

  % side walls
  edge_thickness = Xmax/10;
  h_edge = h_bottom_square;
  
  L1 = [0, h_bottom_square, edge_thickness];
  L2 = [Xmax-edge_thickness, h_bottom_square, 0];
  L3 = [Xmax, h_bottom_square, Zmax-edge_thickness];
  L4 = [edge_thickness, h_bottom_square, Zmax];
  U1 = [Xmax, h_bottom_square + h_edge, 0];
  U2 = [Xmax, h_bottom_square + h_edge, Zmax];
  U3 = [0, h_bottom_square + h_edge, Zmax];
  U4 = [0, h_bottom_square + h_edge, 0];
  
  GEOblock(out, L1, U1, n_Diamond^2, 0);
  GEOblock(out, L2, U2, n_Diamond^2, 0);
  GEOblock(out, L3, U3, n_Diamond^2, 0);
  GEOblock(out, L4, U4, n_Diamond^2, 0);

  %write box
  L = [ 0, 0, 0 ];
  U = [ Xmax/2, Ymax, Zmax ];
  GEObox(out, L, U);

  %write footer
  fprintf(out,'end\n'); %end the file

  %close file
  fclose(out);
  disp('...done');
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % .inp file
  disp('Writing INP file...');

  % open file
  out = fopen([DSTDIR,filesep,BASENAME,filesep,BASENAME,'.inp'],'wt');

  P1 = [ pillar_centre_X-2*delta_center,	pillar_centre_Y, pillar_centre_Z ];
  P2 = [ pillar_centre_X, pillar_centre_Y, pillar_centre_Z ];
  E = [ 1, 0,	0];
  H = [ 0, 0,	0];
  type = 10;
  GEOexcitation(out, 7, P1, P2, E, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, FREQUENCY, 0, 0, 0, 0);
  
  Xpos_bc = 1; Xpos_param = [1,1,0];
  Ypos_bc = 2; Ypos_param = [1,1,0];
  Zpos_bc = 2; Zpos_param = [1,1,0];
  Xneg_bc = 2; Xneg_param = [1,1,0];
  Yneg_bc = 2; Yneg_param = [1,1,0];
  Zneg_bc = 2; Zneg_param = [1,1,0];
  GEOboundary(out, Xpos_bc, Xpos_param, Ypos_bc, Ypos_param, Zpos_bc, Zpos_param, Xneg_bc, Xneg_param, Yneg_bc, Yneg_param, Zneg_bc, Zneg_param);
  
  iteration_method = 5;
  propagation_constant = 0;
  flag_1 = 0;
  flag_2 = 0;
  id_character = 'id';
  GEOflag(out, iteration_method, propagation_constant, flag_1, flag_2, ITERATIONS, TIMESTEP, id_character);

  GEOmesh(out, delta_X_vector, delta_Y_vector, delta_Z_vector);
  
  % EPS snapshots for controlling the geometry
  first = ITERATIONS;
  repetition = ITERATIONS;
  GEOtime_snapshot(out, first, repetition, 1, [Xmax/2,0,0], [Xmax/2,Ymax,Zmax], [0,0,0], [0,0,0], [0,0,0], 0, 1);
  GEOtime_snapshot(out, first, repetition, 2, [0,Ymax/2,0], [Xmax/2,Ymax/2,Zmax], [0,0,0], [0,0,0], [0,0,0], 0, 1);
  GEOtime_snapshot(out, first, repetition, 3, [0,0,Zmax/2], [Xmax/2,Ymax,Zmax/2], [0,0,0], [0,0,0], [0,0,0],0, 1);
  
  % frequency snapshots
  first = ITERATIONS;
  repetition = ITERATIONS;
  interpolate = 1;
  real_dft = 0;
  mod_only = 0;
  mod_all = 1;
  starting_sample = 0;
  E=[1,1,1];
  H=[1,1,1];
  J=[0,0,0];
  power = 0;
  
  if SNAPSHOTS_ON == 1
    for iX = 1:length(Xplanes)
      plane = 1;
      P1 = [Xplanes(iX),0,0];
      P2 = [Xplanes(iX),Ymax,Zmax];
      GEOfrequency_snapshot(out, first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, FREQUENCY, starting_sample, E, H, J);
      GEOtime_snapshot(out, first, repetition, plane, P1, P2, E, H, J, power,0);
    end
    for iY = 1:length(Yplanes)
      plane = 2;
      P1 = [0,Yplanes(iY),0];
      P2 = [Xmax/2,Yplanes(iY),Zmax];
      GEOfrequency_snapshot(out, first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, FREQUENCY, starting_sample, E, H, J);
      GEOtime_snapshot(out, first, repetition, plane, P1, P2, E, H, J, power,0);
    end
    for iZ = 1:length(Zplanes)
      plane = 3;
      P1 = [0,0,Zplanes(iZ)];
      P2 = [Xmax/2,Ymax,Zplanes(iZ)];
      GEOfrequency_snapshot(out, first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, FREQUENCY, starting_sample, E, H, J);
      GEOtime_snapshot(out, first, repetition, plane, P1, P2, E, H, J, power,0);
    end
  end
  
  if PROBES_ON == 1
    % probes
    step=10;
    E=[1,1,1];
    H=[1,1,1];
    J=[0,0,0];
    power = 0;
    for iY =1:length(probes_Y_vector)
      % XY probes
      for iX =1:length(probes_X_vector)
        GEOprobe(out, [probes_X_vector(iX), probes_Y_vector(iY), Zplanes(6)], step, E, H, J, power );
      end
      % ZY probes
      for iZ =1:length(probes_Z_vector)
        GEOprobe(out, [Xplanes(5), probes_Y_vector(iY), probes_Z_vector(iZ)], step, E, H, J, power );
      end
    end
    
    % ZY center probes
    for iY =1:length(probes_Y_vector_center)
      for iZ =1:length(probes_Z_vector_center)
        GEOprobe(out, [Xplanes(4), probes_Y_vector_center(iY), probes_Z_vector_center(iZ)], step, E, H, J, power );
      end
    end
  end
  
  %write footer
  fprintf(out,'end\n'); %end the file

  %close file
  fclose(out);
  disp('...done');
end
