function info = DBRinfo(n1, n2, varargin)
  % TODO: create GUI
  % TODO: support more parameter sets
  % TODO: return normalized t1,t2, etc + bot/mid/topgap values in real+normalized freqs+wavelengths (maybe as list for easy use with vline)
  
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'n1', @isnumeric);
  p = inputParserWrapper(p, 'addRequired', 'n2', @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'wavelength', NaN, @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 't1', NaN, @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 't2', NaN, @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'a', NaN, @isnumeric);
  p = inputParserWrapper(p, 'parse', n1, n2, varargin{:});
  
  info = struct();
  info.n1 = p.Results.n1;
  info.n2 = p.Results.n2;
  
  info.wavelength = p.Results.wavelength;
  info.t1 = p.Results.t1;
  info.t2 = p.Results.t2;
  info.a = p.Results.a;
  
  if ~isnan(info.t1) && ~isnan(info.t2)
    % general DBR
    if isnan(info.a)
      info.a = info.t1 + info.t2;
    end
    info.midgap = info.a ./ ( 2*(info.n1 .* info.t1 + info.n2 .* info.t2) );
    info.epsilon1 = (info.n1).^2;
    info.epsilon2 = (info.n2).^2;
    info.delta_epsilon = abs(info.epsilon2 - info.epsilon1);
    info.criteria1 = info.delta_epsilon ./ min(info.epsilon1, info.epsilon2);
    info.criteria2 = min(info.t1, info.t2) ./ info.a;
    info.gapsize_relative = info.criteria1 * sin(pi.*(info.t1)./(info.a)) ./ pi;
  elseif isnan(info.t1) && isnan(info.t2)
    % quarter-wave stack
    info.midgap = (info.n1 + info.n2) ./ (4 * info.n1 .* info.n2);
    info.gapsize_relative = (4/pi) * asin(abs( (info.n1 - info.n2) ./ (info.n1 + info.n2) ));
    if ~isnan(info.wavelength)
      info.t1 = info.wavelength ./ (4*info.n1);
      info.t2 = info.wavelength ./ (4*info.n2);
      info.a = info.t1 + info.t2;
    end
  else
    error('unsupported parameter set');
  end
  info.gapsize_absolute = info.gapsize_relative .* info.midgap;
  info.botgap = info.midgap - 0.5*info.gapsize_absolute;
  info.topgap = info.midgap + 0.5*info.gapsize_absolute;
  info.t1_over_a = info.t1/info.a;
  info.t2_over_a = info.t2/info.a;
  info.gap_points_wavelength = [info.a./info.topgap, info.a./info.midgap, info.a./info.botgap];
end
