% Recreating the plots from figure 2 in Khitrova2006.

% TODO: Figure out why the Carmichael spectrum splits at much higher Qs than the Andreani spectrum.

close all;
clear all;

clear('i');

normalize_spectra = true;
set_spectra_height = true;

% figure 2c
gamma = 2*pi*9*1e9;
g = pi*82*1e9;
E0 = 1.1424*get_eV();
omega0 = E0/get_hb();
lambda0 = 2*pi*get_c0()/omega0;

Hz_to_meV = ((get_hb()/get_eV())*1e3); % angular frequency (omega)
%  Hz_to_meV = get_h()/(1e-3*get_eV()); % frequency (f, nu)

Delta_E_meV_range = linspace(-0.5,0.5,1000);
Delta_E_eV_range = Delta_E_meV_range*1e-3;
E_eV_range = Delta_E_eV_range + E0/get_eV();
omega_range = E_eV_range*get_eV()/get_hb();

Q_list = [970, 1594, 1777, 2383, 3000, 6000];
spectrum_height = [27.5, 17.5, 15, 10, 11, 20];
%Q_list = [970];

mainfig = figure; hold on;
subfig = figure; hold on;

cc = hsv(length(Q_list));
legend_list = {};
for idx = 1:length(Q_list)

  Q = Q_list(idx);
  
  kappa = omega0/Q;

  % debug output
  disp(sprintf('kappa = %E', kappa));
  disp(sprintf('gamma/2 = %E', gamma/2));
  disp(sprintf('2*g/gamma = %E', 2*g/gamma));
  
  % Emission spectrum expression from Andreani1999
  [S_Andreani, omega_p, omega_m] = function_S_Andreani(omega_range, omega0, kappa, gamma, g);
  
  % Emission spectrum expression from Carmichael1989
  [S_Carmichael_general, lambda_p, lambda_m] = function_S_Carmichael(omega_range, omega0, -kappa/2, gamma, g);
  %    [S_Carmichael_general, lambda_p, lambda_m] = function_S_Carmichael(omega_range, omega0, -kappa/(2*pi), gamma, g);
  S_Carmichael_general = abs(S_Carmichael_general);
  
  if normalize_spectra
    S_Andreani = S_Andreani ./ max(S_Andreani);
    S_Carmichael_general = S_Carmichael_general ./ max(S_Carmichael_general);
  end

  if set_spectra_height
    S_Andreani           = spectrum_height(idx) * S_Andreani;
    S_Carmichael_general = spectrum_height(idx) * S_Carmichael_general;
  end

  FWHM_meV = -2*imag(omega_p)*Hz_to_meV;
  
  peak_pos_p = (real(omega_p)-omega0)*Hz_to_meV;
  peak_pos_m = (real(omega_m)-omega0)*Hz_to_meV;
  
  disp(['Q = ', num2str(Q), ' FWHM_meV = ', num2str(FWHM_meV), ' peak_pos_p = ', num2str(peak_pos_p), ' peak_pos_m = ', num2str(peak_pos_m)]);

  figure(mainfig); hold on;
  subplot(2, 2, [2,4]); hold on;
  
  plot(Delta_E_meV_range, S_Andreani, 'color', cc(idx,:),  'marker', '+');
%    plot(Delta_E_meV_range, S_Carmichael_general, 'color', cc(idx,:), 'marker', 'o');
  
  xlabel('E-E_{0} (meV)');
  ylabel('Spontaneous emission (a.u.)');

  figure(subfig); hold on;
  
  subplot(2, 3, idx); hold on;
  
  plot(Delta_E_meV_range, S_Andreani, 'k', 'marker', '+');
  legend_list{end+1} = ['Q = ', num2str(Q), ' Andreani1999'];

%    plot(Delta_E_meV_range, S_Carmichael_general, 'm', 'marker', 'o');
%    legend_list{end+1} = ['Q = ', num2str(Q), ' Carmichael1989'];

%    legend( {legend_list{end-1}, legend_list{end}} );
  
  title(['Q = ', num2str(Q), ', FWHM = ', num2str(FWHM_meV), ' meV, E_{+}-E_{0} = ', num2str(peak_pos_p), ' meV, E_{-}-E_{0} = ', num2str(peak_pos_m), ' meV']);
  xlabel('E-E_{0} (meV)');
  ylabel('Spontaneous emission (a.u.)');
  
%    vline(g*Hz_to_meV, 'k--');
%    vline(-g*Hz_to_meV, 'k--');

  vline(peak_pos_m-FWHM_meV/2, 'r--');
  vline(peak_pos_m, 'r-');
  vline(peak_pos_m+FWHM_meV/2, 'r--');

  vline(peak_pos_p-FWHM_meV/2, 'b--');
  vline(peak_pos_p, 'b-');
  vline(peak_pos_p+FWHM_meV/2, 'b--');

  hline(0.5);

end

figure(mainfig); hold on;
subplot(2, 2, [2,4]); hold on;
legend(legend_list);
hline(0.5);

% figures 2a and 2b
Q = linspace(0,4000,1000);
kappa = omega0./Q;
gamma_array = gamma*ones(size(Q));
Qlim = omega0/(4*g+gamma);

%  omega_p = omega0 - (i/4)*(kappa+gamma) + sqrt(g^2-((kappa-gamma)/4).^2);
%  omega_m = omega0 - (i/4)*(kappa+gamma) - sqrt(g^2-((kappa-gamma)/4).^2);
[S_dummy, omega_p, omega_m] = function_S_Andreani(1, omega0, kappa, gamma, g);

% figure 2a
figure(mainfig);
subplot(2, 2, 1); hold on;
plot(Q, (real(omega_m)-omega0)*Hz_to_meV, 'r-');
subplot(2, 2, 1); hold on;
plot(Q, (real(omega_p)-omega0)*Hz_to_meV, 'b-');
axis([0, 4000, -0.2, 0.2]);
legend('real(\Omega_{-})-\omega_{0}', 'real(\Omega_{+})-\omega_{0}');
xlabel('Quality factor Q');
ylabel('Relative energy (meV)');
vline(Qlim, 'r--', ['Qlim = ', num2str(Qlim)]);

% figure 2b
figure(mainfig);
subplot(2, 2, 3); hold on;
plot(Q, -2*imag(omega_m)*Hz_to_meV,'r-');
subplot(2, 2, 3); hold on;
plot(Q, -2*imag(omega_p)*Hz_to_meV,'b-');
subplot(2, 2, 3); hold on;
plot(Q, kappa*Hz_to_meV,'g-');
subplot(2, 2, 3); hold on;
plot(Q, gamma_array*Hz_to_meV,'k-');
legend('-2\cdot{}imag(\Omega_{-})', '-2\cdot{}imag(\Omega_{+})', '\kappa', '\gamma_{os}');
xlabel('Quality factor Q');
ylabel('FWHM (meV)');
axis([0, 4000, -0.2, 1.2]);
vline(Qlim, 'r--', ['Qlim = ', num2str(Qlim)]);

Q_Purcell = 250;
kappa_Purcell = omega0./Q_Purcell;
[S_dummy, omega_p_Purcell, omega_m_Purcell] = function_S_Andreani(1, omega0, kappa_Purcell, gamma, g);
slope = (4*g^2/omega0)*Hz_to_meV;
yp_Purcell = -2*imag(omega_p_Purcell)*Hz_to_meV
ym_Purcell = -2*imag(omega_m_Purcell)*Hz_to_meV

vline(Q_Purcell, 'r--');
hline(yp_Purcell);
hline(ym_Purcell);
plot(Q, slope*(Q-Q_Purcell) + yp_Purcell, 'r--');

% figure 2a bis
figure; hold on;
plot(Q, (imag(omega_m-omega0))*Hz_to_meV, 'r-');
plot(Q, (imag(omega_p-omega0))*Hz_to_meV, 'b-');
axis([0, 4000, -1.2, 0.2]);
legend('imag(\Omega_{-}-\omega_{0})', 'imag(\Omega_{+}-\omega_{0})');
xlabel('Quality factor Q');
ylabel('Relative energy (meV)');
vline(Qlim, 'r--', ['Qlim = ', num2str(Qlim)]);

% figure 2b bis
figure; hold on;
%  plot(Q, -2*imag(omega_m)*Hz_to_meV,'r-');
plot(Q, -2*imag(omega_p)*Hz_to_meV,'b-');
%  plot(Q, kappa*Hz_to_meV,'g-');
plot(Q, gamma_array*Hz_to_meV,'k-');
legend('-2\cdot{}imag(\Omega_{-})', '-2\cdot{}imag(\Omega_{+})', '\kappa', '\gamma_{os}');
xlabel('Quality factor Q');
ylabel('FWHM (meV)');
axis([0, 4000, -0.2, 1.2]);
vline(Qlim, 'r--', ['Qlim = ', num2str(Qlim)]);

vline(Q_Purcell, 'r--');
hline(yp_Purcell);
hline(ym_Purcell);
plot(Q, slope*(Q-Q_Purcell) + yp_Purcell, 'r--');

figure;
plot(Q, kappa);
xlabel('Quality factor Q');
ylabel('kappa');

fprintf('kappa = [%E, %E]\n', min(kappa), max(kappa));
fprintf('gamma = [%E, %E]\n', min(gamma), max(gamma));
