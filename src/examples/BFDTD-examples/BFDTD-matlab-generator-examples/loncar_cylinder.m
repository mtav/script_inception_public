function INFILENAME = loncar_cylinder(BASENAME, DSTDIR, ITERATIONS, print_holes_top, print_holes_bottom, HOLE_TYPE, pillar_radius_mum, EXCITATION_FREQUENCY, SNAPSHOTS_FREQUENCY,excitation_type)
      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      % description:
      %  function loncar_structure(BASENAME, DSTDIR, HOLE_TYPE, pillar_radius_mum, EXCITATION_FREQUENCY, SNAPSHOTS_FREQUENCY)
      %  creates a Loncar type structure (cylinder with transverse circular holes)
      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      % Settings
      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      print_mesh = true;
      print_holes = true;
      % print_holes_top = true;
      % print_holes_bottom = true;
      print_pillar = true;
      print_podium = false;
      print_freqsnap = true;
      print_timesnap = true;
      print_epssnap = true;
      print_excitation = true;
      print_probes = true;
      SNAPSHOTS_ON = 1;

      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      % arguments
      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      disp('Reading input parameters...');

      if exist('BASENAME','var')==0
              disp('BASENAME not given');
          BASENAME = 'loncar_structure';
      end
      
      if exist('DSTDIR','var')==0
              disp('DSTDIR not given');
          DSTDIR = uigetdir(getuserdir(),'DSTDIR');
      end
      if ~(exist(DSTDIR,'dir'))
              error(['dir ',DSTDIR,' not found']);
              return;
      end
      mkdir([DSTDIR,filesep,BASENAME]);

      %wavelength
      lambda = 637*10^-3;%mum

      if exist('print_holes_bottom','var')==0
              error('print_holes_bottom not given');
      end

      if exist('print_holes_top','var')==0
              error('print_holes_top not given');
      end
      
      if exist('EXCITATION_FREQUENCY','var')==0
              disp('EXCITATION_FREQUENCY not given');
              EXCITATION_FREQUENCY = get_c0()/lambda;
      end

      % pillar radius
      if exist('pillar_radius_mum','var')==0
              disp('pillar_radius_mum not given');
              pillar_radius_mum = 0.150/2.0;%mum
      end
      
      if exist('HOLE_TYPE','var')==0
              disp('HOLE_TYPE not given');
              HOLE_TYPE=1;
      end
      
      % refractive indices
      n_Diamond = 2.4;%no unit
      n_Air = 1;%no unit
      n_bottom_square=3.5214;%no unit
      % distance between holes
      d_holes_mum = 0.220;%mum
      % hole radius
      hole_radius_X = 0.28*d_holes_mum;%mum
      %hole_radius_Z = pillar_radius_mum - (d_holes_mum-2*hole_radius_X);%mum
      hole_radius_Z = hole_radius_X;
      % number of holes on bottom
      bottom_N = 12;%no unit
      % number of holes on top
      top_N = 12;%no unit
      % distance between 2 holes around cavity
      d_holes_cavity = 2*d_holes_mum;%mum
      Lcav = d_holes_cavity - d_holes_mum; % mum
      % d_holes_cavity = Lcav + d_holes_mum;
      % top box offset
      top_box_offset=1;%mum
      %bottom square thickness
      
      % ITERATIONS = 261600;%no unit
      % ITERATIONS = 32000;%no unit
      % ITERATIONS = 10;%no unit

%        ITERATIONS=1048400
      FIRST=65400;
      REPETITION=524200;
      WALLTIME=360;

      TIMESTEP=0.9;%mus
      TIME_CONSTANT=4.000000E-09;%mus
      AMPLITUDE=1.000000E+01;%V/mum???
      TIME_OFFSET=2.700000E-08;%mus
              
      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      % additional calculations
      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      
      % max mesh intervals
      delta_diamond = 0.5*lambda/(15*n_Diamond);
      delta_hole = delta_diamond;
      delta_outside = 2*delta_diamond;
      delta_center = delta_diamond;
      delta_boundary = delta_diamond;
      
      % center area where excitation takes place (for meshing)
      center_radius = 2*delta_center;

      % buffers (area outside pillar where mesh is fine)
      X_buffer = 4*delta_diamond;%mum
      Y_buffer = 4*delta_diamond;%mum
      Z_buffer = 4*delta_diamond;%mum

      % dimension and position parameters
      Ymax = 5*2*pillar_radius_mum;%2*(pillar_radius_mum + Y_buffer + 4*delta_outside);%mum
      pillar_height = (bottom_N+top_N)*d_holes_mum + Lcav;
      Xmax = pillar_height;%mum
      Zmax = Ymax;%mum
      
      pillar_centre_Y = Ymax/2;
      pillar_centre_X = bottom_N*d_holes_mum + Lcav/2;
      pillar_centre_Z = Zmax/2;

      % meshing parameters
      thicknessVector_X = [ ];
      max_delta_Vector_X = [ ];
      mesh_factor=1;
      for i=1:bottom_N
              thicknessVector_X = [ thicknessVector_X, d_holes_mum/2 - hole_radius_X, 2*hole_radius_X, d_holes_mum/2 - hole_radius_X ];
              max_delta_Vector_X = [ max_delta_Vector_X, mesh_factor*delta_diamond, mesh_factor*delta_hole, mesh_factor*delta_diamond ];
      end
      thicknessVector_X = [ thicknessVector_X, Lcav/2-center_radius, 2*center_radius, Lcav/2-center_radius ];
      max_delta_Vector_X = [ max_delta_Vector_X, mesh_factor*delta_diamond, mesh_factor*delta_center, mesh_factor*delta_diamond ];
      for i=1:top_N
              thicknessVector_X = [ thicknessVector_X, d_holes_mum/2 - hole_radius_X, 2*hole_radius_X, d_holes_mum/2 - hole_radius_X ];
              max_delta_Vector_X = [ max_delta_Vector_X, mesh_factor*delta_diamond, mesh_factor*delta_hole, mesh_factor*delta_diamond ];
      end

      delta_min = min(max_delta_Vector_X);

      if HOLE_TYPE == 1
        thicknessVector_Y_1 = [ Ymax/2-pillar_radius_mum-Y_buffer, Y_buffer, pillar_radius_mum-center_radius, center_radius ];
      elseif HOLE_TYPE == 2
        thicknessVector_Y_1 = [ Ymax/2-pillar_radius_mum-Y_buffer, Y_buffer, pillar_radius_mum-center_radius, center_radius ];
      else
        thicknessVector_Y_1 = [ Ymax/2-pillar_radius_mum-Y_buffer, Y_buffer, pillar_radius_mum-center_radius, center_radius ];
      end

      thicknessVector_Y_2 = fliplr(thicknessVector_Y_1);
      thicknessVector_Y = [ thicknessVector_Y_1, thicknessVector_Y_2 ];
      
      max_delta_Vector_Y_1 = [ delta_outside, delta_boundary, delta_hole, delta_center ];
      max_delta_Vector_Y_2 = fliplr(max_delta_Vector_Y_1);
      max_delta_Vector_Y = [ max_delta_Vector_Y_1, max_delta_Vector_Y_2 ];

      %disp(['thicknessVector_Y = ',thicknessVector_Y])
      %thicknessVector_Y
      %max_delta_Vector_Y
      %disp(['max_delta_Vector_Y = ',])

      thicknessVector_Z = [ Zmax/2.0-pillar_radius_mum-Z_buffer, Z_buffer, pillar_radius_mum-hole_radius_Z, hole_radius_Z-center_radius, center_radius ];
      max_delta_Vector_Z = [ delta_outside, delta_boundary, delta_diamond, delta_diamond, delta_center ];
      
      [ delta_X_vector, local_delta_X_vector ] = subGridMultiLayer(max_delta_Vector_X,thicknessVector_X);
      [ delta_Y_vector, local_delta_Y_vector ] = subGridMultiLayer(max_delta_Vector_Y,thicknessVector_Y);
      [ delta_Z_vector, local_delta_Z_vector ] = subGridMultiLayer(max_delta_Vector_Z,thicknessVector_Z);

      % for the frequency snapshots
      
      Xplanes = [ 0,
      bottom_N/2*d_holes_mum,
      pillar_centre_X-delta_center,
      pillar_centre_X,
      pillar_centre_X+delta_center,
      bottom_N*d_holes_mum + Lcav + top_N/2*d_holes_mum,
      pillar_height ];
      
      Yplanes = [ 0,
      Ymax/2-pillar_radius_mum-Y_buffer,
      Ymax/2-pillar_radius_mum,
      Ymax/2-hole_radius_X,
      Ymax/2-2*delta_center,
      Ymax/2-delta_center,
      Ymax/2,
      Ymax/2+delta_center,
      Ymax/2+2*delta_center,
      Ymax/2+hole_radius_X,
      Ymax/2+pillar_radius_mum,
      Ymax/2+pillar_radius_mum+Y_buffer,
      Ymax ];

      Zplanes = [ 0,
      Zmax/2-pillar_radius_mum-Z_buffer,
      Zmax/2-pillar_radius_mum,
      Zmax/2-2*delta_center,
      Zmax/2-delta_center,
      Zmax/2 ];
      
      % for probes
      probes_X_vector = Xplanes(2:length(Xplanes)-1);
      probes_Y_vector = Yplanes(2:8);
      probes_Z_vector = Zplanes(2:4);
      
      probes_X_vector_center = Xplanes(3:5);
      probes_Y_vector_center = [Yplanes(6),Yplanes(8)];
      
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
      %~ copyfile(fullfile(getuserdir(),'MATLAB','entity.lst'),[DSTDIR,filesep,BASENAME]);
      % .in file
      INFILENAME = [DSTDIR,filesep,BASENAME,filesep,BASENAME,'.in'];
      GEOin(INFILENAME, { [BASENAME,'.inp'],[BASENAME,'.geo'] });
      % .sh file
      %TODO: improve this
      % WORKDIR = ['$HOME/loncar_structure','/',BASENAME];
      GEOshellscript([DSTDIR,filesep,BASENAME,filesep,BASENAME,'.sh'], BASENAME, '$HOME/bin/fdtd', '$JOBDIR', WALLTIME);

      % .cmd file
      GEOcommand([DSTDIR,filesep,BASENAME,filesep,BASENAME,'.cmd'], BASENAME);
      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      % .geo file
      disp('Writing GEO file...');

      % open file
      out = fopen([DSTDIR,filesep,BASENAME,filesep,BASENAME,'.geo'],'wt');

      % write header
      fprintf(out,'**GEOMETRY FILE\n');
      fprintf(out,'\n');

      % initialize current y
      X_current=0;
          
      if print_pillar
          % create main pillar
          L = [ X_current, Ymax/2 - pillar_radius_mum, Zmax/2 - pillar_radius_mum ];
          U = [ X_current + pillar_height, Ymax/2 + pillar_radius_mum, Zmax/2 + pillar_radius_mum ];
          GEOblock(out, L, U, n_Diamond^2, 0);
      end

      X_current = X_current + d_holes_mum/2;

      if print_holes
          % hole settings
          permittivity = n_Air^2;
          conductivity = 0;
          
          % create bottom holes
          for i=1:bottom_N
          
              if print_holes_bottom
                  centre = [ X_current, Ymax/2, Zmax/2 ];
                  if HOLE_TYPE == 1
                  GEOcylinder(out, centre, 0, hole_radius_X, 2*pillar_radius_mum, permittivity, conductivity, 0);
                  elseif HOLE_TYPE == 2
                  lower = [ X_current - hole_radius_X, Ymax/2 - pillar_radius_mum, Zmax/2 - hole_radius_X];
                  upper = [ X_current + hole_radius_X, Ymax/2 + pillar_radius_mum, Zmax/2 + hole_radius_X];
                  GEOblock(out, lower, upper, permittivity, conductivity);
                  else
                  lower = [ X_current - hole_radius_X, Ymax/2 - pillar_radius_mum, Zmax/2 - hole_radius_Z];
                  upper = [ X_current + hole_radius_X, Ymax/2 + pillar_radius_mum, Zmax/2 + hole_radius_Z];
                  GEOblock(out, lower, upper, permittivity, conductivity);
                  end
              end

              X_current = X_current + d_holes_mum;
          end

          X_current = X_current - d_holes_mum + d_holes_cavity;

          % create top holes
          for i=1:top_N
          
              if print_holes_top
                  centre = [ X_current, Ymax/2, Zmax/2 ];
                  if HOLE_TYPE == 1
                  GEOcylinder(out, centre, 0, hole_radius_X, 2*pillar_radius_mum, permittivity, conductivity, 0);
                  elseif HOLE_TYPE == 2
                  lower = [ X_current - hole_radius_X, Ymax/2 - pillar_radius_mum, Zmax/2 - hole_radius_X];
                  upper = [ X_current + hole_radius_X, Ymax/2 + pillar_radius_mum, Zmax/2 + hole_radius_X];
                  GEOblock(out, lower, upper, permittivity, conductivity);
                  else
                  lower = [ X_current - hole_radius_X, Ymax/2 - pillar_radius_mum, Zmax/2 - hole_radius_Z];
                  upper = [ X_current + hole_radius_X, Ymax/2 + pillar_radius_mum, Zmax/2 + hole_radius_Z];
                  GEOblock(out, lower, upper, permittivity, conductivity);
                  end
              end
              
              X_current = X_current + d_holes_mum;
          end
          
      end

          %write box
          L = [ 0, 0, 0 ];
          U = [ Xmax, Zmax, Ymax/2 ];
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

      if print_excitation
          P_Xm = [ pillar_centre_X-2*delta_center, pillar_centre_Y, pillar_centre_Z ];
          P_Xp = [ pillar_centre_X+2*delta_center, pillar_centre_Y, pillar_centre_Z ];
          P_Ym1 = [ pillar_centre_X, pillar_centre_Y-1*delta_center, pillar_centre_Z ];
          P_Yp1 = [ pillar_centre_X, pillar_centre_Y+1*delta_center, pillar_centre_Z ];
          P_Ym2 = [ pillar_centre_X, pillar_centre_Y-2*delta_center, pillar_centre_Z ];
          P_Yp2 = [ pillar_centre_X, pillar_centre_Y+2*delta_center, pillar_centre_Z ];
          P_Zm1 = [ pillar_centre_X, pillar_centre_Y, pillar_centre_Z-1*delta_center ];
          P_Zp1 = [ pillar_centre_X, pillar_centre_Y, pillar_centre_Z+1*delta_center ];
          P_Zm2 = [ pillar_centre_X, pillar_centre_Y, pillar_centre_Z-2*delta_center ];
          P_Zp2 = [ pillar_centre_X, pillar_centre_Y, pillar_centre_Z+2*delta_center ];
          P_center = [ pillar_centre_X, pillar_centre_Y, pillar_centre_Z ];
          Ey = [ 0, 1, 0 ];
          Ez = [ 0, 0, 1 ];
          H = [ 0, 0, 0 ];
          type = 10;
          


        if excitation_type == 1
          GEOexcitation(out, 7, P_Ym1, P_center, Ey, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, EXCITATION_FREQUENCY, 0, 0, 0, 0);
        elseif  excitation_type == 2
          GEOexcitation(out, 7, P_Zm1, P_center, Ez, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, EXCITATION_FREQUENCY, 0, 0, 0, 0);
        elseif  excitation_type == 3
          GEOexcitation(out, 7, P_Ym2, P_center, Ey, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, EXCITATION_FREQUENCY, 0, 0, 0, 0);
        elseif  excitation_type == 4
          GEOexcitation(out, 7, P_Zm2, P_center, Ez, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, EXCITATION_FREQUENCY, 0, 0, 0, 0);
        else
          error('invalid direction');
        end


          
      end

          Xpos_bc = 2; Xpos_param = [1,1,0];
          Ypos_bc = 2; Ypos_param = [1,1,0];
          Zpos_bc = 1; Zpos_param = [1,1,0];
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

      if print_mesh
          GEOmesh(out, delta_X_vector, delta_Y_vector, delta_Z_vector);
      end
          
      % frequency snapshots
      first = FIRST;
      repetition = REPETITION;
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
        %disp('Writing snapshots')
        %for iY = 1:length(Yplanes)
            %plane = 2;
            %P1 = [0, Yplanes(iY), 0];
            %P2 = [Xmax, Yplanes(iY), Ymax/2];
            %disp('Writing snapshots A')
            %GEOfrequency_snapshot(out, first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, SNAPSHOTS_FREQUENCY, starting_sample, E, H, J);
            %disp('Writing snapshots B')
            %GEOtime_snapshot(out, first, repetition, plane, P1, P2, E, H, J, power,0);
        %end
        %for iX = 1:length(Xplanes)
            %plane = 1;
            %P1 = [Xplanes(iX), 0, 0];
            %P2 = [Xplanes(iX), Zmax, Ymax/2];
            %GEOfrequency_snapshot(out, first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, SNAPSHOTS_FREQUENCY, starting_sample, E, H, J);
            %GEOtime_snapshot(out, first, repetition, plane, P1, P2, E, H, J, power,0);
        %end
        %for iZ = 1:length(Zplanes)
            %plane = 3;
            %P1 = [0, 0, Zplanes(iZ)];
            %P2 = [Xmax, Zmax, Zplanes(iZ)];
            %GEOfrequency_snapshot(out, first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, SNAPSHOTS_FREQUENCY, starting_sample, E, H, J);
            %GEOtime_snapshot(out, first, repetition, plane, P1, P2, E, H, J, power,0);
        %end
        
        plane = 1;
        P1 = [pillar_centre_X, 0, 0];
        P2 = [pillar_centre_X, Zmax, Ymax/2];
        GEOfrequency_snapshot(out, first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, SNAPSHOTS_FREQUENCY, starting_sample, E, H, J);
        GEOtime_snapshot(out, first, repetition, plane, P1, P2, E, H, J, power,0);
        
        plane = 2;
        P1 = [0, Zmax/2, 0];
        P2 = [Xmax, Zmax/2, Ymax/2];
        GEOfrequency_snapshot(out, first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, SNAPSHOTS_FREQUENCY, starting_sample, E, H, J);
        GEOtime_snapshot(out, first, repetition, plane, P1, P2, E, H, J, power,0);
        
        plane = 3;
        P1 = [0, 0, Ymax/2-2*delta_center];
        P2 = [Xmax, Zmax, Ymax/2-2*delta_center];
        GEOfrequency_snapshot(out, first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, SNAPSHOTS_FREQUENCY, starting_sample, E, H, J);
        GEOtime_snapshot(out, first, repetition, plane, P1, P2, E, H, J, power,0);
          
      end

      if print_probes
          % probes
          step=10;
          E=[1,1,1];
          H=[1,1,1];
          J=[0,0,0];
          power = 0;
          for iX =1:length(probes_X_vector)
              % XZ probes
              for iZ =1:length(probes_Z_vector)
                  GEOprobe(out, [probes_X_vector(iX), Yplanes(6), probes_Z_vector(iZ)], step, E, H, J, power );
              end
              % XY probes
              for iY =1:length(probes_Y_vector)
                  GEOprobe(out, [probes_X_vector(iX), probes_Y_vector(iY), Zplanes(5)], step, E, H, J, power );
              end
          end
          
          % XY center probes
          for iX =1:length(probes_X_vector_center)
              for iY =1:length(probes_Y_vector_center)
                  GEOprobe(out, [probes_X_vector_center(iX), probes_Y_vector_center(iY), Zplanes(4)], step, E, H, J, power );
              end
          end
      end
      
      %write footer
      fprintf(out,'end\n'); %end the file

      %close file
      fclose(out);
      disp('...done');
end
