function waveguide_modes()

  x = linspace(0, 3*pi/2);
  d=1;
  mu=1;
  mu1=1;
  y_even = mu/mu1*x.*tan(x);
  y_odd = mu/mu1*x.*cot(x);
  y = sqrt(1-x.^2);
  figure;
  plot(x,y_even);
  figure;
  plot(x,y_odd);
  figure;
  plot(x,y);

end
