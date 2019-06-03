%then in Matlab:
%t=-2*w+tau:(1/f)/10:2*w+tau;
%plot(t,A*exp(-(t-tau).^2/w^2).*exp(i*2*pi*f*t),'r');
%hold on;
%data=dlmread('p01_id_.prn','',1,0); plot(1e-12*data(:,1),data(:,2),'b');

t = -200*w+tau:(1/f)/100:200*w+tau;
%N=10000
%t = -1/(2*f)+tau:(1/f)/100:1/(2*f)+tau;

% to make sure that length(t)*(t(2)-t(1))*f, so that the maximum of the peak is really on f0. :)
%t=t(1:48300);
%u=u(1:48300);

u = A*exp(-(t-tau).^2/w^2).*sin(2*pi*f*t);
[calcFFT_output, lambda_vec_mum, freq_vec_Mhz] = calcFFT(u, t(2)-t(1));
Y = calcFFT_output.*conj(calcFFT_output);
%close all;
figure; hold on;

subplot(1,2,1);
plot(t,u);

subplot(1,2,2);
plot(freq_vec_Mhz,Y);

hold on;
axis([f-2/w,f+2/w,min(Y),max(Y)]);
vline(fmin,'g');
vline(fmax,'g');
vline(f,'r');
hline(max(Y)/2,'k')

%%to plot the FFT:
%t=-20*w+tau:(1/f)/100:20*w+tau; u=A*exp(-(t-tau).^2/w^2).*sin(2*pi*f*t); [calcFFT_output, lambda_vec_mum, freq_vec_Mhz] = calcFFT(u, t(2)-t(1)); Y=calcFFT_output.*conj(calcFFT_output); plot(freq_vec_Mhz,Y); axis([f-1/w,f+1/w,min(Y),max(Y)])

%A=10.0; tau=2.7e-08; w=4e-09; f=2500000000.0;
%t=-200*w+tau:(1/f)/100:200*w+tau; u=A*exp(-(t-tau).^2/w^2).*sin(2*pi*f*t); [calcFFT_output, lambda_vec_mum, freq_vec_Mhz] = calcFFT(u, t(2)-t(1)); Y=calcFFT_output.*conj(calcFFT_output); plot(freq_vec_Mhz,Y); axis([f-1/w,f+1/w,min(Y),max(Y)])
%hold on; plot(freq_vec_Mhz, max(Y)*(exp(-pi^2*w^2*(freq_vec_Mhz-f).^2)).^2,'go');
