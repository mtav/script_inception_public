function INFILENAME = just_signal(ITERATIONS,excitation_direction)
     
    BASENAME = ['just_signal_',num2str(ITERATIONS),'_',num2str(excitation_direction)];
    DSTDIR = [getuserdir(),filesep,'DATA',filesep,'just_signal_test'];
  mkdir([DSTDIR,filesep,BASENAME]);
    INFILENAME = [DSTDIR,filesep,BASENAME,filesep,BASENAME,'.in'];

  lambda = 637*10^-3;%mum
    FREQUENCY = get_c0()/lambda;
  n_Air = 1;%no unit
  
  TIMESTEP = 0.9;%mus
  TIME_CONSTANT = 4.000000E-09;%mus
  AMPLITUDE = 1.000000E+01;%V/mum???
  TIME_OFFSET = 2.700000E-08;%mus
    
  Xmax = 1;%mum
  Ymax = 1;%mum
  Zmax = 1;%mum
  
  delta_mesh = lambda/(10*n_Air);
  thicknessVector = [ Ymax ];
  max_delta_Vector = [ delta_mesh ];
  
  [ delta_X_vector, local_delta_X_vector ] = subGridMultiLayer(max_delta_Vector,thicknessVector);
  [ delta_Y_vector, local_delta_Y_vector ] = subGridMultiLayer(max_delta_Vector,thicknessVector);
  [ delta_Z_vector, local_delta_Z_vector ] = subGridMultiLayer(max_delta_Vector,thicknessVector);
    
  copyfile(fullfile(getuserdir(),'MATLAB','entity.lst'),[DSTDIR,filesep,BASENAME]);
  GEOin(INFILENAME, { [BASENAME,'.inp'],[BASENAME,'.geo'] });
  GEOshellscript([DSTDIR,filesep,BASENAME,filesep,BASENAME,'.sh'], BASENAME);
  GEOcommand([DSTDIR,filesep,BASENAME,filesep,BASENAME], BASENAME);
    
  out = fopen([DSTDIR,filesep,BASENAME,filesep,BASENAME,'.geo'],'wt');
  fprintf(out,'**GEOMETRY FILE\n');
  fprintf(out,'\n');
  GEObox(out, [ 0, 0, 0 ], [ Xmax, Ymax, Zmax ]);
  fprintf(out,'end\n'); %end the file
  fclose(out);
  
  out = fopen([DSTDIR,filesep,BASENAME,filesep,BASENAME,'.inp'],'wt');
    P_Xm = [ Xmax/2.0-2*delta_mesh, Ymax/2.0, Zmax/2.0 ];
    P_Xp = [ Xmax/2.0+2*delta_mesh, Ymax/2.0, Zmax/2.0 ];
    P_Ym = [ Xmax/2.0, Ymax/2.0-2*delta_mesh, Zmax/2.0 ];
    P_Yp = [ Xmax/2.0, Ymax/2.0+2*delta_mesh, Zmax/2.0 ];
    P_Zm = [ Xmax/2.0, Ymax/2.0, Zmax/2.0-2*delta_mesh ];
    P_Zp = [ Xmax/2.0, Ymax/2.0, Zmax/2.0+2*delta_mesh ];
    P_center = [ Xmax/2.0, Ymax/2.0, Zmax/2.0 ];
    E = [ 1, 0,	0 ];
    H = [ 0, 0,	0 ];
    type = 10;
    
    if excitation_direction == 1
    GEOexcitation(out, 7, P_center, P_Xm, E, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, FREQUENCY, 0, 0, 0, 0);
    elseif  excitation_direction == 2
    GEOexcitation(out, 7, P_center, P_Xp, E, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, FREQUENCY, 0, 0, 0, 0);
    elseif  excitation_direction == 3
    GEOexcitation(out, 7, P_center, P_Ym, E, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, FREQUENCY, 0, 0, 0, 0);
    elseif  excitation_direction == 4
    GEOexcitation(out, 7, P_center, P_Yp, E, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, FREQUENCY, 0, 0, 0, 0);
    elseif  excitation_direction == 5
    GEOexcitation(out, 7, P_center, P_Zm, E, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, FREQUENCY, 0, 0, 0, 0);
    elseif  excitation_direction == 6
    GEOexcitation(out, 7, P_center, P_Zp, E, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, FREQUENCY, 0, 0, 0, 0);
    elseif excitation_direction == 7
    GEOexcitation(out, 7, P_Xm, P_center, E, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, FREQUENCY, 0, 0, 0, 0);
    elseif  excitation_direction == 8
    GEOexcitation(out, 7, P_Xp, P_center, E, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, FREQUENCY, 0, 0, 0, 0);
    elseif  excitation_direction == 9
    GEOexcitation(out, 7, P_Ym, P_center, E, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, FREQUENCY, 0, 0, 0, 0);
    elseif  excitation_direction == 10
    GEOexcitation(out, 7, P_Yp, P_center, E, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, FREQUENCY, 0, 0, 0, 0);
    elseif  excitation_direction == 11
    GEOexcitation(out, 7, P_Zm, P_center, E, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, FREQUENCY, 0, 0, 0, 0);
    elseif  excitation_direction == 12
    GEOexcitation(out, 7, P_Zp, P_center, E, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, FREQUENCY, 0, 0, 0, 0);
    else
        error('invalid direction');
    end
  Xpos_bc = 2; Xpos_param = [1,1,0];
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
  
    step = 10;
    E = [1,1,1];
    H = [1,1,1];
    J = [0,0,0];
    power = 0;
    
    GEOprobe(out, [ Xmax/2.0-4*delta_mesh, Ymax/2.0, Zmax/2.0 ], step, E, H, J, power );
    GEOprobe(out, [ Xmax/2.0+4*delta_mesh, Ymax/2.0, Zmax/2.0 ], step, E, H, J, power );
    GEOprobe(out, [ Xmax/2.0, Ymax/2.0-4*delta_mesh, Zmax/2.0 ], step, E, H, J, power );
    GEOprobe(out, [ Xmax/2.0, Ymax/2.0+4*delta_mesh, Zmax/2.0 ], step, E, H, J, power );
    GEOprobe(out, [ Xmax/2.0, Ymax/2.0, Zmax/2.0-4*delta_mesh ], step, E, H, J, power );
    GEOprobe(out, [ Xmax/2.0, Ymax/2.0, Zmax/2.0+4*delta_mesh ], step, E, H, J, power );
    
  fprintf(out,'end\n'); %end the file
  fclose(out);
end
