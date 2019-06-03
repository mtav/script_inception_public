% creates a multimode decay function
% can be used to test the various fitting function (cf harminv_fit.m for example)
%
% The function is defined as follows:
%  gamma0 = pi*f0(i)/Q0(i);
%  y = y + A0(i)*sin(2*pi*f0(i)*x).*exp(-gamma0*x);
%
% where f0,Q0,A0 are lists of the frequencies, Q-factors and amplitude respectively of the different sine components desired
%
% The function also returns fmin and fmax variables which can be used to set an appropriate frequency range to plot the FFT.
%
% example usage:
%  f0 = [30,50,200,1000]
%  Q0 = [20,40,30,5e3]
%  A0 = [100,20,30,4000]
%  dt = 1/(300*max(f0));
%  tmin = 0;
%  tmax = 15*Q0(1)*1/(min(f0));
%  [x,y,fmin,fmax] = expsine(dt, tmin, tmax, f0, Q0, A0);

function [y,fmin,fmax] = expsine(x, f0, Q0, A0)
  y = zeros(size(x));
  
  fmin_list = zeros(size(f0));
  fmax_list = zeros(size(f0));
  
  for i=1:length(f0)
    gamma0 = pi*f0(i)/Q0(i);
    y = y + A0(i)*sin(2*pi*f0(i)*x).*exp(-gamma0*x);

    delta_f0 = f0(i)/Q0(i);
    fmin_list(i) = f0(i) - 10*delta_f0;
    fmax_list(i) = f0(i) + 10*delta_f0;

  end
  
  fmin = min(fmin_list);
  fmax = max(fmax_list);

end
