close all;
clear all;

FIB_infos_struct = FIB_infos();
[mag, beamCurrent_pA] = meshgrid(FIB_infos_struct.standard_magnifications, FIB_infos_struct.beamInfos.beamCurrent_pA);
beamDiameter_mum = getSpotSize(beamCurrent_pA);
[resolution_mum_per_pxl, HFW, FIB_infos_struct] = getResolution(mag);
beamDiameter_pixels = floor(beamDiameter_mum ./ resolution_mum_per_pxl);

set(groot, 'defaultTextInterpreter', 'none');

figure;
surf(mag, beamCurrent_pA, beamDiameter_pixels);
xlabel('mag');
ylabel('beamCurrent_pA');
zlabel('beamDiameter_pixels');

figure;
hold on;
plot(mag(1,:), beamDiameter_pixels(1,:), 'ro-', 'DisplayName', sprintf('beamCurrent = %d pA', beamCurrent_pA(1,1)));
plot(mag(end,:), beamDiameter_pixels(end,:), 'bo-', 'DisplayName', sprintf('beamCurrent = %d pA', beamCurrent_pA(end,1)));
legend();
xlabel('mag');
ylabel('beamDiameter_pixels');

figure;
plot(beamCurrent_pA(:,1), beamDiameter_pixels(:,1), 'ro-', 'DisplayName', sprintf('mag = %d', mag(1,1)));
legend();
xlabel('beamCurrent_pA');
ylabel('beamDiameter_pixels');

figure;
plot(beamCurrent_pA(:,end), beamDiameter_pixels(:,end), 'bo-', 'DisplayName', sprintf('mag = %d', mag(1,end)));
legend();
xlabel('beamCurrent_pA');
ylabel('beamDiameter_pixels');
