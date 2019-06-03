function coupling_plot()
  z=linspace(0, pi+pi/2);
  [A, B] = getPower(1, z);
  [Aw, Bw] = getPower(0.3, z);
  figure;
  hold on;
  
  set(0, 'DefaultLineLineWidth', 2);
  
  plot(z,A, 'r-');
  plot(z,B, 'b-');
  plot(z,Aw, 'r--');
  plot(z,Bw, 'b--');
  
  %legend({'F=1','F=0.3'});
  
  xlabel('Length of the coupling region');
  ylabel('Normalized power');
  
  xticks([pi/2, pi]);
  xticklabels({'\pi/(2\gamma)','\pi/\gamma'});
  
  h = zeros(2, 1);
  h(1) = plot(NaN,NaN,'k-');
  h(2) = plot(NaN,NaN,'k--');
  legend(h, 'F=1','F=0.3', 'location', 'east');
  
  n = 5;
  x = [0.3, z(n)];
  y = [0.5, A(n)];
  annotation('textarrow', x, y, 'String', 'Waveguide I');
  

end

function [A, B] = getPower(F, z)
  % F = (kappa/gamma).^2;
  %kappa = 1;
  %gamma = kappa./sqrt(F);
  gamma = 1;
  B = F*(sin(gamma*z)).^2;
  A = 1 - B;
end
