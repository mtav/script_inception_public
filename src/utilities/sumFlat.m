function result = sumFlat(data)
  % simple convenience function to sum over all elements in case data is something complex like data(:,:,2:5,...) or a product/sum, etc
  result = sum(data(:));
end
