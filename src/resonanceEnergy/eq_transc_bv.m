% function eq_transc_bv.m
% besselj: Bessel function of the first kind.
% besselk: Modified Bessel function of the second kind.
function output = eq_transc_bv(u, v, L)
  w = sqrt(v.^2 - u.^2);
  output = (besselj(L-1,u)./besselj(L,u)) + (w./u).*(besselk(L-1,w)./besselk(L,w));
end
