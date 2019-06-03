function getResonanceFrequencies2(filename, probe_col, parametersFile)
  [ folder, basename, ext ] = fileparts(filename);
  [ geoname_folder, geoname_basename ] = fileparts(folder);

  % read the PRN file
  [header, data] = readPrnFile(filename);
  data_name = header(probe_col);

  time_mus = 1e-12*data(:,1);
  data_time_domain = data(:,probe_col);

  % calculate timestep
  % WARNING: The timestep is considered to be constant here!!!
  dt_mus = time_mus(2)-time_mus(1);  % data(*,1) being in 10^-18 s (because input frequency is in 10^6 Hz), dt is in 10^-18 s/1e-12 = 10^-6 s

  % calculate the FFT
  % (with NFFT = double the number of points you want in the output = 2^19)
  % (probe_col = whatever column you want from the time probe file, i.e. Ex,Ey,etc)
  [calcFFT_output, lambda_vec_mum, freq_vec_Mhz] = calcFFT(data_time_domain,dt_mus, 2^19);

  % convert lambda to nm
  lambda_vec_nm = 1e3*lambda_vec_mum;

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  disp(['DATA INFO: min(data_time_domain) = ',num2str(min(data_time_domain))]);
  disp(['DATA INFO: max(data_time_domain) = ',num2str(max(data_time_domain))]);
  if min(data_time_domain)==0 & max(data_time_domain)==0
    disp('WARNING: empty data');
    return;
  end

  ViewingWindowThreshold = 1e-3; % stop plotting when the remaining values are under this ViewingWindowThreshold*max(Y)
  ymin = min(data_time_domain);
  ymax = max(data_time_domain);
  for idx_max=length(data_time_domain):-1:1;
    if data_time_domain(idx_max)>ViewingWindowThreshold*ymax;
      break;
    end;
  end;
  xmin = time_mus(1);
  xmax = time_mus(idx_max);
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % define X and Y for the fitting (Y = power)
  X = lambda_vec_nm;
  Y = calcFFT_output.* conj(calcFFT_output);

  disp(['DATA INFO: min(Y) = ',num2str(min(Y))]);
  disp(['DATA INFO: max(Y) = ',num2str(max(Y))]);
  if min(Y)==0 & max(Y)==0
    disp('WARNING: empty data');
    return;
  end

  idx_max = find(Y==max(Y));
  ViewingWindowSize = 200;
  xmin_global = X(idx_max(1)) - ViewingWindowSize;
  xmax_global = X(idx_max(length(idx_max))) + ViewingWindowSize;

  disp(['DATA INFO: maximums at = ',num2str(X(idx_max))]);

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % peak detection
  aver = sum(Y)/length(Y);
  delta = (max(Y)-aver)/9;
 
  if (delta<0)
    disp(['ERROR delta<0 : ',delta])
    return;
  end

  peaks = peakdet(Y, delta, X);
  peaks
  
  Q_lorentz = zeros(1,size(peaks,1));
  Q_harminv_local = zeros(1,size(peaks,1));
  Q_harminv_global = zeros(1,size(peaks,1));

  %closestInd(Y,peaks(1,3))
  %closestInd(Y,peaks(2,3))
  %closestInd(Y,peaks(3,3))
  %closestInd(Y,peaks(4,3))
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  filename
  [ probefile_folder, probefile_basename, probefile_ext ] = fileparts(filename)
  [ probefile_folder_folder, probefile_folder_basename ] = fileparts(probefile_folder)
  harminv_dir = fullfile( probefile_folder, 'harminv' );
  
  if ~(exist(harminv_dir,'dir'))
    harminv_dir
    mkdir(harminv_dir); 
  end
  
  harminv_basepath = [ harminv_dir, filesep, probefile_basename,'_',header{probe_col} ];
  outfileName =               [ harminv_basepath, '_harminv.out' ];
  harminvDataFile =           [ harminv_basepath, '_harminv.txt' ];

  computeHarminv = 1;
  if computeHarminv
    lambdaLow_mum = xmin_global*1e-3;
    lambdaHigh_mum = xmax_global*1e-3;

    disp(['harminvDataFile = ', harminvDataFile])
    fid = fopen(harminvDataFile,'w+');
    fprintf(fid,'%2.8e\r\n',data(:,probe_col));
    fclose(fid);
    
    [status, lambdaH_mum,Q,outFile,err,minErrInd] = doHarminv(harminvDataFile,dt_mus,lambdaLow_mum,lambdaHigh_mum);
    lambdaH_nm = lambdaH_mum*1e3;
    
    rel=1./err; rel=rel/max(rel)*max(Q);
    
    disp(['parametersFile = ',parametersFile])
    fid = fopen(parametersFile,'w+');
    fprintf(fid,'PeakNo\tFrequency(Hz)\tWavelength(nm)\tQFactor\t\r\n');
    for n=1:size(peaks,1)
      [indS,val]=closestInd(lambdaH_nm,peaks(n,1));
      Q_harminv_global(n) = Q(indS);
      peakWaveLength_nm = peaks(n,1);
      Frequency_Hz = get_c0()/peakWaveLength_nm*1e9;
      fprintf(fid,'%i\t%2.8g\t%2.11g\t%2.8g\r\n',n,Frequency_Hz,peakWaveLength_nm,Q(indS));
    end
    fclose(fid);
  end % end of if computeHarminv
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  for n=1:size(peaks,1)
    [indS,val] = closestInd(X,peaks(n,1));
    peakWaveLength = peaks(n,1);
    peakValue = peaks(n,2);
    
    x = peaks(n,1);
    xmin = peaks(n,4);
    xmax = peaks(n,3);
    [Q, vStart, vEnd] = fitLorentzian(X,Y,xmin,xmax);
    
    Q_lorentz(n) = Q;
    
    Q_harminv_local(n) = getQfactor_harminv(x, harminvDataFile, dt_mus, xmin, xmax);
    
    Q1 = ['Q_L=',num2str(Q_lorentz(n))];
    Q2 = ['Q_{Hl}=',num2str(Q_harminv_local(n))];
    Q3 = ['Q_{Hg}=',num2str(Q_harminv_global(n))];
    
  end
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
end
