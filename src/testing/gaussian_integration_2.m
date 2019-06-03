X = linspace(0.1, 10, 10);
Y = X;

for idx = 1:length(X)
  idx
  lambda = X(idx)
  Rmax = 10*lambda
  Y(idx) = triplequad(@(x, y, z) exp(-8.*(x.^2 + y.^2 + z.^2)./(lambda.^2)), -Rmax, Rmax, -Rmax, Rmax, -Rmax, Rmax)
end

plot(X, Y./(X.^3));
