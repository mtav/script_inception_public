function transmission_v2()
  close all;
  
  figure;
  hold on;

  a = 1;
  f_scaling = 1;

  reference_file = 'bend0.dat';
  geometry_file = 'bend.dat';
  [ frequency, transmission_normalized, reflection_normalized, loss ] = getNormalizedTRLvalues(reference_file, geometry_file);
  plot(f_scaling*frequency,transmission_normalized,'bo');
  plot(f_scaling*frequency,reflection_normalized,'ro');
  plot(f_scaling*frequency,loss,'k-');

%    reference_file = 'bend0-big.dat';
%    geometry_file = 'bend-big.dat';
%    [ frequency, transmission_normalized, reflection_normalized, loss ] = getNormalizedTRLvalues(reference_file, geometry_file);
%    plot(frequency,transmission_normalized,'b:'); plot(frequency,reflection_normalized,'r:'); plot(frequency,loss,'k:');

  %  min(transmission_normalized_big)
  %  max(transmission_normalized_big)
  % axis([0.1,0.2,0,1]);

  % pulse center frequency
  fcen = 0.222222222222222
  
  % pulse width (in frequency)
  df = 0.222222222222222

  % number of frequencies at which to compute flux
  nfreq = 500

  % width of waveguide in mum
  wx = 1.125

  n_block = 2

  fn = linspace(fcen-0.5*df, fcen+0.5*df, nfreq); % normalized frequency, i.e. (real f) / (c0/a)
  lambda = a./fn; % in mum lambda = c0/f = c0/(fn*c0/a) = a/fn
  [reflectance,transmittance] = FabryPerot(lambda, 1, n_block, wx, 0); % lambda and w must be passed in the same unit here!!!

  plot(f_scaling*fn,transmittance,'b-');
  plot(f_scaling*fn,reflectance,'r-');

  title(['Transmission and Reflection for a 1D film with thickness=', num2str(wx),' \mum, n=', num2str(n_block), ', normal incidence'])
  xlabel('frequency')
  ylabel('Transmission and Reflection (no unit)')  
  legend('MEEP transmission','MEEP reflection','MEEP loss','transmission theoretical','reflection theoretical');

%    if inoctave()
%      print -dashed -F:18 -depsc output_octave.eps
%      print -dpng output_octave.png
%    else
%      saveas(gcf, 'output_matlab.png', 'png');
%    end

end
