function [ wavelength_nm, Q_lorentz, Q_harminv_local, Q_harminv_global, handles ] = plotProbe(varargin)
  % Usage:
  %   [ wavelength_nm, Q_lorentz, Q_harminv_local, Q_harminv_global, handles ] = plotProbe(varargin)
  %
  % cf source code for full param value field list...
  %
  % IMPORTANT: time plot uses [tmin_mus_used, tmax_mus_used] time range!
  % IMPORTANT: FFT plot uses [tmin_mus_used, tmax_mus_used] time range!
  % IMPORTANT: harminv uses [tmin_mus_used, tmax_mus_used] time range!
  % IMPORTANT: => [tmin_mus_used, tmax_mus_used] affects time plot, FFT plot and Harminv calculations!!!
  % IMPORTANT: [handles.FFTrange_min_mum, handles.FFTrange_max_mum] also affects range over which peaks are searched for and harminv entries selected.
  % TODO: cleanup this whole mess...
  % TODO: return figure handle instead of taking care of saving inside this function?
  % TODO: Unit specification (or manual arbitrary labeling)
  % TODO: implement options in PP GUI
  % TODO: Make usable without args like doHarminv (or with own GUI...)
  % TODO: Pass multiple ranges to a single harminv call for "local harminv" runs
  % TODO: Pass those ranges as arguments (for potential future GUI range selection feature)
  % TODO: Quadruple axis system: f, lambda, normalized f, normalized lambda ?
  % TODO: Add vertical lines indicating the chosen processing ranges (different from the plotting ranges).
  % TODO: Plot FFT based on harminv output.
  % TODO: Indicate maximum/minimum resolution, Q, etc obtainable in FFT.
  % TODO: move filename + column back into normal args? Ask for file+column if not provided?...

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%%%% create parser
  p = inputParser();
  
  p = inputParserWrapper(p, 'addParamValue', 'filename', '', @ischar);
  
  p = inputParserWrapper(p, 'addParamValue', 'column', -1, @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'handles', struct(), @isstruct);
  p = inputParserWrapper(p, 'addParamValue', 'DoAnalysis', false, @islogical);
  
  % The time range on which to do the Fourier transform and run harminv (always in mus):
  p = inputParserWrapper(p, 'addParamValue', 'tlim', [NaN, NaN],  @(x) isnumeric(x) && length(x)==2);
  
  % The range in which to run harminv (always mum or MHz)
  % IMPORTANT: It is always assumed to be of the form [min, max], i.e. [fmin, fmax] or [lambda_min, lambda_max], i.e.:
  % [fmin, NaN] = [NaN, lambda_max]
  % [NaN, fmax] = [lambda_min, NaN]
  p = inputParserWrapper(p, 'addParamValue', 'harminv_range', [NaN, NaN], @(x) isnumeric(x) && length(x)==2);
  p = inputParserWrapper(p, 'addParamValue', 'harminv_range_type', 'frequency', @(x) any(validatestring(x, {'frequency','wavelength'})));
  
  p = inputParserWrapper(p, 'addParamValue', 'FFT_x_axis_type', 'frequency', @(x) any(validatestring(x, {'frequency','wavelength'})));
  p = inputParserWrapper(p, 'addParamValue', 'FFT_xlabel', 'frequency (MHz)', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'FFT_scalingFactor', 1, @isnumeric);
  %if isfield(handles,'')==0; FFT_f_or_lambda = 2; end; % 1:frequency, 2:wavelength
  %if isfield(handles,'')==0; handles.FFT_xlabel = ; end; \lambda (nm)
  %if isfield(handles,'')==0; p.Results.FFT_scalingFactor = ; end; 1000
  
  p = inputParserWrapper(p, 'parse', varargin{:});
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % create an easier to use variable...
  if strcmpi(validatestring(p.Results.FFT_x_axis_type, {'frequency','wavelength'}), 'frequency');
    FFT_f_or_lambda = 1;
  else
    FFT_f_or_lambda = 2;
  end
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  probe_filename = p.Results.filename;
  if ~ischar(probe_filename) || isempty(probe_filename)
    [FNAME, FPATH, FLTIDX] = uigetfile('*.prn', 'Select a probe file');
    if ~ischar(FNAME) || isempty(FNAME)
      disp('No file selected. Exiting');
      return
    else
      probe_filename = fullfile(FPATH, FNAME);
    end
  end

  % simple hack to quickly fix PP again :)
  handles = p.Results.handles;

  if ~isstruct(handles)
    error('handles variable is not a structure. If you want to pass a filename and column, use plotProbe_CLI(probe_filename, col).');
  end

  % all handle fields
  if isfield(handles,'autosave')==0; handles.autosave = false; end;
  if isfield(handles,'imageSaveBasename')==0; handles.imageSaveBasename = ''; end;
  if isfield(handles,'hide_figures')==0; handles.hide_figures = false; end;
  if isfield(handles,'plotNothing')==0; handles.plotNothing = false; end;
  if isfield(handles,'verbosity')==0; handles.verbosity = 0; end;
  if isfield(handles,'plotLorentzFit')==0; handles.plotLorentzFit = false; end;
  if isfield(handles,'computeLorentz')==0; handles.computeLorentz = false; end;
  if isfield(handles,'computeHarminvLocal')==0; handles.computeHarminvLocal = false; end;
  if isfield(handles,'computeHarminvGlobal')==0; handles.computeHarminvGlobal = true; end;
  if isfield(handles,'useFFTrange')==0; handles.useFFTrange = true; end;
  if isfield(handles,'Qtext')==0; handles.Qtext = true; end;
  if isfield(handles,'peakStars')==0; handles.peakStars = true; end;
  if isfield(handles,'ViewingWindowSize_mum')==0; handles.ViewingWindowSize_mum = 0.200; end;
  if isfield(handles,'ViewingWindowThreshold')==0; handles.ViewingWindowThreshold = 1e-3; end; % stop plotting when the remaining Y values are under handles.ViewingWindowThreshold*max(Y)

  % The range in which to search for peaks:
  if isfield(handles,'FFTrange_min_mum')==0; handles.FFTrange_min_mum = 0.100; end;
  if isfield(handles,'FFTrange_max_mum')==0; handles.FFTrange_max_mum = 1.500; end;
    
  % Choose a plotting range for the FFT automatically:
  if isfield(handles,'autoZoomFFT')==0; handles.autoZoomFFT = true; end;

  % Choose a plotting range for the time automatically:
  if isfield(handles,'autoZoomTime')==0; handles.autoZoomTime = true; end;

  % The plotting ranges:
  if isfield(handles,'FFT_plot_lambda_min_mum')==0; handles.FFT_plot_lambda_min_mum = NaN; end;
  if isfield(handles,'FFT_plot_lambda_max_mum')==0; handles.FFT_plot_lambda_max_mum = NaN; end;

  % currently not implemented: TODO: remove/implement? Seems like more general range specification
  if isfield(handles,'plot_time_Xmin')==0; handles.plot_time_Xmin = NaN; end;
  if isfield(handles,'plot_time_Xmax')==0; handles.plot_time_Xmax = NaN; end;
  if isfield(handles,'plot_time_Ymin')==0; handles.plot_time_Ymin = NaN; end;
  if isfield(handles,'plot_time_Ymax')==0; handles.plot_time_Ymax = NaN; end;

  % currently not implemented: TODO: remove/implement? Seems like more general range specification
  if isfield(handles,'plot_FFT_Xmin')==0; handles.plot_FFT_Xmin = NaN; end;
  if isfield(handles,'plot_FFT_Xmax')==0; handles.plot_FFT_Xmax = NaN; end;
  if isfield(handles,'plot_FFT_Ymin')==0; handles.plot_FFT_Ymin = NaN; end;
  if isfield(handles,'plot_FFT_Ymax')==0; handles.plot_FFT_Ymax = NaN; end;

  %%%%%%%%%%%%%%%%
  wavelength_nm = -1;
  Q_lorentz = -1;
  Q_harminv_local = -1;
  Q_harminv_global = -1;
  
  [ folder, basename, ext ] = fileparts(probe_filename);
  [ geoname_folder, geoname_basename, geoname_basename_ext ] = fileparts(folder);
  geoname_basename = [ geoname_basename, geoname_basename_ext ]; % in case of dots in the directory name

  % read the PRN file if the header or data are not provided in the handles object
  if isfield(handles,'header')==0 || isfield(handles,'data')==0
    [handles.header, handles.data] = readPrnFile(probe_filename);
  end
  
  % Just to make sure we always have the same format for the header.
  handles.header = handles.header(:)';
  
  time_mus = 1e-12*handles.data(:,1);
  
  selected_column = p.Results.column;
  
  % Check if a valid column was given. Else ask user to select from a list of valid values.
  % TODO: Could create a readPrnFile wrapper asking to select file+column (because also used in plotSnapshot() for example)
  if ~isfinite(selected_column) || selected_column < 1 || selected_column > length(handles.header)
    [selected_column, ok] = listdlg('PromptString', 'Choose what you want to plot:\n', 'SelectionMode', 'single', 'ListString', handles.header);
    if ~ok
      disp('No valid column selected. Exiting.');
      return
    end
  end

  %if (selected_column<1) || (selected_column>length(handles.header))
    %warning('Please choose an integer value for ''column'' from the following:')
    %for idx=1:length(handles.header)
     %disp([num2str(idx),' : ',char(handles.header(idx))]);
    %end
    %return;
  %end
  data_name = handles.header(selected_column);
  data_time_domain = handles.data(:,selected_column);

  % calculate timestep
  if length(time_mus) < 2
    error('Not enough data to determine the timestep!');
  end
  
  % WARNING: The timestep is considered to be constant here!!!
  dt_mus = time_mus(2)-time_mus(1);  % handles.data(*,1) being in 10^-18 s (because input frequency is in 10^6 Hz), dt is in 10^-18 s/1e-12 = 10^-6 s

  % cut beginning of time signal:
  % TODO: Select cutoff time based on actual input/output data...
  if isnan(p.Results.tlim(1))
    tmin_mus_used = 0;
  else
    tmin_mus_used = p.Results.tlim(1);
  end
  if isnan(p.Results.tlim(2))
    tmax_mus_used = time_mus(end);
  else
    tmax_mus_used = p.Results.tlim(2);
  end
  if tmin_mus_used < tmax_mus_used
    [time_mus, data_time_domain] = zoomPlot(time_mus, data_time_domain, tmin_mus_used, tmax_mus_used);
  else
    warning( [ 'tmin_mus_used = ', num2str(tmin_mus_used),' >= tmax_mus_used = ', num2str(tmax_mus_used) ] );
  end

  % calculate the FFT
  % TODO: Re-implement nextpow2 NFFT as an option (should run faster)
  % (with NFFT = double the number of points you want in the output = 2^19)
  % (selected_column = whatever column you want from the time probe file, i.e. Ex,Ey,etc)
  % [calcFFT_output, lambda_vec_mum, freq_vec_Mhz] = calcFFT(data_time_domain,dt_mus, 2^19);
  % [calcFFT_output, lambda_vec_mum, freq_vec_Mhz] = calcFFT(data_time_domain,dt_mus, 2^22);
  % [calcFFT_output_oldstyle, lambda_vec_mum_oldstyle, freq_vec_Mhz_oldstyle] = calcFFT(data_time_domain,dt_mus, 2^22);
  [calcFFT_output, lambda_vec_mum, freq_vec_Mhz] = calcFFT(data_time_domain, dt_mus);

  % convert lambda to nm
  lambda_vec_nm = 1e3*lambda_vec_mum;
  %lambda_vec_nm_oldstyle = 1e3*lambda_vec_mum_oldstyle;

  if ~handles.plotNothing
    % create new figure
    if handles.hide_figures
      fig = figure('visible','off');
    else
      fig = figure('visible','on');
    end
  end
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % plot in the time domain to see the ringdown
  if ~handles.plotNothing
    subplot(1,2,1);
    plot(time_mus, data_time_domain);
    xlabel('time (\mus)');
    ylabel([char(data_name),' (arbitrary units)']);
    title( [ geoname_basename,' ', basename, ' ', char(data_name) ],'Interpreter','none');
    %ylabel(data_name);
    %title('Transversal field amplitude');

    % envelope fitting: CURRENTLY UNUSED/DISABLED
    %[xzoom,yzoom] = zoomPlot(time_mus,data_time_domain,4e-8,time_mus(end));
    %[xzoom,yzoom] = zoomPlot(time_mus,data_time_domain,1e-6,time_mus(end));
%      [xzoom,yzoom] = zoomPlot(time_mus, data_time_domain, tmin_mus_used, time_mus(end));
    %res.trace1.x = time_mus
    %res.trace1.y = data_time_domain
%      res.trace1.x = xzoom;
%      res.trace1.y = yzoom;
    %ringdown(res,0.01)
  
    % go back to normal figure
    %figure(fig)
    
  end
  
  disp(['DATA INFO: size(data_time_domain) = ', num2str(size(data_time_domain))]);
  disp(['DATA INFO: min(data_time_domain) = ', num2str(min(data_time_domain))]);
  disp(['DATA INFO: max(data_time_domain) = ', num2str(max(data_time_domain))]);
  if min(data_time_domain(:))==0 && max(data_time_domain(:))==0
    disp('WARNING: empty data');
    return;
  end


  
  if ~handles.plotNothing

    %%% set the axis range for the time domain plot
    
    xmin_time_domain_plot = time_mus(1);
    xmax_time_domain_plot = time_mus(length(data_time_domain));
    ymin = min(data_time_domain);
    ymax = max(data_time_domain);

    % Old time auto-zooming system...
    %% zoom plot on interesting region
    %for idx_max = length(data_time_domain):-1:1;
      %if data_time_domain(idx_max)>handles.ViewingWindowThreshold*ymax;
        %break;
      %end;
    %end;
    %xmax_time_domain_plot = time_mus(idx_max);

    % to show the interesting part of the time domain plot:
    time_domain_y_central = (ymax + ymin) / 2;
    time_domain_y_mean = mean(data_time_domain);
    time_domain_y_range = ymax - ymin;
    
    if handles.autoZoomTime
      for i = length(data_time_domain):-1:1
        if abs(data_time_domain(i) - time_domain_y_mean) > time_domain_y_range/100
          xmax_time_domain_plot = time_mus(i);
          break;
        end
      end
    end

    % finally set the axis
    axis([xmin_time_domain_plot, xmax_time_domain_plot, time_domain_y_central - 1.1*time_domain_y_range/2, time_domain_y_central + 1.1*time_domain_y_range/2]);
  end
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % plot the FFT to locate the resonance peak
  % define X and Y for the fitting (Y = power)
  X = lambda_vec_nm;
  %X_oldstyle = lambda_vec_nm_oldstyle;
  Y = calcFFT_output.* conj(calcFFT_output);
  %Y_oldstyle = calcFFT_output_oldstyle.* conj(calcFFT_output_oldstyle);
  
  % cut of anything to big
  if isnan(handles.FFTrange_min_mum)
    handles.FFTrange_min_mum = 1e-3*min(X);
  end
  if isnan(handles.FFTrange_max_mum)
    handles.FFTrange_max_mum = 1e-3*max(X);
  end
  if handles.useFFTrange && ~isnan(handles.FFTrange_min_mum) && ~isnan(handles.FFTrange_max_mum)
    [X, Y] = zoomPlot(X, Y, 1e3*handles.FFTrange_min_mum, 1e3*handles.FFTrange_max_mum);
  end

  if ~handles.plotNothing
    subplot(1,2,2);
    % TODO: At the moment X is in nm. Code should be cleaned up a bit to make all this easier to read, with X as frequency in MHz by default. (or with normalized units like MEEP/MPB)
    if FFT_f_or_lambda==1
      % plot as a function of frequency
      FFT_plot_X_data = p.Results.FFT_scalingFactor*(get_c0()./(1e-3*X));
    else
      % plot as a function of wavelength
      FFT_plot_X_data = p.Results.FFT_scalingFactor*1e-3*X;
    end
    FFT_plot_Y_data = Y;
    plot(FFT_plot_X_data, FFT_plot_Y_data); % plot the FFT
    xlabel(p.Results.FFT_xlabel);
    ylabel(['FFT of ',char(data_name),' (arbitrary units)']);
    title( [ geoname_basename,' ', basename, ' ', char(data_name) ],'Interpreter','none');
    %title('FFT of the transversal field amplitude');
  end

  disp(['DATA INFO: min(Y) = ',num2str(min(Y))]);
  disp(['DATA INFO: max(Y) = ',num2str(max(Y))]);
  if min(Y(:))==0 && max(Y(:))==0
    disp('WARNING: empty data');
    return;
  end

  % zoom plot on interesting region
  idx_max = find(Y==max(Y));
  %idx_max_oldstyle = find(Y_oldstyle==max(Y_oldstyle));

  % xmin_global and xmax_global are used for:
  % -automatic zooming
  % -automatic choosing of range on which to run harminv
  % NOTE: X is in nanometers
  % TODO: Add units to all variables (or stick to mum/mus standard)
  %xmin_global = X_oldstyle(idx_max_oldstyle(1)) - 1e3*handles.ViewingWindowSize_mum;
  %xmax_global = X_oldstyle(idx_max_oldstyle(length(idx_max))) + 1e3*handles.ViewingWindowSize_mum;
  xmin_global = X(idx_max(1)) - 1e3*handles.ViewingWindowSize_mum;
  xmax_global = X(idx_max(end)) + 1e3*handles.ViewingWindowSize_mum;

  if ~handles.plotNothing

    %%% set FFT plotting range

    % default axis ranges
    FFT_plot_X_min = min(FFT_plot_X_data);
    FFT_plot_X_max = max(FFT_plot_X_data);
    FFT_plot_Y_min = min(FFT_plot_Y_data);
    FFT_plot_Y_max = 1.1*max(FFT_plot_Y_data);

    % set handles.autoZoomFFT to false to get the full FFT plot
    if handles.autoZoomFFT % automatic zoom
      FFT_plot_lambda_min_mum = 1e-3*xmin_global;
      FFT_plot_lambda_max_mum = 1e-3*xmax_global;
    end

    % user-specified ranges
    if ~isnan(handles.FFT_plot_lambda_min_mum)
      FFT_plot_lambda_min_mum = handles.FFT_plot_lambda_min_mum;
    end
    if ~isnan(handles.FFT_plot_lambda_max_mum)
      FFT_plot_lambda_max_mum = handles.FFT_plot_lambda_max_mum;
    end
    
    % set min/max based on frequency/wavelength choice
    if exist('FFT_plot_lambda_min_mum','var')
      if FFT_f_or_lambda==1 % plot as a function of frequency
        FFT_plot_X_max = p.Results.FFT_scalingFactor*(get_c0()./FFT_plot_lambda_min_mum);
      else % plot as a function of wavelength
        FFT_plot_X_min = p.Results.FFT_scalingFactor*FFT_plot_lambda_min_mum;
      end
    end
    if exist('FFT_plot_lambda_max_mum','var')
      if FFT_f_or_lambda==1 % plot as a function of frequency
        FFT_plot_X_min = p.Results.FFT_scalingFactor*(get_c0()./FFT_plot_lambda_max_mum);
      else % plot as a function of wavelength
        FFT_plot_X_max = p.Results.FFT_scalingFactor*FFT_plot_lambda_max_mum;
      end
    end

    % set the defined ranges
    axis([FFT_plot_X_min, FFT_plot_X_max, FFT_plot_Y_min, FFT_plot_Y_max]);

  end

  disp(['DATA INFO: maximums at = ',num2str(X(idx_max))]);

  if p.Results.DoAnalysis
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % peak detection
    % TODO: Manual peak selection GUI...
    aver = sum(Y)/length(Y);
    delta = (max(Y)-aver)/9;
   
    if (delta<=0)
      disp(['ERROR delta<=0 : ',num2str(delta)]);
      return;
    end

    peaks_array = peakdet(Y, delta, X);
    if (handles.verbosity>2)
      peaks_array
    end
    
    wavelength_nm = zeros(1,size(peaks_array,1));
    Q_lorentz = zeros(1,size(peaks_array,1));
    Q_harminv_local = zeros(1,size(peaks_array,1));
    Q_harminv_global = zeros(1,size(peaks_array,1));

    %closestInd(Y,peaks_array(1,3))
    %closestInd(Y,peaks_array(2,3))
    %closestInd(Y,peaks_array(3,3))
    %closestInd(Y,peaks_array(4,3))
    
    if ~handles.plotNothing
      hold on;
    end

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    [ probefile_folder, probefile_basename, probefile_ext ] = fileparts(probe_filename);
    [ probefile_folder_folder, probefile_folder_basename ] = fileparts(probefile_folder);

    harminv_dir = fullfile( probefile_folder, 'harminv' );
    if ~(exist(harminv_dir,'dir'))
      mkdir(harminv_dir); 
    end
    
    %%%
    % set up filenames
    harminv_basepath = [ harminv_dir, filesep, probefile_basename,'_',handles.header{selected_column} ];
    harminvDataFile = [ harminv_basepath, '.harminv.stdin.txt' ];

    outFile = [ harminv_basepath, '.global.harminv.stdout.txt' ];
    outFile_local = [ harminv_basepath, '.local.harminv.stdout.txt' ];

    cmdFile = [ harminv_basepath, '.global.harminv.cmd.txt' ];
    cmdFile_local = [ harminv_basepath, '.local.harminv.cmd.txt' ];
    
    parametersFile = [ harminv_basepath, '.global.harminv.selection.txt' ];
    parametersFile2 = [ harminv_basepath, '.global.harminv.selection2.txt' ];
    parametersFile_local = [ harminv_basepath, '.local.harminv.selection.txt' ]; % NOTE: Unused at the moment. Should be removed or implemented...
    %%%

    if handles.computeHarminvGlobal
    
      % convert from frequency to wavelength if required
      if strcmpi(validatestring(p.Results.harminv_range_type, {'frequency','wavelength'}), 'frequency')
        harminv_range_wavelength(1) = get_c0() ./ p.Results.harminv_range(2);
        harminv_range_wavelength(2) = get_c0() ./ p.Results.harminv_range(1);
      else
        harminv_range_wavelength = p.Results.harminv_range;
      end
      
      % TODO: save the harminv range in the filenames?
      if isnan(harminv_range_wavelength(1))
        harminv_lambdaLow_mum_used = xmin_global*1e-3;
      else
        harminv_lambdaLow_mum_used = harminv_range_wavelength(1);
      end
      if isnan(harminv_range_wavelength(2))
        harminv_lambdaHigh_mum_used = xmax_global*1e-3;
      else
        harminv_lambdaHigh_mum_used = harminv_range_wavelength(2);
      end

      tic;
      disp('Generating harminv input file...');
      fid = fopen(harminvDataFile,'w+');
      %fprintf(fid,'%2.8e\r\n',handles.data(:,selected_column));
      fprintf(fid,'%2.8e\r\n',data_time_domain);
      fclose(fid);
      disp('...done')
      toc;
      
      if (handles.verbosity>1)
        disp('===> Computing global harminv:');
      end
      tic;
      disp('Running harminv...');
      [ status, lambdaH_mum, Q, outFile, err, minErrInd, frequency, decay_constant, amplitude, phase ] = doHarminv(harminvDataFile, dt_mus, harminv_lambdaLow_mum_used, harminv_lambdaHigh_mum_used, outFile, cmdFile);
      disp('...done')
      toc;
      if ( status == 0 )
        if ( length(Q) ~= 0 )
          % calculate time-domain fit based on harminv output
          harminv_time = zeros(size(time_mus));
          %harminv_fig = figure(); hold on;
          for i=1:length(frequency)
            if (handles.verbosity>1)
              disp([num2str(frequency(i)),', ', num2str(decay_constant(i)),', ', num2str(Q(i)),', ', num2str(amplitude(i)),', ', num2str(phase(i)),', ', num2str(err(i))]);
            end
            %harminv_time = harminv_time + amplitude(i)*sin(2*pi*frequency(i)*time_mus+phase(i)).*exp(-decay_constant(i)*time_mus);
            harminv_time = harminv_time + amplitude(i)*cos(-2*pi*frequency(i).*time_mus+phase(i)).*exp(decay_constant(i).*time_mus);
            %plot(time_mus, amplitude(i)*exp(-decay_constant(i).*time_mus));
          end
          %plot(time_mus,harminv_time);
          
          % go back to the regular programming
          %figure(fig);
          
          lambdaH_nm = lambdaH_mum*1e3;
          
          rel=1./err; rel=rel/max(rel)*max(Q);
          
          fid = fopen(parametersFile,'w+');
          fprintf(fid,'PeakNo\tFrequency(Hz)\tWavelength(nm)\tQFactor\tAmplitude\terror\tdecay_constant\tphase\r\n');
          if size(peaks_array,1) >= 1
            for n=1:size(peaks_array,1)
              % TODO: CRITICAL!!!: Look around for close peaks with lower error
              disp(['=====>peaks_array(', num2str(n), ',1) = ', num2str(peaks_array(n, 1))]);
              [indS, val] = closestInd(lambdaH_nm, peaks_array(n, 1));
              if size(indS,1) ~= 1
                disp('WARNING: size(indS) ~= 1. Taking indS(1).');
                indS = indS(1);
              end
              Q_harminv_global(n) = Q(indS);
              peakWaveLength_nm = peaks_array(n,1);
              Frequency_Hz = get_c0()/peakWaveLength_nm*1e9;
              fprintf(fid,'%i\t%2.8g\t%2.11g\t%2.8g\t%g\t%g\t%g\t%g\r\n', n, Frequency_Hz, peakWaveLength_nm, Q(indS), amplitude(indS), err(indS), decay_constant(indS), phase(indS));
            end
          else
            disp('WARNING: No peaks found!');
          end
          fclose(fid);
        else
          warning('harminv was unable to find peaks in the specified frequency range.');
        end
      else
        warning('harminv command failed.');
      end
    end % end of if handles.computeHarminvGlobal
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    if (handles.verbosity>1)
      disp('===> Looping through peaks:');
    end
    
    for n = 1:size(peaks_array,1)
      if handles.peakStars
        if ~handles.plotNothing
          % plot little stars on detected peaks
          if FFT_f_or_lambda==1 % plot as a function of frequency
            plot(p.Results.FFT_scalingFactor*(get_c0()./(1e-3*peaks_array(n,1))), peaks_array(n,2), 'r*');
          else % plot as a function of wavelength
            plot(p.Results.FFT_scalingFactor*1e-3*peaks_array(n,1), peaks_array(n,2), 'r*');
          end
          %plot(peaks_array(n,3),Y(closestInd(X,peaks_array(n,3))),'g*');
          %plot(peaks_array(n,4),Y(closestInd(X,peaks_array(n,4))),'b*');
        end
      end
      [indS,val] = closestInd(X,peaks_array(n,1));
      peakWaveLength = peaks_array(n,1);
      peakValue = peaks_array(n,2);
      
      %%%%%%%%%%%%
      % plot lorentz fit
      x = peaks_array(n,1);
      xmin = peaks_array(n,4);
      xmax = peaks_array(n,3);
      if handles.computeLorentz
        [Q, vStart, vEnd] = fitLorentzian(X,Y,xmin,xmax);
        if plotLorentzFit
          if ~handles.plotNothing
            plot(linspace(xmin,xmax,100),lorentz(vEnd,linspace(xmin,xmax,100)),'r-');
          end
        end
      else
        Q = -1;
      end
      wavelength_nm(n) = peakWaveLength;
      Q_lorentz(n) = Q;
      %%%%%%%%%%%%
      
      if handles.computeHarminvLocal
        Qfactor_harminv = getQfactor_harminv(x, harminvDataFile, dt_mus, xmin, xmax, outFile_local, cmdFile_local);
      else
        Qfactor_harminv = -1;
      end
      
      if size(Qfactor_harminv,1)>0
        Q_harminv_local(n) = Qfactor_harminv;
        
        Q1 = ['Q_L=',num2str(Q_lorentz(n))];
        Q2 = ['Q_{Hl}=',num2str(Q_harminv_local(n))];
        %Q3 = ['Q_{Hg}=',num2str(Q_harminv_global(n))];
        %disp('=================================================')
        %Q_harminv_global(n)
        %disp('=================================================')
        Q3 = ['Q = ',num2str(Q_harminv_global(n))];
        
        if handles.Qtext
          if ~handles.plotNothing
            %text(peakWaveLength, peakValue, {Q1;Q2;Q3}, 'FontSize', 8);
            if FFT_f_or_lambda==1 % plot as a function of frequency
              text(p.Results.FFT_scalingFactor*(get_c0()./(1e-3*peakWaveLength)), peakValue, {Q3}, 'FontSize', 8);
            else % plot as a function of wavelength
              text(p.Results.FFT_scalingFactor*1e-3*peakWaveLength, peakValue, {Q3}, 'FontSize', 8);
            end
            fprintf(1, 'peakWaveLength = %d ; Q = %d\n', peakWaveLength, Q_harminv_global(n));
          end
        end
        
        %text(peakWaveLength, peakValue, {Q1}, 'FontSize', 8);
      end

      %text(peakWaveLength, peakValue + 0*font_size, );
      %text(peakWaveLength, peakValue + 1*font_size, ,'FontSize',font_size;
      %text(peakWaveLength, peakValue + 2*font_size, ,'FontSize',font_size);
      
      %% Write peaks to a text file.
      %Frequency_Hz = get_c0()/peakWaveLength*1e9;
      %fprintf(fid,'%i\t%2.8g\t%2.11g\t%2.8g\r\n',n,Frequency_Hz,peakWaveLength,Q(indS));
      %disp(Frequency_Hz*10^-6)
      %frequency_struct.PeakNo{end+1} = 
      %frequency_struct.Frequency_Hz{end+1} = 
      %frequency_struct.Wavelength_nm{end+1} = 
      %frequency_struct.QFactor = 
      %frequency_struct_array = 

    end % end of loop through peaks

  end % analysis end
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %[Q, vStart, vEnd] = fitLorentzian(X,Y,xmin,xmax);
  %vEnd
  
  %wavelength_nm(n) = peakWaveLength;
  %Q_lorentz(n) = Q;
  
  %%figure
  %plot(linspace(xmin,xmax,100),lorentz(vStart,linspace(xmin,xmax,100)),'r-');
  %%figure
  %plot(linspace(xmin,xmax,100),lorentz(vEnd,linspace(xmin,xmax,100)),'g-');

  %N=10000; xmin=778; xmax=784; Q=112970; y0=0; x0=780.8162; FWHM=x0/Q; A = 0.5*FWHM*(pi*(2.5*1e6-y0)); plot(linspace(xmin,xmax,N),lorentz([x0, y0, A, FWHM],linspace(xmin,xmax,N)),'r-');

  if ~handles.plotNothing
    if handles.autosave == 1
      if length(handles.imageSaveBasename) <= 0
        handles.imageSaveBasename = [dirname(probe_filename), filesep, basename, '_', char(data_name)];
      end
      
      disp(['Saving figure as ', handles.imageSaveBasename, '.png + .fig']);
      saveas_fig_and_png(fig, handles.imageSaveBasename);
      
%        set(fig, 'Position', get(0,'Screensize')); % Maximize figure.
%        disp(['Saving figure as ', handles.imageSaveBasename, '.png']);
%        print(fig,'-dpng','-r300',[handles.imageSaveBasename, '.png']);
%  
%        disp(['Saving figure as ', handles.imageSaveBasename, '.fig']);
%        saveas(gcf,[handles.imageSaveBasename, '.fig'],'fig');

      %print(fig,'-depsc','-r1500',imageSaveBasename);
      %saveas(gcf,[imageSaveBasename,'.png'],'png');
    end
  end

  if (handles.verbosity>3)
    handles
  end

end
