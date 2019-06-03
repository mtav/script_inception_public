meV = 1e-3*get_eV();
GHz = 1e9;

%%%%%%%%%%%
% Khitrova values

gamma = 2*pi*9*GHz;
g = pi*82*GHz;
omega0 = 1.1424*get_eV()/get_hb();

N_Q = 100;
N_delta = 101;

delta_omega = linspace(-0.5, 0.5, N_delta)*meV/get_hb();

Q_peaks = linspace(0, 6000, N_Q);
Q_spectra = [970, 1594, 1777, 2383, 3000, 6000];

CQED_study_wrapper(gamma, g, omega0, delta_omega, Q_peaks, Q_spectra, 'Khitrova');

%%%%%%%%%%%
% quantum emitter properties
lambda0_QD = 940*1e-9;
omega0_QD = 2*pi*get_c0()/lambda0_QD;
gamma_QD = 2*pi*1.59e-1*GHz;

lambda0_NV = 637*1e-9;
omega0_NV = 2*pi*get_c0()/lambda0_NV;
gamma_NV = 3.33e-3*GHz;

% coupling rates (related to chosen quantum emitters!!!)
% RCD S0.5-Ex
g_RCD_S05Ex_NV = 2*pi*8.26*GHz;

% M3 n=3.3 Ex
g_M3_GaP_Ex_NV = 2*pi*1.19*GHz;

g_M3_GaP_Ex_QD = 2*pi*25.5174050747*GHz;

g_bad_QD = 2*pi*10*GHz;

% micropillar
lambda0_micropillar = 937*1e-9;
omega0_micropillar = 2*pi*get_c0()/lambda0_micropillar;
gamma_micropillar = 2*pi*18*GHz;
g_micropillar = pi*39*GHz;

%%%%%%%%%%

gamma = gamma_micropillar;
omega0 = omega0_micropillar;
g = g_micropillar;

%  g_meV = g*get_hb()/meV;

kappa_lim1 = 4*g+gamma; % split
kappa_lim2 = 4*g-gamma; % strong
kappa_lim3 = sqrt(8*g^2-gamma^2); % 2 peak

Q_lim1 = omega0/kappa_lim1;
Q_lim2 = omega0/kappa_lim2;
Q_lim3 = omega0/kappa_lim3;

D = abs(Q_lim2 - Q_lim1);

N_Q = 100*4.5;
N_delta = 101;

delta_omega = linspace(-2*g, 2*g, N_delta);

Q_peaks = linspace(Q_lim1-1.5*D, Q_lim1+3*D, N_Q);
%  Q_spectra = [Q_lim1-1.2*D, Q_lim1-0.0001*D, (Q_lim1+Q_lim2)/2, 5332, Q_lim2, Q_lim3, Q_lim2+1*D, Q_lim1+3*D];
Q_spectra = [4500:100:4900];
%  Q_spectra = [4500:100:4900, 5000, 5332, Q_lim2, Q_lim3];

CQED_study_wrapper(gamma, g, omega0, delta_omega, Q_peaks, Q_spectra, 'example');
