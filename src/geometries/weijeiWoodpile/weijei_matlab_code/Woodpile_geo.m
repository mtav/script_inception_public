function Woodpile_geo(vertical_period, refractive_index_log, refractive_index_outer, directory, w_factor, defect_size_vector)

  interRodDistance=vertical_period/sqrt(2); % Distance between two adjacent logs
  n_logs = 13; % number of logs in each layer
  w = w_factor*vertical_period; % width of the logs
  h = 0.25*vertical_period; % heigth of logs (should be 1/4 for fcc to not overlap)
  L=(n_logs-1)*interRodDistance+w+interRodDistance;  % Length of logs (should > (n_logs-1)*interRodDistance+w)

  eps = refractive_index_log^2; % Dielectric constant of logs (GaP)
  eps_back = refractive_index_outer^2; % Dielectric constant of background material
  n_layers = 37; % Number of layers of logs required
  %defect_size = 1*interRodDistance; % The defect is a cube

  %buffer = max(2*interRodDistance, vertical_period);
  buffer = 1.25;
  box_size = max(n_logs*interRodDistance + w, n_layers*0.25*vertical_period) + 2*buffer;

  XL = 0; % Lower edge of the simulation domain in x direction.
  YL = 0; % Lower edge of the simulation domain in y direction.
  ZL = 0; % Lower edge of the simulation domain in z direction.

  XU = box_size; % Upper edge of the simulation domain in x direction.
  YU = box_size; % Upper edge of the simulation domain in y direction.
  ZU = box_size; % Upper edge of the simulation domain in z direction.

  x1L = -w/2-(n_logs-1)*interRodDistance/2:interRodDistance:(n_logs-1)*interRodDistance/2-w/2;
  x1U = x1L+w;
  y1L = -L/2;
  y1U = L/2;
  zzL = -h/2-(n_layers-1)*h/2:h:(n_layers-1)*h/2-h/2;
  zzU = zzL+h;

  for i=1:4:n_layers
    x_L((1+(i-1)*n_logs):i*n_logs) = x1L;
    x_U((1+(i-1)*n_logs):i*n_logs) = x1U;
    y_L((1+(i-1)*n_logs):i*n_logs) = y1L;
    y_U((1+(i-1)*n_logs):i*n_logs) = y1U;
    z_L((1+(i-1)*n_logs):i*n_logs) = zzL(i);
    z_U((1+(i-1)*n_logs):i*n_logs) = zzU(i);  
  end

  for i=2:4:n_layers
    x_L((1+(i-1)*n_logs):i*n_logs) = y1L;
    x_U((1+(i-1)*n_logs):i*n_logs) = y1U;
    y_L((1+(i-1)*n_logs):i*n_logs) = x1L;
    y_U((1+(i-1)*n_logs):i*n_logs) = x1U;
    z_L((1+(i-1)*n_logs):i*n_logs) = zzL(i);
    z_U((1+(i-1)*n_logs):i*n_logs) = zzU(i);  
  end

  for i=3:4:n_layers
    x_L((1+(i-1)*n_logs):i*n_logs) = x1L+interRodDistance/2;
    x_U((1+(i-1)*n_logs):i*n_logs) = x1U+interRodDistance/2;
    y_L((1+(i-1)*n_logs):i*n_logs) = y1L;
    y_U((1+(i-1)*n_logs):i*n_logs) = y1U;
    z_L((1+(i-1)*n_logs):i*n_logs) = zzL(i);
    z_U((1+(i-1)*n_logs):i*n_logs) = zzU(i);  
  end

  for i=4:4:n_layers
    x_L((1+(i-1)*n_logs):i*n_logs) = y1L;
    x_U((1+(i-1)*n_logs):i*n_logs) = y1U;
    y_L((1+(i-1)*n_logs):i*n_logs) = x1L+interRodDistance/2;
    y_U((1+(i-1)*n_logs):i*n_logs) = x1U+interRodDistance/2;
    z_L((1+(i-1)*n_logs):i*n_logs) = zzL(i);
    z_U((1+(i-1)*n_logs):i*n_logs) = zzU(i);  
  end
  
  x_Lnew = x_L+(XU-XL)/2;
  x_Unew = x_U+(XU-XL)/2;
  y_Lnew = y_L+(YU-YL)/2;
  y_Unew = y_U+(YU-YL)/2;
  z_Lnew = z_L+(ZU-ZL)/2;
  z_Unew = z_U+(ZU-ZL)/2;

  XL_D = (XU-XL)/2 - 0.5*defect_size_vector(1);
  XU_D = (XU-XL)/2 + 0.5*defect_size_vector(1);
  YL_D = (YU-YL)/2 - 0.5*defect_size_vector(2);
  YU_D = (YU-YL)/2 + 0.5*defect_size_vector(2);
  ZL_D = (ZU-ZL)/2 - 0.5*defect_size_vector(3);
  ZU_D = (ZU-ZL)/2 + 0.5*defect_size_vector(3);

  % Write out the .geo file

  fid = fopen([directory, filesep, 'sim.geo'], 'wt');
  fprintf(fid,'**GEOMETRY FILE\n');
  fprintf(fid,'\n');

  fprintf(fid,'BLOCK **name=backfill\n');
  fprintf(fid,'{\n');
  fprintf(fid,'%7E', XL);
  fprintf(fid,' **XL\n');
  fprintf(fid,'%7E', YL);
  fprintf(fid,' **YL\n');
  fprintf(fid,'%7E', ZL);
  fprintf(fid,' **ZL\n');
  fprintf(fid,'%7E', XU);
  fprintf(fid,' **XU\n');
  fprintf(fid,'%7E', YU);
  fprintf(fid,' **YU\n');
  fprintf(fid,'%7E', ZU);
  fprintf(fid,' **ZU\n');
  fprintf(fid,'%7E', eps_back);
  fprintf(fid,' **relative permittivity\n');
  fprintf(fid,'%7E', 0);
  fprintf(fid,' **relative conductivity\n');
  fprintf(fid,'}\n');
  fprintf(fid,'\n');

  fprintf(fid,'BLOCK **name=defect\n');
  fprintf(fid,'{\n');
  fprintf(fid,'%7E', XL_D);
  fprintf(fid,' **XL\n');
  fprintf(fid,'%7E', YL_D);
  fprintf(fid,' **YL\n');
  fprintf(fid,'%7E', ZL_D);
  fprintf(fid,' **ZL\n');
  fprintf(fid,'%7E', XU_D);
  fprintf(fid,' **XU\n');
  fprintf(fid,'%7E', YU_D);
  fprintf(fid,' **YU\n');
  fprintf(fid,'%7E', ZU_D);
  fprintf(fid,' **ZU\n');
  fprintf(fid,'%7E', eps);
  fprintf(fid,' **relative permittivity\n');
  fprintf(fid,'%7E', 0);
  fprintf(fid,' **relative conductivity\n');
  fprintf(fid,'}\n');
  fprintf(fid,'\n');

  for i=1:length(x_Lnew)
    fprintf(fid,'BLOCK **name=woodpile\n');
    fprintf(fid,'{\n');
    fprintf(fid,'%7E', x_Lnew(i));
    fprintf(fid,' **XL\n');
    fprintf(fid,'%7E', y_Lnew(i));
    fprintf(fid,' **YL\n');
    fprintf(fid,'%7E', z_Lnew(i));
    fprintf(fid,' **ZL\n');
    fprintf(fid,'%7E', x_Unew(i));
    fprintf(fid,' **XU\n');
    fprintf(fid,'%7E', y_Unew(i));
    fprintf(fid,' **YU\n');
    fprintf(fid,'%7E', z_Unew(i));
    fprintf(fid,' **ZU\n');
    fprintf(fid,'%7E', eps);
    fprintf(fid,' **relative permittivity\n');
    fprintf(fid,'%7E', 0);
    fprintf(fid,' **relative conductivity\n');
    fprintf(fid,'}\n');
    fprintf(fid,'\n');
  end

  fprintf(fid,'BOX  **name=box\n');
  fprintf(fid,'{\n');
  fprintf(fid,'%7E', XL);
  fprintf(fid,' **XL\n');
  fprintf(fid,'%7E', YL);
  fprintf(fid,' **YL\n');
  fprintf(fid,'%7E', ZL);
  fprintf(fid,' **ZL\n');
  fprintf(fid,'%7E', XU);
  fprintf(fid,' **XU\n');
  fprintf(fid,'%7E', YU);
  fprintf(fid,' **YU\n');
  fprintf(fid,'%7E', ZU);
  fprintf(fid,' **ZU\n');
  fprintf(fid,'}\n');

  fprintf(fid,'\n');
  fprintf(fid,'end');
  fprintf(fid,'\n');

  fclose(fid);
end
