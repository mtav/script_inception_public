clear all;
close all;

Nmodes = 5

d = zeros(Nmodes, 1);
w = zeros(Nmodes, 1);
input_values = zeros(Nmodes, 2);
for k = 1:Nmodes
  w(k) = rand() - I*abs(rand());
  d(k) = rand() + I*rand();
  %input_values(k, 1) = -angle(exp(-w(k)*I));
  input_values(k, 1) = w(k);
  input_values(k, 2) = d(k);
end

input_values = sortrows(input_values);

Nsamples = 2*Nmodes + 2 + 1000

c = zeros(1, Nsamples);
for t = 0:Nsamples-1
  SUMO = 0;
  for k = 1:Nmodes
    SUMO += d(k)*exp(-w(k)*I*t);
  end
  c(t+1) = SUMO;
end

disp('#################################');
disp('Input (w,d) pairs:');
input_values

disp('===> KBDM_Harminv test');
KBDM_output_values = KBDM_Harminv(c, Nmodes);

disp('Output (w,d) pairs:');
KBDM_output_values

disp('output_values - input_values');
KBDM_output_values(1:size(input_values,1), 1:size(input_values,2)) - input_values

disp('===> FDM_Harminv test');
FDM_output_values = FDM_Harminv(c, min(w), max(w), 1, Nmodes);

disp('Output (w,d) pairs:');
FDM_output_values

disp('output_values - input_values');
FDM_output_values(1:size(input_values,1), 1:size(input_values,2)) - input_values
disp('#################################');

figure();
subplot(2, 2, 1); hold on;
plot(1:Nmodes, real(input_values(1:Nmodes, 1)), 'r-+');
plot(1:Nmodes, real(KBDM_output_values(1:Nmodes, 1)), 'g.s');
plot(1:Nmodes, real(FDM_output_values(1:Nmodes, 1)), 'b.d');
axis([1 Nmodes, -1, 1]);
legend({'input','KBDM output','FDM output'});
xlabel('modes');
ylabel('radial frequencies Re(\omega)');

subplot(2, 2, 2); hold on;
plot(1:Nmodes, real(input_values(1:Nmodes, 2)), 'r-+');
plot(1:Nmodes, real(KBDM_output_values(1:Nmodes, 2)), 'g.s');
plot(1:Nmodes, real(FDM_output_values(1:Nmodes, 2)), 'b.d');
axis([1 Nmodes, -1, 1]);
legend({'input','KBDM output','FDM output'});
xlabel('modes');
ylabel('amplitudes Re(d)');

subplot(2, 2, 3); hold on;
plot(1:Nmodes, imag(input_values(1:Nmodes, 1)), 'r-+');
plot(1:Nmodes, imag(KBDM_output_values(1:Nmodes, 1)), 'g.s');
plot(1:Nmodes, imag(FDM_output_values(1:Nmodes, 1)), 'b.d');
axis([1 Nmodes, -1, 1]);
legend({'input','KBDM output','FDM output'});
xlabel('modes');
ylabel('radial frequencies Im(\omega)');

subplot(2, 2, 4); hold on;
plot(1:Nmodes, imag(input_values(1:Nmodes, 2)), 'r-+');
plot(1:Nmodes, imag(KBDM_output_values(1:Nmodes, 2)), 'g.s');
plot(1:Nmodes, imag(FDM_output_values(1:Nmodes, 2)), 'b.d');
axis([1 Nmodes, -1, 1]);
legend({'input','KBDM output','FDM output'});
xlabel('modes');
ylabel('amplitudes Im(d)');
