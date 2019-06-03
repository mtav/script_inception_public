function [fft_out,lambda,freq] = calcFFT(datain,dt,NFFT)
  % function [fft_out,lambda,freq] = calcFFT(datain,dt,NFFT)
  % datain = datain value in time domain
  % dt = timestep in time domain
  % NFFT = double the number of points you want in the output
  % fft_out = magnitude 
  % freq = frequency
  % lambda = wavelength = c0/freq
  % TODO: disable use of NFFT wherever it is still used.

  N = length(datain);
  Nhalf = ceil(N/2);
  NFFT = 2*Nhalf;
  
  freq_full = linspace(0, ((NFFT-1)/NFFT)*(1/dt), NFFT);
  fft_out_full = fft(datain, NFFT);

  % We skip the first frequency to avoid divide by 0 later.
  % TODO: Fix outside code instead to check for Inf value in lambda range?
  freq = freq_full(2:Nhalf);
  fft_out = fft_out_full(2:Nhalf);

  % calculate wavelength for convenience
  lambda = get_c0()./freq;

  % make sure all vectors are column vectors
  fft_out = fft_out(:);
  lambda = lambda(:);
  freq = freq(:);

end
