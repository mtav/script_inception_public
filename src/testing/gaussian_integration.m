function [a1,a2] = gaussian_integration()
  X = linspace(28.275485, 28.275500, 10); % for int(gaussian)~0.246/(2^3) -> a=28.275
  %X = linspace(14.137740, 14.137747, 10); % for int(gaussian^2)~0.246/(2^3) -> a=14.1377
  Y = X;

  for idx = 1:length(X)
    a = X(idx);
    Y(idx) = triplequad(@(x, y, z) exp(-a.*(x.^2 + y.^2 + z.^2)), -1/4, 1/4, -1/4, 1/4, -1/4, 1/4);
    %Y(idx) = triplequad(@(x, y, z) ( exp(-a.*(x.^2 + y.^2 + z.^2)) ).^2, -1/4, 1/4, -1/4, 1/4, -1/4, 1/4);
  end
  
  plot(X,Y);

  hline((1/2)^3,'r--');

  %hline(0.246,'g--');

  hline(0.246/(2^3),'b--');
  
  a1=28.275
  8*triplequad(@(x, y, z) exp(-a1.*(x.^2 + y.^2 + z.^2)), -1/4, 1/4, -1/4, 1/4, -1/4, 1/4)
  
  a2=14.1377
  8*triplequad(@(x, y, z) ( exp(-a2.*(x.^2 + y.^2 + z.^2)) ).^2, -1/4, 1/4, -1/4, 1/4, -1/4, 1/4)
  
  %foo = myfunc(a, 1, 2, 3)
  %triplequad(
end

function ret = myfunc(a, x, y, z)
  ret = exp(-a.*(x.^2 + y.^2 + z.^2));
end
