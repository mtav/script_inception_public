%  graphics_toolkit('gnuplot');
graphics_toolkit('fltk');

close all;
clear all;
f='MPB-scaling-test_lattice_basis_size-1_lattice_size-1_scale-1.out.dat';
[header, data] = readPrnFile(f);
k1 = data(:, 2);

band_2 = data(:, 7);
band_3 = data(:, 8);

band_6 = data(:, 11);
band_7 = data(:, 12);

band_10 = data(:, 15);
band_11 = data(:, 16);

figure;
hold on;

n_1 = 1;
n_2 = 3.5;
n_0 = 2/(1/n_1+1/n_2);

plot(k1, 1/n_2*abs(k1),'r--');
plot(k1, 1/n_0*abs(k1),'g:');
plot(k1, 1/n_1*abs(k1),'b-.');

plot(k1, 1/n_0*abs(k1-2),'g:');
plot(k1, 1/n_0*abs(k1-1),'g:');
plot(k1, 1/n_0*abs(k1+1),'g:');
plot(k1, 1/n_0*abs(k1+2),'g:');

plot(k1, band_2, 'r-');
plot(k1, band_3, 'b-');

plot(k1, band_6, 'r-');
plot(k1, band_7, 'b-');

plot(k1, band_10, 'r-');
plot(k1, band_11, 'b-');

xlim([-0.5, 0.5]);
ylim([0, 1.5]);

title('1D $\lambda/(4n)$ DBR stack in the x direction with $n_1=1$ and $n_2=3.5$');
xlabel('$k_x/(2\pi/a)$');
ylabel('$\omega / (2 \pi c_0 / a) = a / \lambda$');
legend({'$n_2=3.5 \rightarrow y=(1/n_2) \cdot |x|$', '$n_0=2/(1/n_1+1/n_2) \rightarrow y=(1/n0) \cdot |x|$', '$n_1=1 \rightarrow y=(1/n_1) \cdot |x|$'}, 'location', 'southoutside');

vline(0);

FILEBASE = 'lightcone_comparison';
%  graphics_toolkit('gnuplot');
%  saveas(gcf, [FILEBASE,'.pdf']);
%  graphics_toolkit('fltk');
print(gcf, FILEBASE, '-dpdflatexstandalone');
system(['pdflatex ',FILEBASE,'.tex']);
