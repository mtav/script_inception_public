function rotated_cylinder(DSTDIR, BASENAME, angle_degrees)
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %description:
  % creates a rotated cylinder and makes EPS snapshots of it.
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %arguments
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  disp('Reading input parameters...');

  if exist('DSTDIR','var')==0
    disp('DSTDIR not given');
      DSTDIR = uigetdir(getuserdir());
  end
  if ~(exist(DSTDIR,'dir'))
    error('dir not found');
    return;
  end
  
  if exist('BASENAME','var')==0
    disp('BASENAME not given');
      BASENAME = 'rotated_cylinder';
  end

  if exist('angle_degrees','var')==0
    disp('angle_degrees not given');
    angle_degrees = 45;
  end

  mkdir([DSTDIR,filesep,BASENAME]);
    
  Xmax=1;
  Ymax=1;
  Zmax=1;
  
  ITERATIONS = 1;%no unit
  TIMESTEP=0.9;%mus
  TIME_CONSTANT=4.000000E-09;%mus
  AMPLITUDE=1.000000E+01;%V/mum???
  TIME_OFFSET=2.700000E-08;%mus
  FREQUENCY=1;%MHz

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
%  	copyfile(fullfile(getuserdir(),'MATLAB','entity.lst'),[DSTDIR,filesep,BASENAME]);
  % .in file
  GEOin([DSTDIR,filesep,BASENAME,filesep,BASENAME,'.in'], { [BASENAME,'.inp'],[BASENAME,'.geo'] });
  % .sh file
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

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  radius = 1/4;
  cylinder_height = 3/4;
  L = [ 0, 0, 0 ];
  U = [ Xmax, (1-cylinder_height)*Ymax, Zmax ];
  block_center = (L+U)/2;
  cylinder_center = [Xmax/2,(radius+(cylinder_height)/2)*Ymax,Zmax/2];

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  axis_point = [0,0,0];
  % create bottom block
  GEOblock(out, L, U, 2, 0);
  GEOrotation(out, axis_point, [0,0,-1], 0);

  % create cylinder
  GEOcylinder(out, cylinder_center, 0, radius, cylinder_height, 3, 0, 0);	
  GEOrotation(out, axis_point, [0,0,-1], 0);

  % create sphere
  GEOsphere(out, cylinder_center, radius, 0, 3, 0);
  GEOrotation(out, axis_point, [0,0,-1], 0);

  % create sphere
  GEOsphere(out, cylinder_center, (cylinder_height)/2, 0, 3, 0);
  GEOrotation(out, axis_point, [0,0,-1], 0);
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  axis_point = cylinder_center;
  % create bottom block
  GEOblock(out, L, U, 2, 0);
  GEOrotation(out, axis_point, [0,0,-1], angle_degrees);

  % create cylinder
  GEOcylinder(out, cylinder_center, 0, radius, cylinder_height, 3, 0, angle_degrees);	
  GEOrotation(out, axis_point, [0,0,-1], angle_degrees);

  % create sphere
  GEOsphere(out, cylinder_center, radius, 0, 3, 0);
  GEOrotation(out, axis_point, [0,0,-1], angle_degrees);

  % create sphere
  GEOsphere(out, cylinder_center, (cylinder_height)/2, 0, 3, 0);
  GEOrotation(out, axis_point, [0,0,-1], angle_degrees);
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  axis_point = block_center;
  % create bottom block
  GEOblock(out, L, U, 2, 0);
  GEOrotation(out, axis_point, [0,0,-1], -angle_degrees);

  % create cylinder
  GEOcylinder(out, cylinder_center, 0, radius, cylinder_height, 3, 0, -angle_degrees);	
  GEOrotation(out, axis_point, [0,0,-1], -angle_degrees);

  % create sphere
  GEOsphere(out, cylinder_center, radius, 0, 3, 0);
  GEOrotation(out, axis_point, [0,0,-1], -angle_degrees);

  % create sphere
  GEOsphere(out, cylinder_center, (cylinder_height)/2, 0, 3, 0);
  GEOrotation(out, axis_point, [0,0,-1], -angle_degrees);
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  %write box
  L = [ 0, 0, 0 ];
  U = [ Xmax, Ymax, Zmax ];
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

  P1 = [ 2*Xmax/4, Ymax/2, Zmax/2 ];
  P2 = [ 3*Xmax/4, Ymax/2, Zmax/2 ];
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
  id_character = '_id_';
  GEOflag(out, iteration_method, propagation_constant, flag_1, flag_2, ITERATIONS, TIMESTEP, id_character);

  delta_X_vector = subGridMultiLayer(Xmax/50,[Xmax]);
  delta_Y_vector = subGridMultiLayer(Ymax/50,[Ymax]);
  delta_Z_vector = subGridMultiLayer(Zmax/50,[Zmax]);
  GEOmesh(out, delta_X_vector, delta_Y_vector, delta_Z_vector);
  
  % frequency snapshots
  first = ITERATIONS;
  repetition = ITERATIONS;
  interpolate = 1;
  real_dft = 0;
  mod_only = 0;
  mod_all = 1;
  starting_sample = 0;
  E=[0,0,0];
  H=[0,0,0];
  J=[0,0,0];
  power = 0;

  Px1 = [Xmax/2, 0      , 0     ];
  Px2 = [Xmax/2, Ymax   , Zmax  ];
  Py1 = [0     , Ymax/2 , 0     ];
  Py2 = [Xmax  , Ymax/2 , Zmax  ];
  Pz1 = [0     , 0      , Zmax/2];
  Pz2 = [Xmax  , Ymax   , Zmax/2];
  
  % frequency snapshots
  % for i = 1:Nx_frequency_snapshot
    % GEOfrequency_snapshot(out, first, repetition, interpolate, real_dft, mod_only, mod_all, 1, Px1, Px2, FREQUENCY, starting_sample, E, H, J);
  % end
  % for i = 1:Ny_frequency_snapshot
    % GEOfrequency_snapshot(out, first, repetition, interpolate, real_dft, mod_only, mod_all, 2, Py1, Py2, FREQUENCY, starting_sample, E, H, J);
  % end
  % for i = 1:Nz_frequency_snapshot
    % GEOfrequency_snapshot(out, first, repetition, interpolate, real_dft, mod_only, mod_all, 3, Pz1, Pz2, FREQUENCY, starting_sample, E, H, J);
  % end

  % time snapshots
  GEOtime_snapshot(out, first, repetition, 1, Px1, Px2, E, H, J, power,1);
  GEOtime_snapshot(out, first, repetition, 2, Py1, Py2, E, H, J, power,1);
  GEOtime_snapshot(out, first, repetition, 3, Pz1, Pz2, E, H, J, power,1);
  
  % probes
  step=1;
  E=[1,1,1];
  H=[1,1,1];
  J=[0,0,0];
  power = 0;
  
  % probes
  % for i =1:N_probes
    % GEOprobe(out, [Xmax/2, Ymax/2, Zmax/2], step, E, H, J, power );
  % end
  
  %write footer
  fprintf(out,'end\n'); %end the file

  %close file
  fclose(out);
  disp('...done');

end
