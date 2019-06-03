close all;
clear all;

x = linspace(-10,10);
%y = exp(-x.^2);
y = exp(-(x-(-10)).^2)+exp(-(x-(10)).^2);
fft_y = fft(y);

figure;
N=2;
M=2;
k=1;
k = plotRealImag(y, 'y', N, M, k);
k = plotRealImag(fft_y, 'fft(y)', N, M, k);

% https://uk.mathworks.com/matlabcentral/answers/41380-discrete-fourier-transform-of-real-valued-gaussian-using-fft

Ntot = 128;
% grid in time
tn = linspace(-10.0,10.0,Ntot);
% grid in frequency
fn = tn/(20.0*20.0/Ntot);
% Gaussian function in t-domain
gauss = exp(-tn.^2);

fftgauss = fftshift(fft(gauss));

dftgauss = zeros(1,Ntot);
for n = 1:Ntot
  for m = 1:Ntot
      dftgauss(n) = dftgauss(n) + gauss(m)*exp(2.0*pi*i*fn(n)*tn(m));
  end
end

dftgauss2 = zeros(1,Ntot);
for n = 1:Ntot
  for m = 1:Ntot
      %dftgauss2(n) = dftgauss2(n) + gauss(m)*exp(2.0*pi*i*(m-Ntot/2)*(n/Ntot - 1/2));
      dftgauss2(n) = dftgauss2(n) + gauss(m)*exp(2.0*pi*i* ((m-1)*Ntot/(Ntot-1) - Ntot/2) * ((n-1)/(Ntot-1) - 1/2));
  end
end

X = fftshift(fft(ifftshift(gauss)));

figure;
hold on;
real_dftgauss = real(dftgauss);
real_dftgauss = real_dftgauss./max(real_dftgauss(:));
real_dftgauss2 = real(dftgauss2);
real_dftgauss2 = real_dftgauss2./max(real_dftgauss2(:));

plot(fn, real_dftgauss, 'bo');
plot(fn, real_dftgauss2, 'gs');
plot(fn, exp(-pi^2*fn.^2), 'r-');

figure;
N=5;
M=2;
k=1;
k = plotRealImag(gauss, 'gauss', N, M, k);
k = plotRealImag(fftgauss, 'fftgauss', N, M, k);
k = plotRealImag(abs(fftgauss), 'abs(fftgauss)', N, M, k);
k = plotRealImag(dftgauss, 'dftgauss', N, M, k);
k = plotRealImag(X, 'fftshift(fft(ifftshift(gauss)))', N, M, k);

% http://uk.mathworks.com/matlabcentral/answers/40257-gaussian-fft
