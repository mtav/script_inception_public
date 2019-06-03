close all;
clear all;

K = 10
N=24000
noise=7/100

Q_min=1
Q_max=1000
freq_min=3e14 % ~ 1.000 mum
freq_max=6e14 % ~ 0.500 mum
A_min=0
A_max=1
decay_min = 0
decay_max = 1e11

%% compute derived values
T_min = 1/freq_max
T_max = 1/freq_min
timestep = T_min/100

datafile = '/tmp/data'
Npoints = 1e5

[freq_model, decay_model] = harminv_generateModes(K, freq_min, freq_max, decay_min, decay_max);
harminv_generateSignal(datafile, Npoints, timestep, freq_model, decay_model);

figure;
data = harminv_plotSignal(datafile);

figure;
harminv_plotModes(timestep, freq_model, decay_model, 'r+');

% add some annotations
subplot(2,2,1);

start_freq = min(freq_model)
stop_freq = max(freq_model)

phi_min = -timestep*2*pi*start_freq
phi_max = -timestep*2*pi*stop_freq

hold all;
plot([cos(phi_max),0,cos(phi_min)], [sin(phi_max),0,sin(phi_min)], 'g--');

t=linspace(0,2*pi);
hold all;
plot(cos(t), sin(t), 'g--');

[freq_extracted, decay_extracted, Q, amp, phase, err] = harminv2(datafile, timestep, start_freq, stop_freq);

if ~isempty(freq_extracted)
  harminv_plotModes(timestep, freq_extracted, decay_extracted, 'bo');
  %legend({'model','extracted'});
end

%% choose random u values
%u0 = rand(K,1) .* exp(I*2*pi*rand(K,1));
%%r = rand(K,1);
%%l = 2*pi*r.*rand(K,1);
%%u1 = r.*exp(I*l);
%x = 2*rand(K,1) - 1;
%y = 2*sqrt(1-x.^2).*rand(K,1) - sqrt(1-x.^2);
%u1 = x+I*y;

%omega_real = 2*pi*rand(K,1);
%omega_imag = 5e-4*rand(K,1);

%omega0 = omega_real - I*omega_imag;

%% choose K random frequency (f), Q-factor (Q), amplitude (A) values
%Q = (Q_max - Q_min)*rand(K,1) + Q_min;
%gamma = (gamma_max - gamma_min)*rand(K,1) + gamma_min;
%f = (f_max - f_min)*rand(K,1) + f_min;
%A = (A_max - A_min)*rand(K,1) + A_min;

%% compute derived values
%nu = 2*pi*f;
%%gamma = pi*abs(f)./Q;
%omega1 = nu - I*gamma;
%%omega = nu;
%u2 = exp(-I*omega0);
%u3 = exp(-I*dt*omega1);

%%figure;
%%Nplots=4;
%%subplot(Nplots,1,1);
%%plot(u0, 'o');
%%subplot(Nplots,1,2);
%%plot(u1, 'o');
%%subplot(Nplots,1,3);
%%plot(u2, 'o');
%%subplot(Nplots,1,4);
%%plot(u3, 'o');

%%figure;
%%Nplots=4;
%%subplot(Nplots,1,1);
%%plot(u0, 'o');
%%subplot(Nplots,1,2);
%%plot(u1, 'o');
%%subplot(Nplots,1,3);
%%plot(u2, 'o');
%%subplot(Nplots,1,4);
%%plot(u3, 'o');

%%harminv_plotModes(1, omega0);
%[f, decay] = harminv_generateModes(K, fmin, fmax, decay_min, decay_max);
