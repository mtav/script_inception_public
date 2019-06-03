t = linspace(0, 1000*2*pi, 100000);

alpha_list = [];

max_real_fft_left = [];
max_real_fft_right = [];

max_imag_fft_left = [];
max_imag_fft_right = [];

res_abs_fft_left = [];
res_abs_fft_right = [];

res_angle_fft_left = [];
res_angle_fft_right = [];

for alpha = linspace(0,1,100)
    close all;
    T = 2*pi;
    myfunc = sin((2*pi/T)*t+alpha*T);
%    myfunc = exp(i*((2*pi/T)*t+alpha*T));
    %plotTime_and_FFTs(t, myfunc);
    %title(sprintf('f = %f T = %f \\alpha = %f', 1/T, T, alpha));

    
    F = fft(myfunc);
    
    real_fft_myfunc = real(F);
    imag_fft_myfunc = imag(F);
    abs_fft_myfunc = abs(F);
    angle_fft_myfunc = angle(F)/(2*pi);
    
    mid = round(length(abs_fft_myfunc)/2);
    abs_fft_myfunc_1 = abs_fft_myfunc(1:mid);
    abs_fft_myfunc_2 = abs_fft_myfunc(mid+1:end);
    
    idx_left = find(abs_fft_myfunc_1 == max(abs_fft_myfunc_1 ));
    idx_right = mid + find(abs_fft_myfunc_2 == max(abs_fft_myfunc_2 ));
    
%    mini = min(abs_fft_myfunc);
 %   maxi = max(abs_fft_myfunc);
    %idx_mini = find(abs_fft_myfunc==mini);
%     idx_maxi = find(abs_fft_myfunc==maxi);
%     idx_left = min(idx_mini, idx_maxi);
%     idx_right = max(idx_mini, idx_maxi);
%     
%     idx_maxi(1)
%     idx_m

    alpha_list(end+1) = alpha;
    max_real_fft_left(end+1) = real_fft_myfunc(idx_left);
    max_real_fft_right(end+1) = real_fft_myfunc(idx_right);
    max_imag_fft_left(end+1) = imag_fft_myfunc(idx_left);
    max_imag_fft_right(end+1) = imag_fft_myfunc(idx_right);
    res_abs_fft_left(end+1) = abs_fft_myfunc(idx_left);
    res_abs_fft_right(end+1) = abs_fft_myfunc(idx_right);
    res_angle_fft_left(end+1) = angle_fft_myfunc(idx_left);
    res_angle_fft_right(end+1) = angle_fft_myfunc(idx_right);

end

figure;
hold on;
plot(alpha_list, max_real_fft_right, 'r-o');
plot(alpha_list, max_real_fft_left, 'b-o');
legend('right peak','left peak');
title('peak amplitudes of real(fft(f(t)))');

figure;
hold on;
plot(alpha_list, max_imag_fft_right, 'r-o');
plot(alpha_list, max_imag_fft_left, 'b-o');
legend('right peak','left peak');
title('peak amplitudes of imag(fft(f(t)))');

figure;
hold on;
plot(alpha_list, max_real_fft_right, 'r-s');
plot(alpha_list, max_real_fft_left, 'b-s');
plot(alpha_list, max_imag_fft_right, 'r-o');
plot(alpha_list, max_imag_fft_left, 'b-o');
legend('right real peak','left real peak','right imag peak','left imag peak');
title('real and imag peak amplitudes of fft(f(t))');

figure;
hold on;
plot(alpha_list, res_angle_fft_right, 'r-o');
plot(alpha_list, res_angle_fft_left, 'b-o');
legend('right peak','left peak');
title('peak amplitudes of angle(fft(f(t)))');
