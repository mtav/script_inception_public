function sub_indices = ind2sub_array(siz, linear_indices)
  % Equivalent to the Matlab/Octave ind2sub function, but returns all components into a single variable, i.e.:
  %
  % >> IND = [3 4 5 6];
  % >> s = [3,3];
  % >> sub_idx = ind2sub_array(s,IND)
  %  sub_idx =
  %
  %   ans(:,:,1) =
  %   3   1   2   3
  %
  %   ans(:,:,2) =
  %   1   2   2   2
  %
  % source ref: octave-3.6.1/liboctave/Array-util.cc
  %
  % TODO: Implement Matlab-like behaviour for ind2sub in the case of fewer indices. (should be in another function)
  % TODO: Create sub2ind_array() which can take an array as argument list (unless there is a Matlab-trick for argument unpacking...).
  % Solution:
  %  inds = num2cell(inds);
  %  value = A(inds{:});
  %  source: http://stackoverflow.com/questions/6390766/matlab-accessing-an-element-of-a-multidimensional-array-with-a-list
  
  linear_indices = linear_indices - 1; % moving to 0-indexed system

  Ndims = length(siz(:));
  Nindices = length(linear_indices(:));

  %sub_indices = ones([size(linear_indices), Ndims]);
  %return
  
  sub_indices = ones(Nindices, Ndims);
  
  for idx = 1:Nindices
  
    linear_index = linear_indices(idx);
    
    k = linear_index;
    for component_idx = 1:Ndims
      sub_indices(idx, component_idx) = mod(k, siz(component_idx));
      k = (k - sub_indices(idx, component_idx)) / siz(component_idx);
    end
    
  end

  sub_indices = sub_indices + 1; % back to 1-indexed system
  
  sub_indices = reshape(sub_indices, [size(linear_indices), Ndims]);
  
end
