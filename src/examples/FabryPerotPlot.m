% Example usage of the FabryPerot() function to create a measurement-like transmittance plot:

% input parameters
lambda = linspace(0.75, 1.7, 100);
n_outside = 2;
n_inside = 3;
thickness = 1;
incidence_angle = linspace(-pi/4, pi/4, 100);

% create plot
[X, Y] = meshgrid(incidence_angle, lambda);
[reflectance, transmittance] = FabryPerot(Y, n_outside, n_inside, thickness, X);
% surf(X, Y, transmittance);
% view(0,90);
figure();

subplot(1,2,1);
imagesc(incidence_angle, lambda, reflectance);
colorbar();
set(gca,'Ydir','normal');
title('reflectance');
xlabel('incidence angle (radians)');
ylabel('wavelength (\mum)');
axis([min(incidence_angle), max(incidence_angle), min(lambda), max(lambda)]);

subplot(1,2,2);
imagesc(incidence_angle, lambda, transmittance);
colorbar();
set(gca,'Ydir','normal');
title('transmittance');
xlabel('incidence angle (radians)');
ylabel('wavelength (\mum)');
axis([min(incidence_angle), max(incidence_angle), min(lambda), max(lambda)]);

subplot(1,2,1);
hold on;
for m = 1:10
  plot(incidence_angle , FabryPerot_bands(n_inside, thickness, incidence_angle, m), 'k-');
  plot(incidence_angle , FabryPerot_bands(n_inside, thickness, incidence_angle, m-1/2), 'k--');
end
axis([min(incidence_angle), max(incidence_angle), min(lambda), max(lambda)]);

subplot(1,2,2);
hold on;
for m = 1:10
  plot(incidence_angle , FabryPerot_bands(n_inside, thickness, incidence_angle, m), 'k-');
  plot(incidence_angle , FabryPerot_bands(n_inside, thickness, incidence_angle, m-1/2), 'k--');
end
axis([min(incidence_angle), max(incidence_angle), min(lambda), max(lambda)]);

sgtitle(['thickness=',num2str(thickness),' n_{inside}=',num2str(n_inside), ' n_{outside}=',num2str(n_outside)]);
