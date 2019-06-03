function create_harminv_input_files(SRCDIR, DSTDIR)
  % create harminv input files for SRCDIR and places them in DSTDIR + tries to locate resonance peak

  if exist('SRCDIR','var')==0
    disp('SRCDIR not given');
      SRCDIR = uigetdir(pwd(),'SRCDIR');
  end
  if ~(exist(SRCDIR,'dir'))
    error('dir not found');
  end

  if exist('DSTDIR','var')==0
    disp('DSTDIR not given');
      DSTDIR = uigetdir(pwd(),'DSTDIR');
  end
  if ~(exist(DSTDIR,'dir'))
    error('dir not found');
  end

  % ===================
  function [ vEnd, vStart, dt, fmin, fmax, peak_frequency_vector ] = processProbe(BASE)
    %=======================================
    % create simple .prn file containing Ex
    %=======================================
    format long e
    INFILE = [ SRCDIR, filesep, BASE, '.prn' ];
    if ~(exist(INFILE,'file'))
      fprintf('WARNING: File %s not found\n',INFILE);
      vEnd=0;vStart=0;dt=0;fmin=0;fmax=0;
      return;
    end
    [header, data] = readPrnFile(INFILE);
    % Time Ex Ey Ez Hx Hy Hz 
    out = data(:,2);
    save([DSTDIR,filesep,BASE,'_Ex.prn'],'out','-ascii');
    
    [ vEnd, vStart, dt, fmin, fmax, peak_frequency_vector ] = analyzePRN(INFILE, [DSTDIR,filesep,BASE,'_bilan.txt'], 1/25);
  end
  
  % ===================
  function writeHarmInvArgs()
    %=======================================
    % analyze top probes from source pillar
    %=======================================
    % get pillar cavity frequency
    dt_vec = [0,0,0,0];
    fmin_vec = [0,0,0,0];
    fmax_vec = [0,0,0,0];
    [ vEnd1, vStart1, dt_vec(1), fmin_vec(1), fmax_vec(1), peak_frequency_vector1 ] = processProbe('p62id');
    [ vEnd2, vStart2, dt_vec(2), fmin_vec(2), fmax_vec(2), peak_frequency_vector2 ] = processProbe('p71id');
    [ vEnd3, vStart3, dt_vec(3), fmin_vec(3), fmax_vec(3), peak_frequency_vector3 ] = processProbe('p80id');
    [ vEnd4, vStart4, dt_vec(4), fmin_vec(4), fmax_vec(4), peak_frequency_vector4 ] = processProbe('p89id');
    
    %================================================
    % add theoretical resonance frequency (ugly hack)
    %================================================
    
    [ pillar_type, n_type, radius, N_bottom, N_top, basename ] = getDataFromDirname(SRCDIR);
    %wavelength
    lambda=900*10^-3;%mum

    %helpers
    h_GaAs=64*10^-3;%mum
    h_AlGaAs=81*10^-3;%mum

    if n_type == 0
      n_GaAs=3.521;%no unit
      n_AlGaAs=2.973;%no unit
    else
      n_GaAs=lambda/(4*h_GaAs);%no unit
      n_AlGaAs=lambda/(4*h_AlGaAs);%no unit
    end
    n0 = 1; % air refractive index
    Lcav = 253; % (nm)

    [ E, lambda, radius_vector, E_vector, lambda_vector ] = resonanceEnergy(n_GaAs, n_AlGaAs, n0, Lcav, radius);

    peak_frequency_vector4 = [ peak_frequency_vector4, get_c0()/(lambda*10^(-3)) ];
    disp('=== peak_frequency_vector4 ===');
    % length(peak_frequency_vector4)
    % peak_frequency_vector4
    
    %================================================
    % generate the new pillar!!!
    %================================================
    % newDir = fullfile(getuserdir(),'DATA','newPillars_timeNFF_only');
    % newDir = fullfile(getuserdir(),'DATA','newPillars_freqNFF_only');
    % newDir = fullfile(getuserdir(),'DATA','newPillars_time_only');
    % newDir = fullfile(getuserdir(),'DATA','newPillars_freq_only');
    % newDir = fullfile(getuserdir(),'DATA','newPillars');
    newDir = fullfile(getuserdir(),'DATA','newPillars_madness');
    mkdir(newDir);
    % newDir = DSTDIR;
    
    micropillar(radius, [newDir,filesep,basename,'_1'], [basename,'_1'], n_type, N_bottom, N_top, peak_frequency_vector4, 1, 1);
    micropillar(radius, [newDir,filesep,basename,'_32000'], [basename,'_32000'], n_type, N_bottom, N_top, peak_frequency_vector4, 1, 32000);
    micropillar(radius, [newDir,filesep,basename,'_65000'], [basename,'_65000'], n_type, N_bottom, N_top, peak_frequency_vector4, 1, 65000);
    
    %=======================================
    % create harminv_parameters.txt file
    %=======================================
    for i=1:length(dt_vec)
      fprintf('%d: dt=%E fmin=%E fmax=%E\n', i, dt_vec(i), fmin_vec(i), fmax_vec(i));
    end
    dt = min(dt_vec);
    
    if dt==0
      error('dt==0');
    end
    
    fmin = min(fmin_vec);
    fmax = max(fmax_vec);
    %write parameters to file
    file = fopen([DSTDIR,filesep,'harminv_parameters.txt'],'w');
    fprintf('final: dt=%E fmin=%E fmax=%E\n', dt, fmin, fmax);
    fprintf(file,'final: dt=%E fmin=%E fmax=%E\n', dt, fmin, fmax);
    fclose(file);
    
  end
  % ===================
        
  writeHarmInvArgs();
  
end
