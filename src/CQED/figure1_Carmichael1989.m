% re-creating figure 1 from Carmichael1989

% TODO: Add Mollow triplet plot (free space resonance fluorescence)

gamma = 2*pi*9*1e9;

g = 5*gamma/2;

E0 = 1.1424*get_eV();
omega0 = E0/get_hb();
Q = 50e6;
kappa = omega0/Q;

disp(sprintf('kappa = %E', kappa));
disp(sprintf('gamma/2 = %E', gamma/2));
disp(sprintf('2*g/gamma = %E', 2*g/gamma));

x = linspace(-10, 10, 1000);

omega = x*gamma/2 + omega0;

% Spontaneous emission spectrum expression from Carmichael1989
[S_Carmichael_general, lambda_p, lambda_m, S_Carmichael_weak, S_Carmichael_strong, T_Carmichael_strong] = function_S_Carmichael(omega, omega0, kappa, gamma, g);

figure;
legend_text = {};

subplot(1,2,1); hold on;

plot(x, 2*S_Carmichael_general/max(S_Carmichael_general), 'k-');
legend_text{end+1} = '2\pi S(\omega) general';

%  plot(x, 2*S_Carmichael_weak/max(S_Carmichael_weak), 'r-o');
%  legend_text{end+1} = '2\pi S(\omega) for \kappa>>g>>\gamma/2';

plot(x, 2*S_Carmichael_strong/max(S_Carmichael_strong), 'g-');
legend_text{end+1} = '2\pi S(\omega) for g>>\kappa, g>>\gamma/2';

plot(x, 2*T_Carmichael_strong/max(T_Carmichael_strong), 'b-');
legend_text{end+1} = '2\pi T(\omega) for g>>\kappa, g>>\gamma/2';

xlabel('2*(\omega-\omega_{0})/\gamma');
ylabel('2\pi S(\omega) (normalized)');
legend(legend_text);
ylim([0,2.5]);

vline(2*(-g - gamma/2 )/gamma, 'r--');
vline(2*(-g           )/gamma, 'b--');
vline(2*(-g + gamma/2 )/gamma, 'r--');

vline(2*( g - gamma/2 )/gamma, 'r--');
vline(2*( g           )/gamma, 'b--');
vline(2*( g + gamma/2 )/gamma, 'r--');

subplot(1,2,2); hold on;
plot(x, 2*S_Carmichael_general, 'k-');
%  plot(x, 2*S_Carmichael_weak, 'r-o');
plot(x, 2*S_Carmichael_strong, 'g-');
plot(x, 2*T_Carmichael_strong, 'b-');

xlabel('2*(\omega-\omega_{0})/\gamma');
ylabel('2\pi S(\omega)');
legend(legend_text);

axis manual;

vline(2*(-g - gamma/2 )/gamma, 'r--');
vline(2*(-g           )/gamma, 'b--');
vline(2*(-g + gamma/2 )/gamma, 'r--');
  
vline(2*( g - gamma/2 )/gamma, 'r--');
vline(2*( g           )/gamma, 'b--');
vline(2*( g + gamma/2 )/gamma, 'r--');

%  legend({'2\pi S(\omega) general', '2\pi S(\omega) for \kappa>>g>>\gamma/2', '2\pi S(\omega) for g>>\kappa, g>>\gamma/2', '2\pi T(\omega) for g>>\kappa, g>>\gamma/2'});
