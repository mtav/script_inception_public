function [ vEnd, vStart, dt, fmin, fmax, peak_frequency_vector, data_min, data_max ] = analyzePRN2(fullpath, peak_file, delta_scaling, snapshot_col, probe_col)
  % Analyzes a single PRN file
  % snapshot_col:
  %1 x
  %2 z
  %3 Exmod
  %4 Exre
  %5 Exim
  %6 Eymod
  %7 Eyre
  %8 Eyim
  %9 Ezmod
  %10 Ezre
  %11 Ezim
  %12 Hxmod
  %13 Hxre
  %14 Hxim
  %15 Hymod
  %16 Hyre
  %17 Hyim
  %18 Hzmod
  %19 Hzre
  %20 Hzim
  % probe_col:
  %1 Time
  %2 Ex
  %3 Ey
  %4 Ez
  %5 Hx
  %6 Hy
  %7 Hz

    verbose=1;
  time_plot = 1;
  freq_plot_all = 1;
  freq_plot_zoom1 = 0;
  freq_plot_zoom2 = 0;
  
  %===============================
  % preparations
  %===============================

  if exist('fullpath','var')==0
    disp('fullpath not given');
    [FileName,PathName] = uigetfile('*.prn','Select the probe PRN file');
    fullpath = [PathName, filesep, FileName];
  end
    if verbose == 1
        disp(['fullpath = ',fullpath]);
    end

  if ~(exist(fullpath,'file'))
    error( ['File not found: ',fullpath] );
    return;
  end

  [ folder, basename, ext ] = fileparts(fullpath);
  if ~(isempty(folder))
    cd(folder);
  end
  
  [ foo, headquarters ] = fileparts(folder);

  if exist('peak_file','var')==0
    % disp('peak_file not given');
    peak_file = [folder, filesep, basename, '_bilan.txt'];
  end
  
  if exist('delta_scaling','var')==0
    % disp('delta_scaling not given');
    delta_scaling = 1/3;
  end

  if exist('snapshot_col','var')==0
    % disp('snapshot_col not given');
    snapshot_col = 3;
  end

  if exist('probe_col','var')==0
    % disp('probe_col not given');
    probe_col = 2;
  end
  
  % clf
  
  %===============================

    filebasename = basename;
    [header, data] = readPrnFile([filebasename,'.prn']);
  % size(header)
  % size(data)

  if verbose == 1
        disp(['processing ',filebasename,'.prn'])
    end

    data_min = min(data(:,probe_col));
    data_max = max(data(:,probe_col));

    if verbose == 1    
            disp(['min(data(:,',num2str(probe_col),'))=',num2str(data_min)]);
            disp(['max(data(:,',num2str(probe_col),'))=',num2str(data_max)]);
    end

  if time_plot == 1
    disp('	figure 1')
    figure;hold on;
    % size(data(:,1)*1e-9)
    % size(data(:,probe_col))
    plot(data(:,1)*1e-9,data(:,probe_col));
    title([ headquarters, '\\', basename,'  ',header{probe_col}]);
    xlabel('time (ns)');
    saveas(gcf,[filebasename,'_',header{probe_col},'.png'],'png');
  end
  
  %WARNING: The timestep is considered to be constant here!!!
    
  dt = 1e-12*(data(2,1)-data(1,1));  % Normally the data in probe file is in values of 1e*18 seconds
  
    if verbose == 1
        disp('	fourier transform start');
    end
    [calcFFT_output, lambda_vec] = calcFFT(data(:,probe_col),dt, 2^19);
  lambda_vec = 1e3*lambda_vec; % to get lambda in nm
    if verbose == 1
        disp('	fourier transform end');
    end

    %calculate magnitude of fft
    c_y_mag = abs(calcFFT_output);
    %calculate power of fft
    c_y_pow = calcFFT_output.* conj(calcFFT_output);

    % c_Mag=2*abs(calcFFT_output);
    % c_Mag=c_y_mag;
    c_Mag=c_y_pow;
    
  wavelength_vec = lambda_vec;

  if freq_plot_all == 1
    disp('	figure 2')
    figure;hold on;
    plot(wavelength_vec, c_Mag,'-b+');
    title([ headquarters, '\\', basename,' ',header{probe_col},'  Spectrum at Timestep:',num2str(length(data))])
    xlabel('Wavelength (nm)');
    ylabel('Mag');
    % saveas(gcf,[filebasename,'_',header{probe_col},'_FFT_all','.png'],'png');
    % writePrnFile(   [filebasename,'_',header{probe_col},'_FFT_all','.prn'],'wavelength Mag',[ wavelength_vec(:), c_Mag(:) ]);
  end

  fprintf('length(wavelength_vec)=%d\n',length(wavelength_vec));
  fprintf('min(wavelength_vec)=%E\n',min(wavelength_vec));
  fprintf('max(wavelength_vec)=%E\n',max(wavelength_vec));
    
  %===============================
    Mag_aver = sum(c_Mag)/length(c_Mag);
    detPeak_delta = delta_scaling * (max(c_Mag)-Mag_aver);

  fprintf('min = %E\n',min(c_Mag));
  fprintf('max = %E\n',max(c_Mag));
  fprintf('average = %E\n',Mag_aver);
  fprintf('detPeak_delta = %E\n',detPeak_delta);
    vStart=0;
    vEnd=0;
    fmin=0;
    fmax=0;

  % [ peakdata_all, peakdata_loc ] = zoomOnPeak(lambda_vec, c_Mag, detPeak_delta);

  % fprintf('Number of peaks found: %d\n', size(peakdata_loc,2));
  
  % wavelength_vec = peakdata_all.Xzoom;
  % c_Mag_zoom_1 = peakdata_all.Yzoom;
  %===============================
  
  if freq_plot_zoom1 == 1
    disp('	figure 3')
    figure;hold on;
    plot(wavelength_vec,c_Mag_zoom_1,'-b+');
    title([ headquarters, '\\', basename,' ',header{probe_col},'  Spectrum at Timestep:',num2str(length(data))]);
    xlabel('Wavelength (nm)');
    ylabel('Mag');
    saveas(gcf,[filebasename,'_',header{probe_col},'_FFT_zoom1','.png'],'png');
    writePrnFile(   [filebasename,'_',header{probe_col},'_FFT_zoom1','.prn'],'wavelength Mag',[ wavelength_vec(:), c_Mag_zoom_1(:) ]);
  end

  fprintf('length(wavelength_vec)=%d\n',length(wavelength_vec));
  fprintf('min(wavelength_vec)=%E\n',min(wavelength_vec));
  fprintf('max(wavelength_vec)=%E\n',max(wavelength_vec));
  
  %===============================
  peak_frequency_vector = [];
  return;
  superfile = fopen(peak_file,'w');
  % fprintf(superfile,'===============\n');
  % fprintf(superfile,'=== %s\n',fullpath);
  fprintf(superfile,'frequency, decay constant, Q, amplitude, phase, error\n');
  Qmax = -Inf;
  Qmax_idx = -1;
  for i=1:length(peakdata_loc)
    % fprintf(          'Q(%E)=%E\n',peakdata_loc(i).vEnd(1),peakdata_loc(i).Q);
    % fprintf(superfile,'Q(%E)=%E\n',peakdata_loc(i).vEnd(1),peakdata_loc(i).Q);
    lambda = peakdata_loc(i).vEnd(1);
    lambda_idx = peakdata_loc(i).index;
    
    frequency = 10^3*get_c0()/lambda;
    peak_frequency_vector = [ peak_frequency_vector, frequency ];

    amplitude = abs(calcFFT_output(lambda_idx));
    phase = angle(calcFFT_output(lambda_idx));
    decay_constant = 0;
    Err = 0;
    fprintf(superfile, '%E, %E, %E, %E, %E, %E\n', frequency, decay_constant, peakdata_loc(i).Q, amplitude, phase, Err);
    if(peakdata_loc(i).Q>Qmax)
      Qmax = peakdata_loc(i).Q;
      Qmax_idx = i;
    end
  end
  
  % fprintf(superfile,'=============================================================\n');
  fclose(superfile);
  %===============================
  wavelength_vec = peakdata_loc(Qmax_idx).Xzoom;
  c_Mag_zoom_2 = peakdata_loc(Qmax_idx).Yzoom;
  vStart = peakdata_loc(Qmax_idx).vStart;
  vEnd = peakdata_loc(Qmax_idx).vEnd;
  %===============================
  
  % wavelength_vec = wavelength_vec(:);
  % c_Mag_zoom_2 = c_Mag_zoom_2(:);
  
  % [x0, y0, A, FWHM] = getLorentzStartValues(wavelength_vec, c_Mag_zoom_2, 0);
  % vStart = [x0, y0, A, FWHM];
  % [x0, y0, A, FWHM] = getLorentzEndValues(wavelength_vec, c_Mag_zoom_2, vStart);
  % vEnd = [x0, y0, A, FWHM];
  
  % return
  
  if freq_plot_zoom2 == 1
    disp('	figure 4')
    figure;hold on;
    plot(wavelength_vec, c_Mag_zoom_2,'ob');
    plot(wavelength_vec, lorentz(vStart, wavelength_vec),'-g');
    plot(wavelength_vec, lorentz(vEnd, wavelength_vec),'-r');
    title([ headquarters, filesep, basename,' ',header{probe_col},'  Spectrum at Timestep:',num2str(length(data))]);
    xlabel('Wavelength (nm)');
    ylabel('Mag');
    saveas(gcf,[filebasename,'_',header{probe_col},'_FFT_zoom2','.png'],'png');
    writePrnFile(   [filebasename,'_',header{probe_col},'_FFT_zoom2','.prn'],'wavelength Mag',[ wavelength_vec(:), c_Mag_zoom_2(:) ]);
  end
  
  lambda0_start = vStart(1);
  lambda0_end = vEnd(1);
  
  fprintf('lambda0_start = %E\n',lambda0_start);
  fprintf('lambda0_end = %E\n', lambda0_end);
  
  lambdamin = min(peakdata_all.Xzoom);
  lambdamax = max(peakdata_all.Xzoom);
  
  % TODO: figure out where 10^-12 and 10^-2 factors come from!!!
  fmin = 10^3*get_c0()/lambdamax;
  fmax = 10^3*get_c0()/lambdamin;
  fprintf('=>dt=%E fmin=%E fmax=%E\n', dt, fmin, fmax);
  % vEnd = [x0, y0, A, FWHM];
  % Q=x0/FWHM = vEnd(1)/vEnd(4)

  % fprintf('Qmax = %E\n', lambda0_end);
  % Qmax
return
