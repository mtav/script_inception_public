function xyzlabel(varargin)
  % Label all axes in one command.
  % The default labels are 'x', 'y', 'z'.
  % Usage examples:
  %   xyzlabel('X_{s}');
  %   xyzlabel('X_{s}', 'Y_{s}');
  %   xyzlabel('X_{s}', 'Y_{s}', 'Z_{s}');
  narginchk(0, 3);
  if nargin > 0
    xlabel(varargin{1});
  else
    xlabel('x');
  end
  if nargin > 1
    ylabel(varargin{2});
  else
    ylabel('y');
  end
  if nargin > 2
    zlabel(varargin{3});
  else
    zlabel('z');
  end
end
