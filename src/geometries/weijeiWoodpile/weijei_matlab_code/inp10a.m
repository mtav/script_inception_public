function inp10a(vertical_period, excitation_direction, directory, w_factor)

  interRodDistance = vertical_period/sqrt(2); % Distance between two adjacent logs
  n_logs = 13; % number of logs in each layer
  w = w_factor*vertical_period; % width of the logs
  h = 0.25*vertical_period; % heigth of logs (should be 1/4 for fcc to not overlap)
  L = (n_logs-1)*interRodDistance+w+interRodDistance;  % Length of logs (should > (n_logs-1)*interRodDistance+w)
  n_layers = 37;
  defect_size = interRodDistance;

  %buffer = max(2*interRodDistance, vertical_period);
  buffer = 1.25;
  box_size = max(n_logs*interRodDistance + w, n_layers*0.25*vertical_period) + 2*buffer;
     
  defect = defect_size/2;
  x = L/2;
  y = L/2;
  z = h*n_layers/2;
  x_space = 0.5*box_size-x;
  y_space = 0.5*box_size-y;
  z_space = 0.5*box_size-z;

  mesh_d = defect/11;

  mesh_x(1) = (0.5*interRodDistance+0.5*w-12*mesh_d)/2;
  mesh_x(2) = (0.5*interRodDistance-w)/3;
  mesh_x(3) = w/4;
  mesh_x(4) = (x_space-5*mesh_x(3))/7;

  mesh_z(1) = (1.5*h-11*mesh_d);
  mesh_z(2) = h/5;
  mesh_z(3) = (z_space-5*mesh_z(2))/7;

  x_mesh_0(1:12) = mesh_d;
  x_mesh_1(1:2) = mesh_x(1);
  x_mesh_2 = repmat([kron([mesh_x(2) mesh_x(3)],ones(1,3)) mesh_x(3)],1,n_logs-1);
  x_mesh_3(1:5) = mesh_x(3);
  x_mesh_4(1:7) = mesh_x(4);

  x_mesh_rev = [x_mesh_0 x_mesh_1 x_mesh_2 x_mesh_3 x_mesh_4];
  x_mesh_for = fliplr(x_mesh_rev);
  xmesh = [x_mesh_for x_mesh_rev];

  ymesh = xmesh;

  z_mesh_0(1:11) = mesh_d;
  z_mesh_1 = mesh_z(1);
  z_mesh_2 = repmat(kron(mesh_z(2),ones(1,5)),1,17);
  z_mesh_3(1:5) = mesh_z(2);
  z_mesh_4(1:7) = mesh_z(3);

  z_mesh_rev = [z_mesh_0 z_mesh_1 z_mesh_2 z_mesh_3 z_mesh_4];
  z_mesh_for = fliplr(z_mesh_rev);
  zmesh = [z_mesh_for z_mesh_rev];

  xp_1 = 0.5*box_size;
  yp_1 = 0.5*box_size;
  zp_1 = 0.5*box_size;

  xp_2 = 0.5*box_size+4*mesh_d;
  yp_2 = 0.5*box_size;
  zp_2 = 0.5*box_size;

  xp_3 = 0.5*box_size;
  yp_3 = 0.5*box_size+4*mesh_d;
  zp_3 = 0.5*box_size;

  xp_4 = 0.5*box_size;
  yp_4 = 0.5*box_size;
  zp_4 = 0.5*box_size-5*mesh_d;

  if excitation_direction == 0
    xe_1 = 0.5*box_size-mesh_d;
    ye_1 = 0.5*box_size;
    ze_1 = 0.5*box_size;
    xe_2 = 0.5*box_size+mesh_d;
    ye_2 = 0.5*box_size;
    ze_2 = 0.5*box_size;
  elseif excitation_direction == 1
    xe_1 = 0.5*box_size;
    ye_1 = 0.5*box_size-mesh_d;
    ze_1 = 0.5*box_size;
    xe_2 = 0.5*box_size;
    ye_2 = 0.5*box_size+mesh_d;
    ze_2 = 0.5*box_size;
  else
    xe_1 = 0.5*box_size;
    ye_1 = 0.5*box_size;
    ze_1 = 0.5*box_size-mesh_d;
    xe_2 = 0.5*box_size;
    ye_2 = 0.5*box_size;
    ze_2 = 0.5*box_size+mesh_d;
  end

  % Write out the .inp file

  filename = [directory, filesep, 'sim.inp'];
  fid = fopen(filename, 'wt');

  current_source = 7;
  P1 = [xe_1,ye_1,ze_1];
  P2 = [xe_2,ye_2,ze_2];

  if excitation_direction == 0
    E = [1,0,0];
  elseif excitation_direction == 1
    E = [0,1,0];
  else
    E = [0,0,1];
  end
  H = [0,0,0];
  source_type = 10; % GAUSSIAN MODULATED SINUSOID
  time_constant = 4.000000E-09;
  amplitude = 1.000000E+01;
  time_offset = 2.700000E-08;
  frequency = get_c0()/0.637; % 4.706318E+08 **FREQUENCY (MHZ)     637 nm
  GEOexcitation(fid, current_source, P1, P2, E, H, source_type, time_constant, amplitude, time_offset, frequency)
  
  GEOboundary(fid,2,[1,1,0],2,[1,1,0],2,[1,1,0],2,[1,1,0],2,[1,1,0],2,[1,1,0]);

  iteration_method = 5;
  propagation_constant = 0;
  flag_1 = 0;
  flag_2 = 0;
  iterations = 1048400;
  timestep = 0.95;
  id_character = 'a';
  GEOflag(fid, iteration_method, propagation_constant, flag_1, flag_2, iterations, timestep, id_character)

  fprintf(fid,'XMESH **name=mesh\n');
  fprintf(fid,'{\n');
  for i=1:length(xmesh)
      fprintf(fid,'%7E', xmesh(i));
      fprintf(fid,'\n');
  end
  fprintf(fid,'}\n');
  fprintf(fid,'\n');

  fprintf(fid,'YMESH **name=mesh\n');
  fprintf(fid,'{\n');
  for i=1:length(ymesh)
      fprintf(fid,'%7E', ymesh(i));
      fprintf(fid,'\n');
  end
  fprintf(fid,'}\n');
  fprintf(fid,'\n');

  fprintf(fid,'ZMESH **name=mesh\n');
  fprintf(fid,'{\n');
  for i=1:length(zmesh)
      fprintf(fid,'%7E', zmesh(i));
      fprintf(fid,'\n');
  end
  fprintf(fid,'}\n');
  fprintf(fid,'\n');

  fprintf(fid,'PROBE **name=probe 1 centro\n');
  fprintf(fid,'{\n');
  fprintf(fid,'%7E', xp_1);
  fprintf(fid,' **X\n');
  fprintf(fid,'%7E', yp_1);
  fprintf(fid,' **Y\n');
  fprintf(fid,'%7E', zp_1);
  fprintf(fid,' **Z\n');
  fprintf(fid,'10 **STEP\n');
  fprintf(fid,'1 **EX\n');
  fprintf(fid,'1 **EY\n');
  fprintf(fid,'1 **EZ\n');
  fprintf(fid,'1 **HX\n');
  fprintf(fid,'1 **HY\n');
  fprintf(fid,'1 **HZ\n');
  fprintf(fid,'0 **JX\n');
  fprintf(fid,'0 **JY\n');
  fprintf(fid,'0 **JZ\n');
  fprintf(fid,'0 **POW\n');
  fprintf(fid,'}\n');
  fprintf(fid,'\n');

  fprintf(fid,'PROBE **name=probe 2 X+\n');
  fprintf(fid,'{\n');
  fprintf(fid,'%7E', xp_2);
  fprintf(fid,' **X\n');
  fprintf(fid,'%7E', yp_2);
  fprintf(fid,' **Y\n');
  fprintf(fid,'%7E', zp_2);
  fprintf(fid,' **Z\n');
  fprintf(fid,'10 **STEP\n');
  fprintf(fid,'1 **EX\n');
  fprintf(fid,'1 **EY\n');
  fprintf(fid,'1 **EZ\n');
  fprintf(fid,'1 **HX\n');
  fprintf(fid,'1 **HY\n');
  fprintf(fid,'1 **HZ\n');
  fprintf(fid,'0 **JX\n');
  fprintf(fid,'0 **JY\n');
  fprintf(fid,'0 **JZ\n');
  fprintf(fid,'0 **POW\n');
  fprintf(fid,'}\n');
  fprintf(fid,'\n');

  fprintf(fid,'PROBE **name=probe 3 Y+\n');
  fprintf(fid,'{\n');
  fprintf(fid,'%7E', xp_3);
  fprintf(fid,' **X\n');
  fprintf(fid,'%7E', yp_3);
  fprintf(fid,' **Y\n');
  fprintf(fid,'%7E', zp_3);
  fprintf(fid,' **Z\n');
  fprintf(fid,'10 **STEP\n');
  fprintf(fid,'1 **EX\n');
  fprintf(fid,'1 **EY\n');
  fprintf(fid,'1 **EZ\n');
  fprintf(fid,'1 **HX\n');
  fprintf(fid,'1 **HY\n');
  fprintf(fid,'1 **HZ\n');
  fprintf(fid,'0 **JX\n');
  fprintf(fid,'0 **JY\n');
  fprintf(fid,'0 **JZ\n');
  fprintf(fid,'0 **POW\n');
  fprintf(fid,'}\n');
  fprintf(fid,'\n');

  fprintf(fid,'PROBE **name=probe 4 Z-\n');
  fprintf(fid,'{\n');
  fprintf(fid,'%7E', xp_4);
  fprintf(fid,' **X\n');
  fprintf(fid,'%7E', yp_4);
  fprintf(fid,' **Y\n');
  fprintf(fid,'%7E', zp_4);
  fprintf(fid,' **Z\n');
  fprintf(fid,'10 **STEP\n');
  fprintf(fid,'1 **EX\n');
  fprintf(fid,'1 **EY\n');
  fprintf(fid,'1 **EZ\n');
  fprintf(fid,'1 **HX\n');
  fprintf(fid,'1 **HY\n');
  fprintf(fid,'1 **HZ\n');
  fprintf(fid,'0 **JX\n');
  fprintf(fid,'0 **JY\n');
  fprintf(fid,'0 **JZ\n');
  fprintf(fid,'0 **POW\n');
  fprintf(fid,'}\n');
  fprintf(fid,'\n');

  fprintf(fid,'end\n');

  fclose(fid);
end
