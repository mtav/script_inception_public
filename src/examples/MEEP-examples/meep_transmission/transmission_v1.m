function transmission_v1()
  close all;
  hold on;

  f_scaling = get_c0()/1e-6;

%    reference_file = 'bend0.dat';
%    geometry_file = 'bend.dat';

  reference_file = 'meep_transmission_1D/bend0.dat';
  geometry_file = 'meep_transmission_1D/bend.dat';

  [ frequency, transmission_normalized, reflection_normalized, loss ] = getNormalizedTRLvalues(reference_file, geometry_file);
  plot(f_scaling*frequency,transmission_normalized,'bo');
  plot(f_scaling*frequency,reflection_normalized,'ro');
  plot(f_scaling*frequency,loss,'k-');
  return

%    reference_file = 'bend0-big.dat';
%    geometry_file = 'bend-big.dat';
%    [ frequency, transmission_normalized, reflection_normalized, loss ] = getNormalizedTRLvalues(reference_file, geometry_file);
%    plot(frequency,transmission_normalized,'b:'); plot(frequency,reflection_normalized,'r:'); plot(frequency,loss,'k:');

  %  min(transmission_normalized_big)
  %  max(transmission_normalized_big)
  % axis([0.1,0.2,0,1]);

  fcen = 1; % pulse center frequency
  df = 2; % pulse width (in frequency)
  nfreq = 500; % number of frequencies at which to compute flux
%    sx = 16; % size of cell in X direction
  w = 1; % width of waveguide

  f = linspace(fcen-0.5*df, fcen+0.5*df, nfreq);
  lambda = 1./f;
  [reflectance,transmittance] = FabryPerot(lambda, 1, sqrt(12), w, 0);

%    hold on;
%    plot(f_scaling*f,transmittance,'b-');
%    plot(f_scaling*f,reflectance,'r-');

%    legend('transmission','reflection','loss', 'transmission big','reflection big','loss big','transmission theoretical','reflection theoretical');
  title(['Transmission and Reflection for a 1D film with thickness=',num2str(w)',' \mum, epsilon=12, normal incidence'])
  xlabel('frequency (Hz)')
  ylabel('Transmission and Reflection (no unit)')  
  legend('MEEP transmission','MEEP reflection','MEEP loss','transmission theoretical','reflection theoretical');

%    if inoctave()
%      print -dashed -F:18 -depsc output_octave.eps
%      print -dpng output_octave.png
%    else
%      saveas(gcf, 'output_matlab.png', 'png');
%    end

end
