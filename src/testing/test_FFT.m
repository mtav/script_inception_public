close all;
clear all;

N = 1e3;
lambda0 = 1;
f0 = get_c0()/lambda0;
omega0 = 2*pi*f0;
T0 = 1/f0;
tau = T0/100;
Fs = 1/tau;

t = 0:tau:N*tau;

f0 = exp(j*omega0*t);
f1 = cos(omega0*t);
f2 = sin(omega0*t);

NFFT = 2*ceil(N/2);

F0 = fft(f0, NFFT);
F1 = fft(f1, NFFT);
F2 = fft(f2, NFFT);

f = linspace(-Fs/2,Fs/2,NFFT);

%  figure;
%  subplot(2,2,1);
%  plot(t, real(f0));
%  subplot(2,2,3);
%  plot(t, imag(f0));
%  subplot(2,2,2);
%  plot(f, real(F0));
%  subplot(2,2,4);
%  plot(f, imag(F0));
%  
%  figure;
%  subplot(2,2,1);
%  plot(t, real(f1));
%  subplot(2,2,3);
%  plot(t, imag(f1));
%  subplot(2,2,2);
%  plot(f, real(F1));
%  subplot(2,2,4);
%  plot(f, imag(F1));
%  
%  figure;
%  subplot(2,2,1);
%  plot(t, real(f2));
%  subplot(2,2,3);
%  plot(t, imag(f2));
%  subplot(2,2,2);
%  plot(f, real(F2));
%  subplot(2,2,4);
%  plot(f, imag(F2));

j = 0:NFFT-1;
f = ones(size(j));

for k = 0:NFFT-1
  F(k+1) = sum(f(k+1)*exp(-i*2*pi*j*k/NFFT));
end
