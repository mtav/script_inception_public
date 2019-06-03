function [linear_indices, values, abs_err, sub_indices, minerr] = closestInd(A, b, tol)
  %  function [linear_indices, values, abs_err, sub_indices, minerr] = closestInd(A, b, tol)
  %
  %  Find the elements in array *A* closest to value *b* and return their indices.
  %    * If tol is not given, simply search for the closest values.
  %    * If tol is given, search for all values in the b+/-tol range.
  %
  %  Input:
  %    * A : array of any dimensions
  %    * b : scalar number
  %    * tol : scalar number
  %
  %  Output:
  %    * linear_indices : linear-indices of the found values
  %    * values : the found values
  %    * abs_err : absolute error between b and the found values
  %    * sub_indices : sub-indices of the found values
  %    * minerr : smallest distance from A to b
  %
  %  Assuming *K* closest values where found and *M = ndims(A)*, the size of the return values are:
  %    * linear_indices, values and abs_err all have the same size:
  %      * If A is a vector, then they are vectors with the same orientation as A, i.e. of size [K,1] or [1,K].
  %      * If A is a multidimensional array, then they are column vectors of size [K,1].
  %    * sub_indices : [K,M]
  %
  %  Special cases:
  %    * If A is empty, then all return values are empty arrays.
  %    * If no closest values or values within the requested range were found, then all return values are empty arrays, except *minerr*, which will either be the smallest distance to *b* or *NaN* if no such distance could be computed.
  %
  %  Note: This function also replaces the old "[value,pos] = findnear(A,b)" function. But be aware of the different return values and the change in dimensions!!!
  %
  %  TODO: finish testing this function and its use in calcMV()+plotProbe(), etc functions

  % create absolute error array
  abs_err_array = abs(A-b);
  
  % get global minimum absolute error
  minerr = min(abs_err_array(:));

  if ~exist('tol', 'var')
    tol = minerr;
  end

  % find indices of minima positions
  if ~isempty(abs_err_array)
    linear_indices = find(abs_err_array <= tol);
  else
    linear_indices = [];
  end

  % set additional return variables, if requested
  if nargout >= 2
    values = A(linear_indices);
  end
  
  if nargout >= 3
    abs_err = abs_err_array(linear_indices);
  end

  if nargout >= 4
    sub_indices = ind2sub_array(size(A), linear_indices(:));
    sub_indices = permute(sub_indices,[1 3 2]);
  end
    
end
