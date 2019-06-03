function ret = interpolate(x_vector,y_vector,idx1,idx2,x)
  ret = y_vector(idx1) + (y_vector(idx2)-y_vector(idx1))/(x_vector(idx2)-x_vector(idx1))*(x-x_vector(idx1));
end
