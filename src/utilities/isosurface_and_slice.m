function isosurface_and_slice(X, Y, Z, V, varargin)

  % TODO: turn off edge lines? (octave+matlab)

  % create parser
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'X', @isnumeric);
  p = inputParserWrapper(p, 'addRequired', 'Y', @isnumeric);
  p = inputParserWrapper(p, 'addRequired', 'Z', @isnumeric);
  p = inputParserWrapper(p, 'addRequired', 'V', @isnumeric);
  p = inputParserWrapper(p, 'addOptional', 'isovalue', 0.5, @isnumeric);
  p = inputParserWrapper(p, 'addOptional', 'xslice', [], @isnumeric);
  p = inputParserWrapper(p, 'addOptional', 'yslice', [], @isnumeric);
  p = inputParserWrapper(p, 'addOptional', 'zslice', [], @isnumeric);
  p = inputParserWrapper(p, 'parse', X, Y, Z, V, varargin{:});

  figure; hold all;
  isosurface (X, Y, Z, V, p.Results.isovalue);
  slice(X, Y, Z, V, p.Results.xslice, p.Results.yslice, p.Results.zslice);
  xlabel('x');ylabel('y');zlabel('z');
  xlim([min(X(:)),max(X(:))]);
  ylim([min(Y(:)),max(Y(:))]);
  zlim([min(Z(:)),max(Z(:))]);
  colorbar;
  axis equal;
end
