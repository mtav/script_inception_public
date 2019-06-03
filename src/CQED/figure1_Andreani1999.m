% figure 1 from Andreani1999

Hz_to_meV = ((get_hb()/get_eV())*1e3); % angular frequency (omega)

% input parameters
Q = 2000; % no unit
kappa = 0.6 *1e-3*get_eV()/get_hb(); % Hz
V = 0.13 *(1e-6)^3; % mum^3

%  f_split = 100; % no unit
%  fmax = 200;

f_split = 1000; % no unit
fmax = 10000;

% directly computable parameters
omega0 = Q*kappa; % Hz

% TODO: label all those values: What are n,d,G,H,A,B,C,etc?
% calulate n: the refractive index

% f: oscillator strength of the dipole
f = f_split; % no unit

% d: dipole moment of the quentum emitter
d = sqrt( (get_e()^2*get_hb()*f) / (2*get_me()*omega0) ); % Coul*m

% g: coupling rate
% gamma: emission rate of the quantum emitter in bulk material

% intermediate values:
% G = g*n
% H = gamma/n
G = sqrt( (1/(4*pi*get_epsilon0())) * (pi*get_e()^2*f)/(get_me()*V) ); % g = G*1/n
H = (4/3 * (1/(4*pi*get_epsilon0())) * ((d^2*omega0^3)/(get_hb()*get_c0()^3)) ); % gamma = H*n

% solve second order equation A*n^2 + B*n + C = 0 for n
% this ensures that 4*g = kappa - gamma, when f = f_split
A = H;
B = -kappa;
C = 4*G;

delta = B^2-4*A*C;

n_plus = (-B+sqrt(delta))/(2*A); % no unit
n_minus = (-B-sqrt(delta))/(2*A); % no unit

n = n_minus; % no unit
gamma_split = H*n;
kappa_split = kappa;
g_split = G/n;
im_split = -(kappa_split + gamma_split)/4;

disp(['n = ', num2str(n)]);
fprintf('gamma_split = %E\n', gamma_split*Hz_to_meV);
fprintf('kappa_split = %E\n', kappa_split*Hz_to_meV);
fprintf('g_split = %E\n', g_split*Hz_to_meV);
fprintf('im_split = %E\n', im_split*Hz_to_meV);

% create the plot
f = linspace(0, fmax, fmax); % no unit
d = sqrt( (get_e()^2*get_hb()*f) / (2*get_me()*omega0) ); % Coul*m

G = sqrt( (1/(4*pi*get_epsilon0())) * (pi*get_e()^2*f)/(get_me()*V) ); % g = G*1/n
H = (4/3 * (1/(4*pi*get_epsilon0())) * ((d.^2*omega0^3)/(get_hb()*get_c0()^3)) ); % gamma = H*n
g = G*1/n; % Hz
gamma = H*n; %Hz

delta_omega_p = -(i/4)*(kappa+gamma) + sqrt(g.^2-((kappa-gamma)/4).^2);
delta_omega_m = -(i/4)*(kappa+gamma) - sqrt(g.^2-((kappa-gamma)/4).^2);

% create figure
mainfig = figure; hold on;
Hz_to_meV = ((get_hb()/get_eV())*1e3);

%  omega_p = omega0 - (i/4)*(kappa+gamma) + sqrt(g.^2-((kappa-gamma)/4).^2);
%  omega_m = omega0 - (i/4)*(kappa+gamma) - sqrt(g.^2-((kappa-gamma)/4).^2);
omega = 1; % dummy value because we do not need S here
[S_Andreani, omega_p, omega_m] = function_S_Andreani(omega, omega0, kappa, gamma, g);

% figure 1a
figure(mainfig);
subplot(2, 1, 1); hold on;
plot(f, (real(omega_m-omega0))*Hz_to_meV, 'r-');
subplot(2, 1, 1); hold on;
plot(f, (real(omega_p-omega0))*Hz_to_meV, 'b-');
%  axis([0, fmax, -0.16, 0.16]);
legend('real(\Omega_{-}-\omega_{0})', 'real(\Omega_{+}-\omega_{0})');
xlabel('Oscillator strength f (no unit)');
ylabel('Re(\Omega - \omega_{0}) (meV)');
vline(f_split, 'r--', ['f_{split} = ', num2str(f_split)]);

% figure 1b
figure(mainfig);
subplot(2, 1, 2); hold on;
plot(f, (imag(omega_m-omega0))*Hz_to_meV, 'r-');
subplot(2, 1, 2); hold on;
plot(f, (imag(omega_p-omega0))*Hz_to_meV, 'b-');
legend('imag(\Omega_{-}-\omega_{0})', 'imag(\Omega_{+}-\omega_{0})');
xlabel('Oscillator strength f (no unit)');
ylabel('Im(\Omega - \omega_{0}) (meV)');
axis([0, fmax, -0.32, 0]);
vline(f_split, 'r--', ['f_{split} = ', num2str(f_split)]);

hline(im_split*Hz_to_meV);

figure;
plot(f, gamma);
xlabel('Oscillator strength f (no unit)');
ylabel('gamma');

fprintf('kappa = [%E, %E]\n', min(kappa), max(kappa));
fprintf('gamma = [%E, %E]\n', min(gamma), max(gamma));

disp(['n = ', num2str(n)]);
