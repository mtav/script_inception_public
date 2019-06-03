function generate_resonance_pillar(SRCDIR, DSTDIR)

  % UNFINISHED

  %===============================
  % preparations
  %===============================

  if exist('SRCDIR','var')==0
    disp('SRCDIR not given');
      SRCDIR = uigetdir('D:\Simulations\BFDTD','SRCDIR');
  end
  if ~(exist(SRCDIR,'dir'))
    disp('dir not found');
    return;
  end

  if exist('DSTDIR','var')==0
    disp('DSTDIR not given');
      DSTDIR = uigetdir('D:\Simulations\BFDTD','DSTDIR');
  end
  if ~(exist(DSTDIR,'dir'))
    disp('dir not found');
        mkdir(DSTDIR);
    % return;
  end

  % copyfile(fullfile(getuserdir(),'MATLAB','entity.lst'),DSTDIR);
  % copyfile(fullfile(getuserdir(),'MATLAB','qedc3_2_05.sh'),DSTDIR);
  cd(DSTDIR);

  %===============================
  DSTDIR
  SRCDIR
  close all


  %=======================================
  % analyze top probes from source pillar
  %=======================================
  % get pillar cavity frequency
  dt_vec = [0,0,0,0];
  fmin_vec = [0,0,0,0];
  fmax_vec = [0,0,0,0];
  [ vEnd1, vStart1, dt_vec(1), fmin_vec(1), fmax_vec(1) ] = analyzePRN([SRCDIR,'\\p062id.prn'], [DSTDIR,'\\p062id.peakfile'], 1/4);
  [ vEnd2, vStart2, dt_vec(2), fmin_vec(2), fmax_vec(2) ] = analyzePRN([SRCDIR,'\\p071id.prn'], [DSTDIR,'\\p071id.peakfile'], 1/4);
  [ vEnd3, vStart3, dt_vec(3), fmin_vec(3), fmax_vec(3) ] = analyzePRN([SRCDIR,'\\p080id.prn'], [DSTDIR,'\\p080id.peakfile'], 1/4);
  [ vEnd4, vStart4, dt_vec(4), fmin_vec(4), fmax_vec(4) ] = analyzePRN([SRCDIR,'\\p089id.prn'], [DSTDIR,'\\p089id.peakfile'], 1/4);
  for i=1:length(dt_vec)
    fprintf('%d: dt=%E fmin=%E fmax=%E\n', i, dt_vec(i), fmin_vec(i), fmax_vec(i));
  end
  dt = min(dt_vec);
  fmin = min(fmin_vec);
  fmax = max(fmax_vec);
  fprintf('final: dt=%E fmin=%E fmax=%E\n', dt, fmin, fmax);

  % vEnd = [x0, y0, A, FWHM];
  % Q=x0/FWHM = vEnd(1)/vEnd(4)

  % lambda = 900*10^-3;%mum

  
  
  return;
  
  %===============================
  % get data from source pillar
  %===============================
  % get pillar data
  [ folder, basename, ext ] = fileparts(SRCDIR);
  infos = regexp(basename, '_', 'split');
  pillar_type = infos(2);
  n_type = str2num(char(infos(3)));
  radius = str2num(char(infos(4)))/10;
  
  %===============================
  % generate new pillar
  %===============================

  SNAPSHOTS_ON = 1;
  
  c0=299792458;%mum/mus
  FREQUENCY = c0/lambda;

  dirname = strcat('pillar_',pillar_type,'_',num2str(n_type),'_',num2str(10*radius),'_at_cavity_frequency');
  micropillar(radius, dirname, 'qedc3_2_05', n_type, a_N_bottom, a_N_top, FREQUENCY, SNAPSHOTS_ON);
  
end
