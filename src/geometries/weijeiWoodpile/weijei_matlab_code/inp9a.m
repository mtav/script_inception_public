function inp9a(vertical_period, excitation_direction, directory, w_factor)
  clc 
  clear all

  d=0.342;
  a=d/sqrt(2); % Distance between two adjacent logs
  n_logs=13; % number of logs in each layer
  w=0.2*d; % width of the logs
  h=0.25*d; % heigth of logs (should be 1/4 for fcc to not overlap)
  L=(n_logs-1)*a+w+a;  % Length of logs (should > (n_logs-1)*a+w)
  n_layers=37;
  Def_a=0.9*a;

  defect=Def_a/2;
  x=L/2;
  y=L/2;
  z=h*n_layers/2;
  x_space=2-x;
  y_space=2-y;
  z_space=2-z;

  mesh_d=defect/10;

  mesh_x(1)=(0.5*a+0.5*w-11*mesh_d)/3;
  mesh_x(2)=(0.5*a-w)/3;
  mesh_x(3)= w/4;
  mesh_x(4)=(x_space-5*mesh_x(3))/7;

  mesh_z(1)=(1.5*h-10*mesh_d)/2;
  mesh_z(2)=h/5;
  mesh_z(3)=(z_space-5*mesh_z(2))/7;

  x_mesh_0(1:11)=mesh_d;
  x_mesh_1(1:3)=mesh_x(1);
  x_mesh_2=repmat([kron([mesh_x(2) mesh_x(3)],ones(1,3)) mesh_x(3)],1,n_logs-1);
  x_mesh_3(1:5)=mesh_x(3);
  x_mesh_4(1:7)=mesh_x(4);

  x_mesh_rev=[x_mesh_0 x_mesh_1 x_mesh_2 x_mesh_3 x_mesh_4];
  x_mesh_for=fliplr(x_mesh_rev);
  xmesh=[x_mesh_for x_mesh_rev];

  ymesh=xmesh;

  z_mesh_0(1:10)=mesh_d;
  z_mesh_1(1:2)=mesh_z(1);
  z_mesh_2=repmat(kron(mesh_z(2),ones(1,5)),1,17);
  z_mesh_3(1:5)=mesh_z(2);
  z_mesh_4(1:7)=mesh_z(3);

  z_mesh_rev=[z_mesh_0 z_mesh_1 z_mesh_2 z_mesh_3 z_mesh_4];
  z_mesh_for=fliplr(z_mesh_rev);
  zmesh=[z_mesh_for z_mesh_rev];


  xp_1=2;
  yp_1=2+4*mesh_d;
  zp_1=2;

  xp_2=2+4*mesh_d;
  yp_2=2;
  zp_2=2;

  xp_3=2;
  yp_3=2;
  zp_3=2-5*mesh_d;

  xp_4=2;
  yp_4=2;
  zp_4=2;

  xe_1=2;
  ye_1=2;
  ze_1=2-mesh_d;
  xe_2=2;
  ye_2=2;
  ze_2=2+mesh_d;

  % Write .inp files whose are adaped for Gema V.2 

  fid = fopen('0.9a_ez.inp', 'wt');

  fprintf(fid,'PROBE **PROBE DEFINITION 1 Ez\n');
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

  fprintf(fid,'PROBE **PROBE DEFINITION 2 Ey\n');
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

  fprintf(fid,'PROBE **PROBE DEFINITION 3 Ex\n');
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

  fprintf(fid,'PROBE **PROBE DEFINITION 4\n');
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

  fprintf(fid,'EXCITATION **EXCITATION DEFINITION\n');
  fprintf(fid,'{\n');
  fprintf(fid,'7 ** CURRENT SOURCE \n');
  fprintf(fid,'%7E', xe_1);
  fprintf(fid,' **X\n');
  fprintf(fid,'%7E', ye_1);
  fprintf(fid,' **Y\n');
  fprintf(fid,'%7E', ze_1);
  fprintf(fid,' **Z\n');
  fprintf(fid,'%7E', xe_2);
  fprintf(fid,' **X\n');
  fprintf(fid,'%7E', ye_2);
  fprintf(fid,' **Y\n');
  fprintf(fid,'%7E', ze_2);
  fprintf(fid,' **Z\n');
  fprintf(fid,'0 **EX\n');
  fprintf(fid,'0 **EY\n');
  fprintf(fid,'1 **EZ\n');
  fprintf(fid,'0 **HX\n');
  fprintf(fid,'0 **HY\n');
  fprintf(fid,'0 **HZ\n');
  fprintf(fid,'10 **GAUSSIAN MODULATED SINUSOID\n');
  fprintf(fid,'4.000000E-009 **TIME CONSTANT\n');
  fprintf(fid,'1.000000E+001 **AMPLITUDE\n');
  fprintf(fid,'2.700000E-008 **TIME OFFSET\n');
  fprintf(fid,'4.706318E+008 **FREQUENCY (MHZ)     637 nm\n');
  fprintf(fid,'0.000000E+00 **UNUSED PARAMETER\n');
  fprintf(fid,'0.000000E+00 **UNUSED PARAMETER\n');
  fprintf(fid,'0.000000E+00 **UNUSED PARAMETER\n');
  fprintf(fid,'0.000000E+00 **UNUSED PARAMETER\n');
  fprintf(fid,'}\n');
  fprintf(fid,'\n');

  fprintf(fid,'FLAG  **PROGRAM CONTROL OPTIONS\n');
  fprintf(fid,'{\n');
  fprintf(fid,'5 **ITERATION METHOD\n');
  fprintf(fid,'0.000000 **PROPAGATION CONSTANT (IGNORED IN 3D MODEL)\n');
  fprintf(fid,'0 **FLAG ONE\n');
  fprintf(fid,'0 **FLAG TWO\n');
  fprintf(fid,'1048400.000000 **ITERATIONS\n');
  fprintf(fid,'0.950000 **TIMESTEP\n');
  fprintf(fid,'"a" **ID CHARACTER (ALWAYS USE QUOTES)\n');
  fprintf(fid,'}\n');
  fprintf(fid,'\n');

  fprintf(fid,'BOUNDARY  **BOUNDARY DEFINITION\n');
  fprintf(fid,'{\n');
  fprintf(fid,'2 1 1 0 **X+\n');
  fprintf(fid,'2 1 1 0 **Y+\n');
  fprintf(fid,'2 1 1 0 **Z+\n');
  fprintf(fid,'2 1 1 0 **X-\n');
  fprintf(fid,'2 1 1 0 **Y-\n');
  fprintf(fid,'2 1 1 0 **Z-\n');
  fprintf(fid,'}\n');
  fprintf(fid,'\n');

  fprintf(fid,'XMESH **XMESH DEFINITION\n');
  fprintf(fid,'{\n');
  for i=1:length(xmesh),
      fprintf(fid,'%7E', xmesh(i));
      fprintf(fid,' **XMESH\n');
  end
  fprintf(fid,'}\n');
  fprintf(fid,'\n');

  fprintf(fid,'YMESH **YMESH DEFINITION\n');
  fprintf(fid,'{\n');
  for i=1:length(ymesh),
      fprintf(fid,'%7E', ymesh(i));
      fprintf(fid,' **YMESH\n');
  end
  fprintf(fid,'}\n');
  fprintf(fid,'\n');

  fprintf(fid,'ZMESH **ZMESH DEFINITION\n');
  fprintf(fid,'{\n');
  for i=1:length(zmesh),
      fprintf(fid,'%7E', zmesh(i));
      fprintf(fid,' **ZMESH\n');
  end
  fprintf(fid,'}\n');
  fprintf(fid,'\n');

  fprintf(fid,'end\n');

  fclose(fid);
end
