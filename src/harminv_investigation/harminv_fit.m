function harminv_fit()
  % creates a multimode decay and tries various Q-factor finding methods:
  % 1) envelope fitting
  % 2) harminv
  % 3) lorentz fit of the FFT
  
  %f0 = [30,50,100,1000]
  %Q0 = [20,40,30,2e6]
  %A0 = [10,20,30,40]

  f0 = [100]
  Q0 = [5e2]
  A0 = [40]

  %f0 = [30,50,200,1000]
  %Q0 = [20,40,30,5e3]
  %A0 = [100,20,30,4000]

  dt = 1/(300*max(f0));
  tmin = 0;
  tmax = 15*Q0(1)*1/(min(f0));
  
  disp('=== Creating sample function ===');
  x = tmin:dt:tmax;
  [y,fmin,fmax] = expsine(x, f0, Q0, A0);
  
  orig = figure(); hold on;
  title('raw data');
  plot(x,y,'b.');
  
  %disp('=== Running ringdown FFT fit directly ===')
  %%% FFT for frequency estimation
  %LV = length(y);
  %%P = abs(fft(y)); Ppos=P(1:(round(LV/2)+1));
  %P = fft(y); Ppos=P(1:(round(LV/2)+1));
  %Y = Ppos.* conj(Ppos);
  %faxis = 1/dt*(0:round(LV/2))/LV;
  %peakf=faxis(find(Ppos==max(P(1:(round(LV/2)+1))))); %#ok<FNDSB>
  %directRingdownFFT=figure();
  %%semilogy(faxis,Ppos,'-'); hold on
  %%plot(faxis,Ppos,'-'); hold on
  %plot(faxis,Y,'-'); hold on
  %plot(peakf,max(Ppos),'dr');
  %title('direct ringdown FFT'); xlabel('Frequency [Hz]'); ylabel('Power')
  %fa=axis; text((fa(2)-fa(1))/2,(fa(4)-fa(3))/2,['f_0: ' num2str(peakf,'%.1f') ' Hz']);

  %[Q, vStart, vEnd] = fitLorentzian(faxis,Y,990,1010)

  %disp('=== Running calcFFT fit directly ===')
  %[calcFFT_output, lambda_vec_mum, freq_vec_Mhz] = calcFFT(y,dt, 2^22);
  %% convert lambda to nm
  %lambda_vec_nm = 1e3*lambda_vec_mum;
  %X = lambda_vec_nm;
  %Y = calcFFT_output.* conj(calcFFT_output);
  %directFFT = figure(); hold on;
  %title('direct FFT');
  %plot(X,Y);
  %[Q, vStart, vEnd] = fitLorentzian(X,Y,2.98e8,3.02e8)

  %disp('=== Running ringdown ===')
  %orig_axis = axis();
  %res.trace1.x = x;
  %res.trace1.y = y;
  %res_rd = ringdown(res)
    
  disp('=== Running harminv ===')
  harminvDataFile = '~/tmpHarminvData.txt';
  
  fid = fopen(harminvDataFile,'w+');
  fprintf(fid,'%2.8e\r\n',y);
  fclose(fid);
  
  fmin
  fmax
  lambdaLow = get_c0()/fmax;
  lambdaHigh = get_c0()/fmin;

  [ inFile_dir, inFile_base, inFile_ext ] = fileparts(harminvDataFile)
  outFile = fullfile(inFile_dir, [inFile_base, '.out'])
  cmdFile = fullfile(inFile_dir, [inFile_base, '.cmd'])  
  [ status, lambda, Q, outFile, err, minErrInd, frequency, decay_constant, amplitude, phase ] = doHarminv(harminvDataFile, dt, lambdaLow, lambdaHigh, outFile, cmdFile);
  outFile
  if ( status == 0 )
    if ( length(Q) ~= 0 )
      % calculate time-domain fit based on harminv output
      harminv_time = zeros(size(x));
      %harminv_fig = figure(); hold on;
      figure(orig); hold on;
      for i=1:length(frequency)
        disp([num2str(frequency(i)),', ', num2str(decay_constant(i)),', ', num2str(Q(i)),', ', num2str(amplitude(i)),', ', num2str(phase(i)),', ', num2str(err(i))]);
        %harminv_time = harminv_time + amplitude(i)*sin(2*pi*frequency(i)*x+phase(i)).*exp(-decay_constant(i)*time_mus);
        %harminv_time = harminv_time + amplitude(i)*cos(-2*pi*frequency(i).*x+phase(i)).*exp(decay_constant(i).*x);
        %harminv_time = harminv_time + amplitude(i)*exp(-2*pi*frequency(i).*x+phase(i)).*exp(decay_constant(i).*x);
        harminv_time = harminv_time + amplitude(i) * exp(-1i*(2*pi*frequency(i)*x - phase(i)) - decay_constant(i)*x);
      end
      plot(x,harminv_time,'r');
      plot(x,y,'b.');
      
      ColorSet = varycolor(length(frequency));
      set(gca, 'ColorOrder', ColorSet);
      
      for i=1:length(frequency)
        plot(x, 2*amplitude(i)*exp(-decay_constant(i).*x),'g','LineWidth',10);
      end
      %axis(orig_axis);
    else
      warning('harminv was unable to find peaks in the specified frequency range.');
    end
  else
    warning('harminv command failed.');
  end

  %disp('=== Running plotProbe ===');
  %filename = '~/tmp.prn';
  %probe_col = 2;
  %autosave = false;
  %imageSaveName = '';
  %hide_figures = false;
  
  %fid = fopen(filename,'wt');
  %fprintf(fid,'x\ty\n');
  %fclose(fid);
  %tab = [1e12*x(:),y(:)];
  %save(filename, 'tab', '-ASCII', '-double', '-tabs', '-append');
  %%for k=1:length(x)
    %%fprintf(fid,'%f\t%f\n',1e12*x(k),y(k));
  %%end
  %%fclose(fid);

  %[ wavelength_nm, Q_lorentz, Q_harminv_local, Q_harminv_global ] = plotProbe(filename, probe_col, autosave, imageSaveName, hide_figures)

end
