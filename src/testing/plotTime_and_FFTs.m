function plotTime_and_FFTs( t, f )
% plots f(t), real(fft(t)) and imag(fft(t))
    figure;
    subplot(1,4,1);
    plot(t,f);
    subplot(1,4,2);
    plot(real(fft(f)));
    subplot(1,4,3);
    plot(imag(fft(f)));
    subplot(1,4,4);
    plot(angle(fft(f))/(2*pi));
end
