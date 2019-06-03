function getResonanceFrequencies(probefile, colnumP)
  % writes the resonance frequencies of probefile/column into multiple files and returns frequency_struct
  
  frequency_struct = struct('PeakNo', {}, 'Frequency_Hz', {}, 'Wavelength_nm', {}, 'QFactor', {});

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  computeHarminv = 1;

  clf;
  
  % read the data
  [header, data] = readPrnFile(probefile);
  if size(data,1)<=2
    return
  end
  %header
  %data

  % parts to build filenames
  [ probefile_folder, probefile_basename, probefile_ext ] = fileparts(probefile)
  [ probefile_folder_folder, probefile_folder_basename ] = fileparts(probefile_folder)
  harminv_dir = fullfile( probefile_folder, 'harminv' );
  %harminv_dir
  %filesep
  %probefile_basename
  %'_'
  %colnumP
  %header
  %header{colnumP}
  harminv_basepath = [ harminv_dir, filesep, probefile_basename,'_',header{colnumP} ];
  title_base = [ fullfile(probefile_folder_basename, probefile_basename), probefile_ext, ' ', header{colnumP} ];
  
  if ~(exist(harminv_dir,'dir'))
    harminv_dir
    mkdir(harminv_dir); 
  end
  
  % file/dir names
  filename_probe_time_png =   [ harminv_basepath, '.png' ];
  filename_probe_time_fig =   [ harminv_basepath, '.fig' ];
  filename_probe_freq_png =   [ harminv_basepath, '_probeFFT.png' ];
  filename_probe_freq_fig =   [ harminv_basepath, '_probeFFT.fig' ];
  filename_harminv_freq_png = [ harminv_basepath, '_harminv.out','.png' ];
  filename_harminv_freq_fig = [ harminv_basepath, '_harminv.out','.fig' ];
  outfileName =               [ harminv_basepath, '_harminv.out' ];
  harminvDataFile =           [ harminv_basepath, '_harminv.txt' ];
  parametersFile =            [ harminv_basepath, '_parameters.txt' ];

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  figure(1); clf;
  plot(data(:,1)*1e-9,data(:,colnumP));

  title(title_base,'Interpreter','none');
  xlabel('time (ns)');
  
  % save time domain plot from probe
  saveas(gcf,filename_probe_time_png,'png');disp(['Saved as ',filename_probe_time_png]);
  saveas(gcf,filename_probe_time_fig,'fig');disp(['Saved as ',filename_probe_time_fig]);
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  dt_mus = 1e-12*(data(2,1)-data(1,1));  % Normally the data in probe file is in values of 1e*18 seconds
  [Y,lambda_mum] = bFFT(data(:,colnumP),dt_mus);
  Mag=2*abs(Y);
  
  aver=sum(Mag)/length(Mag);
  delta=(max(Mag)-aver)/3;
 
  if (delta<0)
    return;
  end

  peaks=peakdet(Mag, delta/3,lambda_mum);
  wavelength_nm=1e3*lambda_mum;
  
  figure(2); clf; hold off;
  plot(wavelength_nm, Mag);
  xlim(1e3*[0.8*min(peaks(:,1)),1.2*max(peaks(:,1))]);
  
  title([ title_base,' Spectrum at Timestep:',num2str(length(data))],'Interpreter','none');
  xlabel('Wavelength (nm)');
  ylabel('Mag');

  if computeHarminv

    lambdaLow = 0.4; %0.62; %set min lamda  0.90
    lambdaHigh = 0.8; %set max lamda  0.98

    fid=fopen(harminvDataFile,'w+');
    fprintf(fid,'%2.8e\r\n',data(:,colnumP));
    fclose(fid);
    
    [status, lambdaH,Q,outFile,err,minErrInd] = doHarminv(harminvDataFile,dt_mus,lambdaLow,lambdaHigh);
    
    figure(3); clf
    plot(lambdaH,Q,'r','LineWidth',2);
    hold on
    rel=1./err; rel=rel/max(rel)*max(Q);
    plot(lambdaH,rel,':')
    hold off
    xlim([lambdaLow lambdaHigh])
    
    if length(Q)
      ylim(sort([0 1.1*max(Q)]))
    end
  
    title(title_base,'interpreter','none')
    xlabel('wavelength(um)')
    ylabel('Q Factor')
    
    % save frequency domain plot from harminv
    saveas(gcf,[outFile,'.png'],'png');disp(['Saved as ',[outFile,'.png']]);
    saveas(gcf,[outFile,'.fig'],'fig');disp(['Saved as ',[outFile,'.fig']]);
    
    fid = fopen(parametersFile,'w+');
    fprintf(fid,'PeakNo\tFrequency(Hz)\tWavelength(nm)\tQFactor\t\r\n');

    for n=1:size(peaks,1)
      figure(2); hold on;
      plot(1e3*peaks(n,1),peaks(n,2),'r*')
      [indS,val]=closestInd(lambdaH,peaks(n,1));
      peakWaveLength=1e3*peaks(n,1);
      peakValue=peaks(n,2);
      text(peakWaveLength,peakValue,['Q=',num2str(Q(indS))],'FontSize',16);
      %% Write peaks to a text file.
      Frequency_Hz = get_c0()/peakWaveLength*1e9;
      fprintf(fid,'%i\t%2.8g\t%2.11g\t%2.8g\r\n',n,Frequency_Hz,peakWaveLength,Q(indS));
      disp(Frequency_Hz*10^-6)
      %frequency_struct.PeakNo{end+1} = 
      %frequency_struct.Frequency_Hz{end+1} = 
      %frequency_struct.Wavelength_nm{end+1} = 
      %frequency_struct.QFactor = 
      %frequency_struct_array = 

    end
      
    fclose(fid);     
  end % end of if computeHarminv

  figure(2);
  % save frequency domain plot from probe
  saveas(gcf,filename_probe_freq_png,'png');disp(['Saved as ',filename_probe_freq_png]);
  saveas(gcf,filename_probe_freq_fig,'fig');disp(['Saved as ',filename_probe_freq_fig]);
  disp('DONE')
end
