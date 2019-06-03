function rgb_values = val2rgb(numeric_values)
  % returns the color R,G,B values for the given numeric values
  % R,G,B values are in the [0,1] range
  % For an input array V, the output array will be of size [size(V,1), size(V,2), 3] (This emulates ind2rgb behaviour.)

  c_range = caxis;
  cmin = c_range(1);
  cmax = c_range(2);
  m = size(colormap, 1);

  index = fix((numeric_values-cmin)/(cmax-cmin)*m)+1
  %Clamp values outside the range [1 m] (ind2rgb does that already, but this avoids warnings)
  index(index<1) = 1;
  index(index>m) = m;

  rgb_values = ind2rgb(index, colormap);
end
