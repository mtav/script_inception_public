% reference:
%  Quantum dot micropillars
%  S Reitzenstein and A Forchel
%  J. Phys. D: Appl. Phys. 43 (2010) 033001 (25pp)
%  http://dx.doi.org/10.1088/0022-3727/43/3/033001

function r = reitzenstein_reflectivity(n0,nalas,ngaas,m)
  r = (n0-(nalas/ngaas)^(2*m))/(n0+(nalas/ngaas)^(2*m));
end
