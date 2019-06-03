function dome_tests(BASENAME, DSTDIR, Nx_frequency_snapshot,Ny_frequency_snapshot,Nz_frequency_snapshot,Nx_time_snapshot,Ny_time_snapshot,Nz_time_snapshot,N_probes)
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %description:
  % creates 4 geometries and one input file
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %arguments
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  disp('Reading input parameters...');

  if exist('BASENAME','var')==0
    disp('BASENAME not given');
      BASENAME = 'minimum';
  end
  
  if exist('DSTDIR','var')==0
    disp('DSTDIR not given');
      DSTDIR = uigetdir(getuserdir());
  end
  if ~(exist(DSTDIR,'dir'))
    error('dir not found');
    return;
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
  copyfile(fullfile(getuserdir(),'MATLAB','entity.lst'),[DSTDIR,filesep,BASENAME]);
  % .in file
  GEOin([DSTDIR,filesep,BASENAME,filesep,BASENAME,'.in'], BASENAME);
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

  % create bottom block
  L = [ 0, 0, 0 ];
  U = [ Xmax/2, Ymax/2, Zmax/2 ];
  GEOblock(out, L, U, 1, 0);

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

  delta_X_vector=[Xmax/2,Xmax/2];
  delta_Y_vector=[Ymax/2,Ymax/2];
  delta_Z_vector=[Zmax/2,Zmax/2];
  GEOmesh(out, delta_X_vector, delta_Y_vector, delta_Z_vector);
    
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

  Px1 = [Xmax/2, 0      , 0     ];
  Px2 = [Xmax/2, Ymax   , Zmax  ];
  Py1 = [0     , Ymax/2 , 0     ];
  Py2 = [Xmax  , Ymax/2 , Zmax  ];
  Pz1 = [0     , 0      , Zmax/2];
  Pz2 = [Xmax  , Ymax   , Zmax/2];
  
  % frequency snapshots
  for i = 1:Nx_frequency_snapshot
    GEOfrequency_snapshot(out, first, repetition, interpolate, real_dft, mod_only, mod_all, 1, Px1, Px2, FREQUENCY, starting_sample, E, H, J);
  end
  for i = 1:Ny_frequency_snapshot
    GEOfrequency_snapshot(out, first, repetition, interpolate, real_dft, mod_only, mod_all, 2, Py1, Py2, FREQUENCY, starting_sample, E, H, J);
  end
  for i = 1:Nz_frequency_snapshot
    GEOfrequency_snapshot(out, first, repetition, interpolate, real_dft, mod_only, mod_all, 3, Pz1, Pz2, FREQUENCY, starting_sample, E, H, J);
  end

  % time snapshots
  for i = 1:Nx_time_snapshot
    GEOtime_snapshot(out, first, repetition, 1, Px1, Px2, E, H, J, power,0);
  end
  for i = 1:Ny_time_snapshot
    GEOtime_snapshot(out, first, repetition, 2, Py1, Py2, E, H, J, power,0);
  end
  for i = 1:Nz_time_snapshot
    GEOtime_snapshot(out, first, repetition, 3, Pz1, Pz2, E, H, J, power,0);
  end
  
  % probes
  step=1;
  E=[1,1,1];
  H=[1,1,1];
  J=[0,0,0];
  power = 0;
  
  % probes
  for i =1:N_probes
    GEOprobe(out, [Xmax/2, Ymax/2, Zmax/2], step, E, H, J, power );
  end
  
  %write footer
  fprintf(out,'end\n'); %end the file

  %close file
  fclose(out);
  disp('...done');

end
