function plotVectors(varargin)
  X = zeros(2,length(varargin));
  Y = zeros(2,length(varargin));
  Z = zeros(2,length(varargin));
  for k = 1:length(varargin)
    X(:,k) = (varargin{k}(1,:))'; % Cell array indexing
    Y(:,k) = (varargin{k}(2,:))';
    Z(:,k) = (varargin{k}(3,:))';
  end
  plot3(X,Y,Z);
  xlabel('X');
  ylabel('Y');
  zlabel('Z');
end
