% Example usage of the FabryPerot() function to create a measurement-like transmittance plot:

% input parameters
prompt = {...
    'Thickness (um):',...
    'n_inside:',...
    'n_outside:',...
    'Lambda min (um):',...
    'Lambda max (um):',...
    'Theta min (degrees):',...
    'Theta max (degrees):',...
    'Reverse Y axis:',...
    };
dlgtitle = 'Input parameters';
dims = [1 35];
definput = {'0.7','1.5', '1', '0.4', '1.0', '-45', '45', '0'};
answer = inputdlg(prompt,dlgtitle,dims,definput);

if isempty(answer)
    return
end

thickness = str2num(answer{1});
n_inside = str2num(answer{2});
n_outside = str2num(answer{3});
lambda = linspace(str2num(answer{4}), str2num(answer{5}), 100);
incidence_angle_deg = linspace(str2num(answer{6}), str2num(answer{7}), 100);
reverse_y_axis = str2num(answer{8});

% lambda(1)
% lambda(end)
% incidence_angle_deg(1)
% incidence_angle_deg(end)

incidence_angle_rad = deg2rad(incidence_angle_deg);

% thickness = 0.7;
% n_inside = 1.5;
% n_outside = 1;
% lambda = linspace(0.4, 1.0, 100);
% incidence_angle_rad = linspace(-pi/4, pi/4, 100);
% incidence_angle_deg = rad2deg(incidence_angle_rad);

% create plot
[X, Y] = meshgrid(incidence_angle_rad, lambda);
[reflectance, transmittance] = FabryPerot(Y, n_outside, n_inside, thickness, X);
% surf(X, Y, transmittance);
% view(0,90);
figure();

subplot(1,2,1);
imagesc(incidence_angle_deg, lambda, reflectance);
colorbar();
set(gca,'Ydir','normal');
title('reflectance');
xlabel('incidence angle (degrees)');
ylabel('wavelength (\mum)');
axis([min(incidence_angle_deg), max(incidence_angle_deg), min(lambda), max(lambda)]);
if reverse_y_axis~=0
    set(gca, 'YDir','reverse');
end

subplot(1,2,2);
imagesc(incidence_angle_deg, lambda, transmittance);
colorbar();
set(gca,'Ydir','normal');
title('transmittance');
xlabel('incidence angle (degrees)');
ylabel('wavelength (\mum)');
axis([min(incidence_angle_deg), max(incidence_angle_deg), min(lambda), max(lambda)]);
if reverse_y_axis~=0
    set(gca, 'YDir','reverse');
end

subplot(1,2,1);
hold on;
for m = 1:10
  plot(incidence_angle_deg , FabryPerot_bands(n_inside, thickness, incidence_angle_rad, m), 'k-');
  plot(incidence_angle_deg , FabryPerot_bands(n_inside, thickness, incidence_angle_rad, m-1/2), 'k--');
end
% axis([min(incidence_angle_deg), max(incidence_angle_deg), min(lambda), max(lambda)]);

subplot(1,2,2);
hold on;
for m = 1:10
  plot(incidence_angle_deg , FabryPerot_bands(n_inside, thickness, incidence_angle_rad, m), 'k-');
  plot(incidence_angle_deg , FabryPerot_bands(n_inside, thickness, incidence_angle_rad, m-1/2), 'k--');
end
% axis([min(incidence_angle_deg), max(incidence_angle_deg), min(lambda), max(lambda)]);

sgtitle(['thickness=',num2str(thickness),' n_{inside}=',num2str(n_inside), ' n_{outside}=',num2str(n_outside)]);
