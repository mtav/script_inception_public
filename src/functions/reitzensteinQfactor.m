% reference:
%  Quantum dot micropillars
%  S Reitzenstein and A Forchel
%  J. Phys. D: Appl. Phys. 43 (2010) 033001 (25pp)
%  http://dx.doi.org/10.1088/0022-3727/43/3/033001

function Q = reitzensteinQfactor(ngaas,nalas,dgaas,dalas,ncav,dcav,lambda,n0,ml,mu)
  meff = 1/2*(ngaas+nalas)/(ngaas-nalas);
  neff = (2*ngaas*nalas)/(ngaas+nalas);
  Lm = meff*(dgaas+dalas);
  Leff = ncav*dcav + 2*neff*Lm
  rl = reitzenstein_reflectivity(n0,nalas,ngaas,ml);
  ru = reitzenstein_reflectivity(n0,nalas,ngaas,mu);
  Q = ((2*Leff)/(lambda))*((pi)/(1-rl*ru));
end
