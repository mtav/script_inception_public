function micropillar(RADIUS, DSTDIR, BASENAME, N_TYPE, BOTTOM_N, TOP_N, FREQUENCY, SNAPSHOTS_ON, ITERATIONS)
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %description:
  %This file creates a .geo file with micro-pillar microcavity.
  % micropillar(RADIUS, DSTDIR, BASENAME, N_TYPE, BOTTOM_N, TOP_N, FREQUENCY, SNAPSHOTS_ON, ITERATIONS)
  % micropillar(1, 'fullfile(getuserdir(),'DATA','test'), 'test', 0, 6, 3, [get_c0()/0.7,get_c0()/0.8,get_c0()/0.9], 1, 32000)
  % micropillar(1, 'fullfile(getuserdir(),'DATA','test'), 'test', 0, 33, 26, 3.331027E+008, 1, 32000)
  %arguments
  % RADIUS in mum
  % DSTDIR
  % BASENAME
  % N_TYPE = 0 or 1
  % BOTTOM_N
  % TOP_N
  % FREQUENCY in MHz
  % SNAPSHOTS_ON = 0 or 1
  %
  %Example command:
  %micropillar(1, '~/TEST/micropillar_40_36/', 'micropillar_40_36', 1, 40, 36, get_c0()/0.900, 1, 100000)
  %
  %Usage:
  %micropillar(RADIUS, DSTDIR, BASENAME, N_TYPE, BOTTOM_N, TOP_N, FREQUENCY, SNAPSHOTS_ON, ITERATIONS)
  %
  %N_TYPE = 1 => refractive index calculated based on desired layer thickness, which is hardcoded in the script as:
  %===
  %h_GaAs=64*10-3;%mum
  %h_AlGaAs=81*10-3;%mum
  %n_GaAs=lambda/(4*h_GaAs);%no unit
  %n_AlGaAs=lambda/(4*h_AlGaAs);%no unit
  %cavity_h=253*10-3;%mum
  %cavity_n=n_GaAs;%no unit
  %===
  %
  %You will also need the latest generator functions from:
  %https://github.com/mtav/script_inception_public
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  disp('Reading input parameters...');

  %wavelength
  lambda=900*10^-3;%mum

  %helpers
  h_GaAs=64*10^-3;%mum
  h_AlGaAs=81*10^-3;%mum

  if N_TYPE == 0
    n_GaAs=3.521;%no unit
    n_AlGaAs=2.973;%no unit
  else
    n_GaAs=lambda/(4*h_GaAs);%no unit
    n_AlGaAs=lambda/(4*h_AlGaAs);%no unit
  end
  
  % N_TYPE
  % n_GaAs
  % n_AlGaAs
  % return

  %radius
  radius=RADIUS;%mum

  %IMPORTANT: We enter the layers from bottom to top. h1/h2 and n1/n2 correspond to this order.

  %bottom square thickness
  h_bottom_square=0.2;%mum
  n_bottom_square=3.5214;%no unit

  %bottom DBR
  bottom_N=BOTTOM_N;%no unit
  bottom_h1=h_GaAs;%mum
  bottom_n1=n_GaAs;%no unit
  bottom_h2=h_AlGaAs;%mum
  bottom_n2=n_AlGaAs;%no unit

  %cavity
  cavity_h=253*10^-3;%mum
  cavity_n=n_GaAs;%no unit

  %top DBR
  top_N=TOP_N;%no unit
  top_h1=h_AlGaAs;%mum
  top_n1=n_AlGaAs;%no unit
  top_h2=h_GaAs;%mum
  top_n2=n_GaAs;%no unit

  %space dimensions
  top_box_offset=1;%mum

  %Filename
  filename = strcat(DSTDIR,filesep,BASENAME);%string
  mkdir(DSTDIR);
  
  % not yet generated files
  %copyfile(fullfile(getuserdir(),'entity.lst'),DSTDIR);
  
  % .sh file
  GEOshellscript([filename,'.sh'], BASENAME);

  if exist('ITERATIONS','var')==0
    disp('ITERATIONS not given');
    ITERATIONS = 261600;%no unit
    % ITERATIONS = 32000;%no unit
    % ITERATIONS=10;%no unit
  end

  TIMESTEP=0.9;%mus
  TIME_CONSTANT=4.000000E-09;%mus
  AMPLITUDE=1.000000E+01;%V/mum???
  TIME_OFFSET=2.700000E-08;%mus
  
  % SNAPSHOTS_ON=0;
    
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %additional calculations
  
  % FREQUENCY=get_c0()/lambda; % if lambda in mum, FREQUENCY will be in MHz
  EXCITATION_FREQUENCY = get_c0()/lambda;

  % max mesh intervals
  delta_bottom_square = lambda/(10*n_bottom_square);
  delta_bottom_1 = lambda/(10*bottom_n1);
  delta_bottom_2 = lambda/(10*bottom_n2);
  delta_cavity = lambda/(10*cavity_n);
  delta_top_1 = lambda/(10*top_n1);
  delta_top_2 = lambda/(10*top_n2);
  delta_air = lambda/4;
  delta_center = lambda/(15*cavity_n);
  delta_boundary = delta_cavity;
  
  center_radius = 4*delta_center;

  %buffers (area outside pillar where mesh is fine)
  y_buffer = 32*delta_top_2;%mum

  Xmax = 2*(radius + 4*delta_cavity + 4*delta_air);%mum
  pillar_height = bottom_N*(bottom_h1+bottom_h2) + cavity_h + top_N*(top_h1+top_h2);
  Ymax = h_bottom_square + pillar_height + y_buffer + top_box_offset;%mum
  Zmax = Xmax;%mum
  
  P1_SNAPSHOT_BOX = [0,0,0];
  P2_SNAPSHOT_BOX = [Xmax/2,h_bottom_square + pillar_height + y_buffer,Zmax];

  pillar_centre_X = Xmax/2;
  pillar_centre_Y = h_bottom_square + bottom_N*(bottom_h1+bottom_h2) + cavity_h/2;
  pillar_centre_Z = Zmax/2;
  
  thicknessVector_Y = [ h_bottom_square ];
  max_delta_Vector_Y = [ delta_bottom_square ];
  for i=1:bottom_N
    thicknessVector_Y = [thicknessVector_Y, bottom_h1, bottom_h2];
    max_delta_Vector_Y = [max_delta_Vector_Y, delta_bottom_1, delta_bottom_2];
  end
  thicknessVector_Y = [ thicknessVector_Y, cavity_h/2-center_radius, 2*center_radius, cavity_h/2-center_radius ];
  max_delta_Vector_Y = [ max_delta_Vector_Y, delta_cavity, delta_center, delta_cavity ];
  for i=1:top_N
    thicknessVector_Y = [thicknessVector_Y, top_h1, top_h2];
    max_delta_Vector_Y = [max_delta_Vector_Y, delta_top_1, delta_top_2];
  end
  thicknessVector_Y = [ thicknessVector_Y, y_buffer, top_box_offset ];
  
  % n_min = 0.1;
  
  max_delta_Vector_Y = [ max_delta_Vector_Y, delta_top_2, delta_air ];

  delta_min = min(max_delta_Vector_Y);

  x_buffer = 4*delta_cavity;%mum
  z_buffer = 4*delta_cavity;%mum

  thicknessVector_X = [ Xmax/2-radius-x_buffer, x_buffer, radius-center_radius, center_radius ];
  thicknessVector_Z = [ Zmax/2-radius-z_buffer, z_buffer, radius-center_radius, center_radius, center_radius, radius-center_radius, z_buffer, Zmax/2-radius-z_buffer ];
  
  max_delta_Vector_X = [ delta_air, delta_cavity, delta_cavity, delta_center ];
  max_delta_Vector_Z = [ delta_air, delta_cavity, delta_cavity, delta_center, delta_center, delta_cavity, delta_cavity, delta_air ];
  
  [ delta_X, local_delta_X ] = subGridMultiLayer(max_delta_Vector_X,thicknessVector_X);
  [ delta_Y, local_delta_Y ] = subGridMultiLayer(max_delta_Vector_Y,thicknessVector_Y);
  [ delta_Z, local_delta_Z ] = subGridMultiLayer(max_delta_Vector_Z,thicknessVector_Z);

  % for the frequency snapshots
  Xplanes = [ 0,
  Xmax/2-radius-x_buffer,
  Xmax/2-radius,
  Xmax/2-2*delta_center,
  Xmax/2-delta_center,
  Xmax/2 ];
    
  Yplanes = [ 0,
  h_bottom_square,
  h_bottom_square + ceil(bottom_N/2)*bottom_h1 + floor(bottom_N/2)*bottom_h2,
  pillar_centre_Y-delta_center,
  pillar_centre_Y,
  pillar_centre_Y+delta_center,
  h_bottom_square + bottom_N*(bottom_h1+bottom_h2) + cavity_h + ceil(top_N/2)*top_h1 + floor(top_N/2)*top_h2,
  h_bottom_square + pillar_height,
  h_bottom_square + pillar_height+1*delta_top_2,
  h_bottom_square + pillar_height+8*delta_top_2,
  h_bottom_square + pillar_height+32*delta_top_2,
  Ymax ];
  
  Zplanes = [ 0,
  Zmax/2-radius-z_buffer,
  Zmax/2-radius,
  Zmax/2-2*delta_center,
  Zmax/2-delta_center,
  Zmax/2,
  Zmax/2+delta_center,
  Zmax/2+2*delta_center,
  Zmax/2+radius,
  Zmax/2+radius+z_buffer,
  Zmax ];
  
  % for probes
  probes_X_vector = Xplanes(2:4);
  probes_Y_vector = Yplanes(2:11);
  probes_Z_vector = Zplanes(2:7);
  
  probes_Y_vector_center = Yplanes(4:6);
  probes_Z_vector_center = [Zplanes(5),Zplanes(7)];
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %GEO file generation
  disp('Writing GEO file...');

  %open file
  out = fopen(strcat(filename,'.geo'),'wt');

  %write header
  fprintf(out,'**GEOMETRY FILE\n');
  fprintf(out,'\n');

  %initialize current y
  y_current=0;

  %write block
  fprintf(out,'BLOCK **Block Definition (XL,YL,ZL,XU,YU,ZU)\n');
  fprintf(out,'{\n');
  fprintf(out,'%E **XL\n', 0);
  fprintf(out,'%E **YL\n', 0);
  fprintf(out,'%E **ZL\n', 0);
  fprintf(out,'%E **XU\n', Xmax);
  fprintf(out,'%E **YU\n', h_bottom_square);
  fprintf(out,'%E **ZU\n', Zmax);
  fprintf(out,'%E **relative Permittivity\n', n_bottom_square^2);
  fprintf(out,'%E **Conductivity\n', 0);
  fprintf(out,'}\n');
  fprintf(out,'\n');
  y_current = y_current + h_bottom_square;

  %write bottom cylinders
  %Bottom DBR ( from Layer2 of AlGaAs)
  for i=1:bottom_N

    %Layer 1
    fprintf(out,'CYLINDER **Cylinder Definition (XL,YL,ZL,XU,YU,ZU,R1,R2)\n');
    fprintf(out,'{\n');
    fprintf(out,'%E **X CENTRE\n', Xmax/2);
    fprintf(out,'%E **Y CENTRE\n', y_current + bottom_h1/2);
    fprintf(out,'%E **Z CENTRE\n', Zmax/2);
    fprintf(out,'%E **RADIUS 1\n', 0);
    fprintf(out,'%E **RADIUS 2\n', radius);
    fprintf(out,'%E **HEIGHT\n', bottom_h1);
    fprintf(out,'%E **Permittivity\n', bottom_n1^2);
    fprintf(out,'%E **Conductivity\n', 0);
    fprintf(out,'}\n');
    fprintf(out,'\n');
    y_current = y_current + bottom_h1;

    %Layer 2
    fprintf(out,'CYLINDER **Cylinder Definition (XL,YL,ZL,XU,YU,ZU,R1,R2)\n');
    fprintf(out,'{\n');
    fprintf(out,'%E **X CENTRE\n', Xmax/2);
    fprintf(out,'%E **Y CENTRE\n', y_current + bottom_h2/2);
    fprintf(out,'%E **Z CENTRE\n', Zmax/2);
    fprintf(out,'%E **RADIUS 1\n', 0);
    fprintf(out,'%E **RADIUS 2\n', radius);
    fprintf(out,'%E **HEIGHT\n', bottom_h2);
    fprintf(out,'%E **Permittivity\n', bottom_n2^2);
    fprintf(out,'%E **Conductivity\n', 0);
    fprintf(out,'}\n');
    fprintf(out,'\n');
    y_current = y_current + bottom_h2;

  end

  %write middle cylinder
  fprintf(out,'CYLINDER **Cylinder Definition (XL,YL,ZL,XU,YU,ZU,R1,R2)\n');
  fprintf(out,'{\n');
  fprintf(out,'%E **X CENTRE\n', Xmax/2);
  fprintf(out,'%E **Y CENTRE\n', y_current + cavity_h/2);
  fprintf(out,'%E **Z CENTRE\n', Zmax/2);
  fprintf(out,'%E **RADIUS 1\n', 0);
  fprintf(out,'%E **RADIUS 2\n', radius);
  fprintf(out,'%E **HEIGHT\n', cavity_h);
  fprintf(out,'%E **Permittivity\n', cavity_n^2);
  fprintf(out,'%E **Conductivity\n', 0);
  fprintf(out,'}\n');
  fprintf(out,'\n');
  y_current = y_current + cavity_h;

  %write top cylinders
  for i=1:top_N

    %Layer 1
    fprintf(out,'CYLINDER **Cylinder Definition (XL,YL,ZL,XU,YU,ZU,R1,R2)\n');
    fprintf(out,'{\n');
    fprintf(out,'%E **X CENTRE\n', Xmax/2);
    fprintf(out,'%E **Y CENTRE\n', y_current + top_h1/2);
    fprintf(out,'%E **Z CENTRE\n', Zmax/2);
    fprintf(out,'%E **RADIUS 1\n', 0);
    fprintf(out,'%E **RADIUS 2\n', radius);
    fprintf(out,'%E **HEIGHT\n', top_h1);
    fprintf(out,'%E **Permittivity\n', top_n1^2);
    fprintf(out,'%E **Conductivity\n', 0);
    fprintf(out,'}\n');
    fprintf(out,'\n');
    y_current = y_current + top_h1;

    %Layer 2
    fprintf(out,'CYLINDER **Cylinder Definition (XL,YL,ZL,XU,YU,ZU,R1,R2)\n');
    fprintf(out,'{\n');
    fprintf(out,'%E **X CENTRE\n', Xmax/2);
    fprintf(out,'%E **Y CENTRE\n', y_current + top_h2/2);
    fprintf(out,'%E **Z CENTRE\n', Zmax/2);
    fprintf(out,'%E **RADIUS 1\n', 0);
    fprintf(out,'%E **RADIUS 2\n', radius);
    fprintf(out,'%E **HEIGHT\n', top_h2);
    fprintf(out,'%E **Permittivity\n', top_n2^2);
    fprintf(out,'%E **Conductivity\n', 0);
    fprintf(out,'}\n');
    fprintf(out,'\n');
    y_current = y_current + top_h2;

  end

  %write box
  fprintf(out,'BOX  **BOX DEFINITION\n');
  fprintf(out,'{\n');
  fprintf(out,'%E **XL\n', 0);
  fprintf(out,'%E **YL\n', 0);
  fprintf(out,'%E **ZL\n', 0);
  fprintf(out,'%E **XU\n', Xmax/2);
  fprintf(out,'%E **YU\n', Ymax);
  fprintf(out,'%E **ZU\n', Zmax);
  fprintf(out,'}\n');
  fprintf(out,'\n');

  %write footer
  fprintf(out,'end\n'); %end the file

  %close file
  fclose(out);
  disp('...done');

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %IN file generation
  disp('Writing IN file...');

  %open file
  out = fopen(strcat(filename,'.in'),'wt');

  %write file
  fprintf(out,'%s\n',BASENAME);
  fprintf(out,'%s\n',BASENAME);

  %close file
  fclose(out);
  disp('...done');

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % .cmd file
  GEOcommand([filename,'.cmd'], BASENAME);

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %INP file generation
  disp('Writing INP file...');

  %open file
  out = fopen(strcat(filename,'.inp'),'wt');

  % excitation
  P1 = [ pillar_centre_X-2*delta_center, pillar_centre_Y, pillar_centre_Z ];
  P2 = [ pillar_centre_X, pillar_centre_Y, pillar_centre_Z ];
  E = [ 1, 0,	0];
  H = [ 0, 0,	0];
  type = 10;
  GEOexcitation(out, 7, P1, P2, E, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, EXCITATION_FREQUENCY);

  % boundary
  fprintf(out,'BOUNDARY  **BOUNDARY DEFINITION\n');
  fprintf(out,'{\n');
  fprintf(out,'1 1 1 0 **X+ \n');
  fprintf(out,'2 1 1 0 **Y+ \n');
  fprintf(out,'2 1 1 0 **Z+ \n');
  fprintf(out,'2 1 1 0 **X- \n');
  fprintf(out,'2 1 1 0 **Y- \n');
  fprintf(out,'2 1 1 0 **Z- \n');
  fprintf(out,'}\n');
  fprintf(out,'\n');

  % flag
  fprintf(out,'FLAG  **PROGRAM CONTROL OPTIONS\n');
  fprintf(out,'{\n');
  fprintf(out,'%d **ITERATION METHOD\n', 5);
  fprintf(out,'%d **PROPAGATION CONSTANT (IGNORED IN 3D MODEL)\n', 0);
  fprintf(out,'%d **FLAG ONE\n', 0);
  fprintf(out,'%d **FLAG TWO\n', 0);
  fprintf(out,'%d **ITERATIONS\n', ITERATIONS);
  fprintf(out,'%E **TIMESTEP\n', TIMESTEP);
  fprintf(out,'"id" **ID CHARACTER (ALWAYS USE QUOTES) \n');
  fprintf(out,'}\n');
  fprintf(out,'\n');

  % mesh X
  fprintf(out,'XMESH **XMESH DEFINITION\n');
  fprintf(out,'{\n');
  for i=1:length(delta_X)
    fprintf(out,'%E\n', delta_X(i));
  end
  fprintf(out,'}\n');
  fprintf(out,'\n');

  % mesh Y
  fprintf(out,'YMESH **YMESH DEFINITION\n');
  fprintf(out,'{\n');
  for i=1:length(delta_Y)
    fprintf(out,'%E\n', delta_Y(i));
  end
  fprintf(out,'}\n');
  fprintf(out,'\n');

  % mesh Z
  fprintf(out,'ZMESH **ZMESH DEFINITION\n');
  fprintf(out,'{\n');
  for i=1:length(delta_Z)
    fprintf(out,'%E\n', delta_Z(i));
  end
  fprintf(out,'}\n');
  fprintf(out,'\n');

  % probe
  function probe(P)
    fprintf(out,'PROBE **PROBE DEFINITION\n');
    fprintf(out,'{\n');
    fprintf(out,'%E **X\n', P(1));
    fprintf(out,'%E **Y\n', P(2));
    fprintf(out,'%E **Z\n', P(3));
    fprintf(out,'%d **STEP\n', 10);
    fprintf(out,'%d **EX\n', 1);
    fprintf(out,'%d **EY\n', 1);
    fprintf(out,'%d **EZ\n', 1);
    fprintf(out,'%d **HX\n', 1);
    fprintf(out,'%d **HY\n', 1);
    fprintf(out,'%d **HZ\n', 1);
    fprintf(out,'%d **JX\n', 0);
    fprintf(out,'%d **JY\n', 0);
    fprintf(out,'%d **JZ\n', 0);
    fprintf(out,'%d **POW\n', 0);
    fprintf(out,'}\n');
    fprintf(out,'\n');
  end
  
  % snapshots
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
  
  % snapshot boxes for NFF (near-to-far-field) transform
  GEOfrequency_snapshot(out, first, repetition, interpolate, real_dft, mod_only, mod_all, 1, P1_SNAPSHOT_BOX, P2_SNAPSHOT_BOX, FREQUENCY, starting_sample, E, H, J);
  GEOtime_snapshot(out, first, repetition, 1, P1_SNAPSHOT_BOX, P2_SNAPSHOT_BOX, E, H, J, power,0);
  
  % probes
  for iY =1:length(probes_Y_vector)
    % XY probes
    for iX =1:length(probes_X_vector)
      probe( [probes_X_vector(iX), probes_Y_vector(iY), Zplanes(6)] );
    end
    % ZY probes
    for iZ =1:length(probes_Z_vector)
      probe( [Xplanes(5), probes_Y_vector(iY), probes_Z_vector(iZ)] );
    end
  end
  
  % ZY center probes
  for iY =1:length(probes_Y_vector_center)
    for iZ =1:length(probes_Z_vector_center)
      probe( [Xplanes(4), probes_Y_vector_center(iY), probes_Z_vector_center(iZ)] );
    end
  end
  
  %write footer
  fprintf(out,'end\n'); %end the file

  %close file
  fclose(out);
  disp('...done');
end
