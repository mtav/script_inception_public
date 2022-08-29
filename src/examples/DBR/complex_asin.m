close all;
clear all;

matlab_arcsin = @(z) -i*log(i*z+(1-z.^2).^(1/2));

figure;
hold on;

P=5 % points in between integers
N=2 % zmax
Npts = 1 + 2*N*(P+1) % number of points
z = linspace(-N, N, Npts);

plot(z, asin(z), 'k-', 'DisplayName', 'arcsin(z)');

plot(z, real(matlab_arcsin(z)), 'r+', 'DisplayName', 'real(matlab\_arcsin(z))');
plot(z, imag(matlab_arcsin(z)), 'bs', 'DisplayName', 'imag(matlab\_arcsin(z))');

legend();
xlabel('z');
ylabel('\theta (radians)');
