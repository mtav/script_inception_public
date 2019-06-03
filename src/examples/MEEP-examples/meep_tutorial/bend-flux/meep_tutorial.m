bend = dlmread('bend.dat',',',0,1);
bend0 = dlmread('bend0.dat',',',0,1);
bend_big = dlmread('bend-big.dat',',',0,1);
bend0_big = dlmread('bend0-big.dat',',',0,1);

frequency = bend(:,1);

transmitted_flux = bend(:,2);
reflected_flux = bend(:,3);
incident_flux = bend0(:,2);

transmitted_flux_big = bend_big(:,2);
reflected_flux_big = bend_big(:,3);
incident_flux_big = bend0_big(:,2);

transmission_normalized = transmitted_flux./incident_flux;
reflection_normalized = -reflected_flux./incident_flux;
transmission_normalized_big = transmitted_flux_big./incident_flux_big;
reflection_normalized_big = -reflected_flux_big./incident_flux_big;

loss = 1 - transmission_normalized - reflection_normalized;
loss_big = 1 - transmission_normalized_big - reflection_normalized_big;

close all; hold on;
plot(frequency,transmission_normalized,'bo-'); plot(frequency,reflection_normalized,'rd-'); plot(frequency,loss,'k-'); legend('transmission','reflection','loss');
plot(frequency,transmission_normalized_big,'b:'); plot(frequency,reflection_normalized_big,'r:'); plot(frequency,loss_big,'k:');
axis([0.1,0.2,0,1]);

if inoctave()
  print -dashed -F:18 -depsc output_octave.eps
  print -dpng output_octave.png
else
  saveas(gcf, 'output_matlab.png', 'png');
end
