function [INFILENAME,AMPLITUDE,TIME_OFFSET,TIME_CONSTANT,FREQUENCY] = just_signal_2(DSTDIR,BASENAME)
    
    excitation_direction = 7;
    
  % lambda = 637*10^-3;%mum
  lambda = 1;%mum
  n_Air = 1;%no unit
  
  % TIMESTEP = 0.9;%mus
    
    % excitation parameters
  % TIME_CONSTANT = 1;%mus
  % AMPLITUDE = 2;%V/mum???
  % TIME_OFFSET = 3;%mus
    % FREQUENCY = get_c0()/lambda;

  % TIME_CONSTANT = 4*10^(-9);%mus
  % AMPLITUDE = 10;%V/mum???
  % TIME_OFFSET = 2.700000E-08;%mus
    % FREQUENCY = get_c0()/lambda;

    % A=10;tau=0;f=get_c0()/(637*10^-3);w=sqrt(log(2))*((10./2.)/f)/2.;
    % delta=20*1/f;t=[tau-delta/2:delta/100:tau+delta/2];plot(t,A*exp(-log(2)*((t-tau)/w).^2).*sin(2*pi*f*t));
    
  AMPLITUDE = 1000;%V/mum???
    FREQUENCY = get_c0()/lambda;
  TIME_CONSTANT = sqrt(log(2))*((10./2.)/FREQUENCY)/2.;%mus
  TIME_OFFSET = 2*TIME_CONSTANT/sqrt(log(2));%mus
    
    delta=20*1/FREQUENCY;t=[TIME_OFFSET-delta/2:delta/100:TIME_OFFSET+delta/2];
    plot(t,AMPLITUDE*exp(-log(2)*((t-TIME_OFFSET)/TIME_CONSTANT).^2).*sin(2*pi*FREQUENCY*t));
    
    STEP=10;
  % TIMESTEP = 1./(4.*STEP*FREQUENCY);%mus
    % ITERATIONS = (40.*1./FREQUENCY)/TIMESTEP;
  TIMESTEP = 0.5;%mus
    ITERATIONS = 2000;
        
    % BASENAME = ['just_signal_',num2str(ITERATIONS),'_',num2str(excitation_direction)];
  mkdir([DSTDIR,filesep,BASENAME]);
    INFILENAME = [DSTDIR,filesep,BASENAME,filesep,BASENAME,'.in'];

  Xmax = 10*lambda;%mum
  Ymax = (4.*10.+1)*lambda;%mum
  Zmax = 10*lambda;%mum
  
  delta_mesh = lambda/(4*n_Air);
  max_delta_Vector = [ delta_mesh ];
  
    disp(['ITERATIONS=',num2str(ITERATIONS)]);
    disp(['TIMESTEP=',num2str(TIMESTEP)]);
    disp(['STEP=',num2str(STEP)]);
    disp(['STEP=',num2str(STEP)]);
    disp(['AMPLITUDE=',num2str(AMPLITUDE)]);
    disp(['FREQUENCY=',num2str(FREQUENCY)]);
    disp(['TIME_CONSTANT=',num2str(TIME_CONSTANT)]);
    disp(['TIME_OFFSET=',num2str(TIME_OFFSET)]);
    disp(['ITERATIONS*TIMESTEP=',num2str(ITERATIONS*TIMESTEP)]);
    disp(['delta_mesh=',num2str(delta_mesh)]);
    disp(['40.*1./FREQUENCY=',num2str(40.*1./FREQUENCY)]);
    
  [ delta_X_vector, local_delta_X_vector ] = subGridMultiLayer(max_delta_Vector,[Xmax]);
  [ delta_Y_vector, local_delta_Y_vector ] = subGridMultiLayer(max_delta_Vector,[Ymax]);
  [ delta_Z_vector, local_delta_Z_vector ] = subGridMultiLayer(max_delta_Vector,[Zmax]);
    
  copyfile(fullfile(getuserdir(),'MATLAB','entity.lst'),[DSTDIR,filesep,BASENAME]);
  GEOin(INFILENAME, { [BASENAME,'.inp'],[BASENAME,'.geo'] });
    GEOshellscript([DSTDIR,filesep,BASENAME,filesep,BASENAME'.sh'], BASENAME, '$HOME/bin/fdtd', '$JOBDIR', 3);
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
    
    if excitation_direction == 1 % EMPTY
    GEOexcitation(out, 7, P_center, P_Xm, E, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, FREQUENCY, 0, 0, 0, 0);
    elseif  excitation_direction == 2 % FAIL
    GEOexcitation(out, 7, P_center, P_Xp, E, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, FREQUENCY, 0, 0, 0, 0);
    elseif  excitation_direction == 3 % EMPTY
    GEOexcitation(out, 7, P_center, P_Ym, E, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, FREQUENCY, 0, 0, 0, 0);
    elseif  excitation_direction == 4 % EMPTY
    GEOexcitation(out, 7, P_center, P_Yp, E, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, FREQUENCY, 0, 0, 0, 0);
    elseif  excitation_direction == 5 % EMPTY
    GEOexcitation(out, 7, P_center, P_Zm, E, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, FREQUENCY, 0, 0, 0, 0);
    elseif  excitation_direction == 6 % EMPTY
    GEOexcitation(out, 7, P_center, P_Zp, E, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, FREQUENCY, 0, 0, 0, 0);
    elseif excitation_direction == 7 % WORKS
    % GEOexcitation(out, 7, P_Xm, P_center, E, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, FREQUENCY, 0, 0, 0, 0);
    GEOexcitation(out, 7, [Xmax/2.0,delta_mesh,Zmax/2.0], [Xmax/2.0+2*delta_mesh,delta_mesh,Zmax/2.0], E, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, FREQUENCY, 0, 0, 0, 0);
    elseif  excitation_direction == 8 % FAIL
    GEOexcitation(out, 7, P_Xp, P_center, E, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, FREQUENCY, 0, 0, 0, 0);
    elseif  excitation_direction == 9 % EMPTY
    GEOexcitation(out, 7, P_Ym, P_center, E, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, FREQUENCY, 0, 0, 0, 0);
    elseif  excitation_direction == 10 % EMPTY
    GEOexcitation(out, 7, P_Yp, P_center, E, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, FREQUENCY, 0, 0, 0, 0);
    elseif  excitation_direction == 11 % EMPTY
    GEOexcitation(out, 7, P_Zm, P_center, E, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, FREQUENCY, 0, 0, 0, 0);
    elseif  excitation_direction == 12 % EMPTY
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
  
    step = STEP;
    E = [1,1,1];
    H = [1,1,1];
    J = [0,0,0];
    power = 0;
    
    % GEOprobe(out, [ Xmax/2.0-4*delta_mesh, Ymax/2.0, Zmax/2.0 ], step, E, H, J, power );
    % GEOprobe(out, [ Xmax/2.0+4*delta_mesh, Ymax/2.0, Zmax/2.0 ], step, E, H, J, power );
    % GEOprobe(out, [ Xmax/2.0, Ymax/2.0-4*delta_mesh, Zmax/2.0 ], step, E, H, J, power );
    % GEOprobe(out, [ Xmax/2.0, Ymax/2.0+4*delta_mesh, Zmax/2.0 ], step, E, H, J, power );
    % GEOprobe(out, [ Xmax/2.0, Ymax/2.0, Zmax/2.0-4*delta_mesh ], step, E, H, J, power );
    % GEOprobe(out, [ Xmax/2.0, Ymax/2.0, Zmax/2.0+4*delta_mesh ], step, E, H, J, power );

    GEOprobe(out, [ Xmax/2.0, delta_mesh+delta_mesh, Zmax/2.0 ], step, E, H, J, power );
    GEOprobe(out, [ Xmax/2.0, delta_mesh+1*10*4*n_Air*delta_mesh, Zmax/2.0 ], step, E, H, J, power );
    GEOprobe(out, [ Xmax/2.0, delta_mesh+2*10*4*n_Air*delta_mesh, Zmax/2.0 ], step, E, H, J, power );
    GEOprobe(out, [ Xmax/2.0, delta_mesh+3*10*4*n_Air*delta_mesh, Zmax/2.0 ], step, E, H, J, power );
    GEOprobe(out, [ Xmax/2.0, delta_mesh+4*10*4*n_Air*delta_mesh, Zmax/2.0 ], step, E, H, J, power );
    
  fprintf(out,'end\n'); %end the file
  fclose(out);
end
