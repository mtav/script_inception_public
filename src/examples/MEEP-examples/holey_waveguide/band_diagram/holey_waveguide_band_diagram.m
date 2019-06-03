close all;
clear all;

fre = dlmread('fre.dat', ',', 0, 1);
fim = dlmread('fim.dat', ',', 0, 1);

k_idx_array = fre(:, 1);
k_x_array   = fre(:, 2);
k_y_array   = fre(:, 3);
k_z_array   = fre(:, 4);
f_array     = fre(:, 5:end);

figure;
hold on;

Nkpoints = size(f_array, 1)
Nbands_max = size(f_array, 2)

color_array = linspace(1, 10, Nbands_max);

for idx = 1:Nkpoints
  f_nonzero = nonzeros(f_array(idx, :));
  k_x = k_x_array(idx)*ones(size(f_nonzero));
  c = color_array(1:length(f_nonzero));
  scatter(k_x, f_nonzero, [], c);
end

% add light cone
area(k_x_array, k_x_array, 1, 'FaceColor', 0.75*ones(1,3));

xlabel('k_x (2\pi)');
ylabel('\omega (2\pic)');

% add markers corresponding to the output fields:
markers = [0.40, 0.1896;
           0.40, 0.3175;
           0.10, 0.4811;
           0.30, 0.8838;
           0.25, 0.2506];

for i = 1:size(markers,1)
  kx   = markers(i,1);
  fcen = markers(i,2);
  text(kx, fcen, sprintf('\\leftarrow kx=%.2f fcen=%.4f', kx, fcen));
end

saveas(gcf, 'holey_waveguide_band_diagram.png');
