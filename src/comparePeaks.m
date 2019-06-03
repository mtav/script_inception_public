function comparePeaks(SRCDIR,X_AXIS_TYPE,probe_col)
  % compares FFT peaks of all pillars
  
  if exist('SRCDIR','var')==0
    disp('SRCDIR not given');
      SRCDIR = uigetdir('D:\DATA\Andrew_pillars','SRCDIR');
  end
  if ~(exist(SRCDIR,'dir'))
    disp('dir not found');
    return;
  end
  
  if exist('probe_col','var')==0
    disp('probe_col not given');
    probe_col = 2;
  end

  if exist('X_AXIS_TYPE','var')==0
    disp('X_AXIS_TYPE not given');
    X_AXIS_TYPE = 0;
  end
  
  lambda_min = 700;%nm
  lambda_max = 950;%nm
  
  freq_min = 10^3*get_c0()/lambda_max;%MHz
  freq_max = 10^3*get_c0()/lambda_min;%MHz

  nGaAs=3.521;%no unit
  nAlGaAs=2.973;%no unit
  n0 = 1; % air refractive index
  Lcav = 253; % (nm)
  
  % freq in MHz
  % lambda_vec in nm
  function [ freq, lambda_vec, fft_pow ] = getFFT(filename)
    disp(['processing ',filename]);
    [header, data] = readPrnFile(filename);
    dt = 1e-12*(data(2,1)-data(1,1));  % Normally the data in probe file is in values of 1e*18 seconds
    % disp('	fourier transform start');
    [cFFT_output, lambda_vec, freq] = calcFFT(data(:,probe_col),dt, 2^19);
    lambda_vec = 1e3*lambda_vec; % to get lambda in nm
    % disp('	fourier transform end');

    %calculate magnitude of fft
    fft_mag = abs(cFFT_output);
    %calculate power of fft
    fft_pow = cFFT_output.* conj(cFFT_output);		
  end

  function processProbe(fulldir,probe_name)
    [ folder, basename, ext ] = fileparts(fulldir);
    probe = [fulldir,filesep,probe_name];
    [ freq, lambda_vec, y ] = getFFT(probe);
    
    if X_AXIS_TYPE == 0
      x = lambda_vec;
    else
      x = freq;
    end

    % all_plots = [ all_plots, x, y ];
    
    infos = regexp(basename, '_', 'split');
    pillar_type = infos(2);
    n_type = str2num(char(infos(3)));
    radius = str2num(char(infos(4)))/10;

    % Oh yeah, add {' '} to get spaces! That is soooo intuitive... :/
    title = strcat(pillar_type,{' '},num2str(n_type),{' '},num2str(radius),{' '},probe_name);
    % all_titles = [ all_titles; title];

    counter = counter + 1;
    y = (y-min(y))/(max(y)-min(y)) + (counter-1);
    plot(x,y);
    if X_AXIS_TYPE == 0
      xlabel('Wavelength (nm)');
      text(900,(counter-1)+0.5,title);
    else
      xlabel('Frequency (MHz)');
      text(get_c0()/(900*10^(-3)),(counter-1)+0.5,title);
    end
    ylabel('Fourier transform (arbitrary units)');
    hold on;
    
  end
  
  function processDir(fulldir)
    fprintf('===>Processing %s\n',fulldir);
    processProbe(fulldir,'p62id.prn');
    processProbe(fulldir,'p71id.prn');
    processProbe(fulldir,'p80id.prn');
    processProbe(fulldir,'p89id.prn');
  end
  
  function addPillars(pillar_type)
    for r=1:0.5:5
      close all;
      counter = 0;
      figure;
      for n_type=0:1
        dirname = strcat('pillar_',pillar_type,'_',num2str(n_type),'_',num2str(10*r));
        % disp(dirname);
        processDir([SRCDIR,filesep,dirname]);
      end
      
      [ vert_E, vert_lambda ] = resonanceEnergy(nGaAs, nAlGaAs, n0, Lcav, r);
      vert_freq = ((vert_E*10^(-3)*get_e())/get_h())*10^(-6); % vert_E in meV^-3, vert_freq in MHz
      if X_AXIS_TYPE == 0
        axis([lambda_min,lambda_max,0,counter]);
        line([vert_lambda ; vert_lambda],[0 ; counter],'Color','r','LineStyle','--');
      else
        axis([freq_min,freq_max,0,counter]);
        line([vert_freq ; vert_freq],[0 ; counter],'Color','r','LineStyle','--');
      end

      
      saveas(gcf,[SRCDIR, filesep, strcat('pillar_',pillar_type,'_',num2str(10*r)),'.png'],'png');
    end
  end
  
  close all;
  counter = 0;
  % all_plots = [];
  % all_titles = [];
  
  % normal use
  addPillars('M2754');
  addPillars('M3687');
  close all;
  
  % for testing
  % processDir(getinput(5));
  % [ vert_E, vert_lambda ] = resonanceEnergy(nGaAs, nAlGaAs, n0, Lcav, 1);
  % vert_freq = ((vert_E*10^(-3)*get_e())/get_h())*10^(-6); % vert_E in meV^-3, vert_freq in MHz
  % if X_AXIS_TYPE == 0
    % axis([lambda_min,lambda_max,0,4]);
    % line([vert_lambda ; vert_lambda],[0 ; 4],'Color','r','LineStyle','--');
  % else
    % axis([freq_min,freq_max,0,4]);
    % line([vert_freq ; vert_freq],[0 ; 4],'Color','r','LineStyle','--');
  % end
  
  % N=size(all_plots,2)/2;
  % title_array = cellstr(all_titles);
  % for i=1:N
    % x = all_plots(:,1+2*(i-1)+0);
    % y = all_plots(:,1+2*(i-1)+1);
    % y = (y-min(y))/(max(y)-min(y)) + (i-1);
    % plot(x,y);
    % text(900,(i-1)+0.5,title_array(i));
    % hold on;
  % end
  
end
