function fft_study(f, Fs, N)
  % checking frequency folding


  %f=20;
  dt = 1/Fs;
  t = (0:N-1)*dt;

  dt
  T = 1/f
  tmax = max(t)
  
  %t=linspace(0,1,100);

  s = cos(2*pi*f*t);
  %s = sin(2*pi*f*t);
  %s = exp(i*2*pi*f*t);

  %Fs=1/(t(2)-t(1));
  frange = linspace(0, Fs, N);
  %frange = 0:
  fft_spectrum = fft(s);

  subplot(2,2,1);
  plot(t, real(s));
  subplot(2,2,2);
  plot(t, imag(s));
  subplot(2,2,3);
  plot(frange, real(fft_spectrum))
  subplot(2,2,4);
  plot(frange, imag(fft_spectrum))
end
