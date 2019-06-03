function wavesimulator_1d_wrapper(Nlayers) %, cavity_size, t1, t2)

  lambda = 0.637;
  n1 = 1;
  n2 = 2.4;
  
  cavity_size = lambda/(1*n2);
  t1 = lambda/(4*n1);
  t2 = lambda/(4*n2);

  thickness_vector = [cavity_size, repmat([t1, t2], 1, Nlayers)];
  n_vector = [n2, repmat([n1, n2], 1, Nlayers)];
  
  b_vector = 1-0.5*n_vector/2.4;
  medium_color_vector = zeros(length(thickness_vector), 3);
  medium_color_vector(:, 3) = b_vector(:);
  
  wavesimulator_1d(thickness_vector, n_vector, medium_color_vector);
  
  %n_vector = [2.4,1,2.4,1];
  %thickness_vector = [lambda/n_vector(1),lambda/(4*n_vector(2)),lambda/(4*n_vector(3)),lambda/(n_vector(4))];
  %wavesimulator_1d(thickness_vector);
  %thickness_vector = [lambda/n_vector(1),lambda/(2*n_vector(2)),lambda/(2*n_vector(3)),lambda/(n_vector(4))];
  %wavesimulator_1d(thickness_vector);
  %thickness_vector = [lambda/n_vector(1),3*lambda/(2*n_vector(2)),2*lambda/(2*n_vector(3)),5*lambda/(n_vector(4))];
  %wavesimulator_1d(thickness_vector);
end
