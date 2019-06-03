function handle = createSurfPlotFromCSV(filename)
  % creates a 3D plot for an input file of the form:
  % x1;y1;f(x1,y1)
  % x1;y2;f(x1,y2)
  % x1;y3;f(x1,y3)
  % x2;y1;f(x2,y1)
  % x2;y2;f(x2,y2)
  % x2;y3;f(x2,y3)
  
  data = dlmread(filename); 
  NX = length(unique(data(:,1)));
  NY = length(unique(data(:,2)));
  x = reshape(data(:,1),NY,NX);
  y = reshape(data(:,2),NY,NX);
  z = reshape(data(:,3),NY,NX);
  handle = surf(x,y,z);
  xlabel('x');
  ylabel('y');
  zlabel('z');
  shading interp;
  set(handle, 'EdgeColor', 'black');
end
