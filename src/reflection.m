function r = reflection(x, wc, wqd, Gamma, Ktot, alpha, g)
  r = 1 - (Ktot/(1+alpha)) * (i*(wqd-wc+x)+(1/2)*Gamma) ./ ( (i*(wqd-wc+x)+(1/2)*Gamma) .* (i*x + (1/2)*Gamma + (1/2)*Ktot) + g^2 );
end
