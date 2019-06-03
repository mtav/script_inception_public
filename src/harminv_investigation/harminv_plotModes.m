function harminv_plotModes(dt, freq, decay, style)
  Nplots_i = 2;
  Nplots_j = 2;
  
  omega = 2*pi*freq - I*decay;
  u = exp(-I*dt*omega);

  subplot(Nplots_i, Nplots_j, 1);
  hold all;
  plot(real(u), imag(u), style);
  axis ([-1, 1, -1, 1], "square");
  xlabel('real(u)');
  ylabel('imag(u)');
  
  subplot(Nplots_i, Nplots_j, 2);
  hold all;
  plot(real(omega), imag(omega), style);
  xlabel('real(omega)');
  ylabel('imag(omega)');
  
  subplot(Nplots_i, Nplots_j, 3);
  hold all;
  plot(freq, decay, style);
  xlabel('freq');
  ylabel('decay');
  
  subplot(Nplots_i, Nplots_j, 4);
  hold all;
  plot(freq, pi*abs(freq)./decay, style);
  xlabel('freq');
  ylabel('Q');

end
