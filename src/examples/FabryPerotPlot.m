% Example usage of the FabryPerot() function to create a measurement-like transmittance plot:

% input parameters
lambda = linspace(0.75, 1.7, 100);
n_outside = 1;
n_inside = 3;
thickness = 1;
incidence_angle = linspace(-pi/4, pi/4, 100);

% create plot
[X, Y] = meshgrid(incidence_angle, lambda);
[reflectance, transmittance] = FabryPerot(Y, n_outside, n_inside, thickness, X);
surf(X, Y, transmittance);
view(0,90);

% create labels
title(['transmittance for thickness=',num2str(thickness),' n=',num2str(n_inside)]);
xlabel('incidence angle (radians)');
ylabel('wavelength (\mum)');

axis([min(incidence_angle), max(incidence_angle), min(lambda), max(lambda)]);

figure;
hold on;
for m = 1:10
  plot(incidence_angle , 2*n_inside*thickness*cos(incidence_angle)/m);
end
axis([min(incidence_angle), max(incidence_angle), min(lambda), max(lambda)]);
