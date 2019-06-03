function plotDatFile(DATFILE,column)
  % CLEAR ALL removes all variables, globals, functions and MEX links.
  %clear all
  % CLC clears the command window and homes the cursor.
  %clc
  format long e
  
  [header, data] = readPrnFile(DATFILE);
  
  x = data(:,1);
  y = data(:,2);
  
  for i = 2:length(x)
    if(x(i)<x(i-1)); break; end
  end

  for j = 2:length(y)
    if(y(j)<y(j-1)); break; end
  end
  
  if i<j
    period = i-1;
    x_vector = x(1:period);
    y_vector = y(1:period:length(y));
  elseif j<i
    period = j-1;
    x_vector = x(1:period:length(x));
    y_vector = y(1:period);
  else
    disp('FATAL ERROR'); return;
  end
  
  length(x_vector)
  length(y_vector)
  
  [X,Y] = meshgrid(x_vector, y_vector);
  
  out = data(:,column);
  Z = reshape(out,size(X,1),size(X,2));
  
  %plot3(x,y,out);
  mesh(X,Y,Z);
  
end
