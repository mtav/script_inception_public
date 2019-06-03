function dX = diffCentered(X)
  % returns a diff array dX of the same size as X with:
  % dX(i) = (X(i+1)-X(i-1))/2 for 1 < i < end
  % dX(1) = (X(2)-X(1))/2
  % dX(end) = (X(end)-X(end-1))/2
  
  % TODO: support arrays with more than 1 dimension
  % TODO: make size(dX) = size(X)
  % TODO: allow choosing diff direction for Ndims > 1
  
  X = X(:);
  dX = [(X(2) - X(1))/2; (X(3:end) - X(1:end-2))/2; (X(end) - X(end-1))/2];
end
