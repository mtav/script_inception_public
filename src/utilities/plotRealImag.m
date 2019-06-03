function k_new = plotRealImag(y, name, i, j, k)
  subplot(i, j, k);
  plot(real(y));
  title(sprintf('real(%s)', name));
  subplot(i, j, k+1);
  plot(imag(y));
  title(sprintf('imag(%s)', name));
  k_new = k+2;
end
