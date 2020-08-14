function info = DBRinfo(n1, n2, varargin)
  % Computes DBR related information.
  % Usage:
  %   DBRinfo(n1, n2)
  %   DBRinfo(n1, n2, 't1', 1.1, 't2', 3)
  %   DBRinfo(n1, n2, 'a', 4.1)
  %   DBRinfo(n1, n2, 'wavelength', 0.637)
  % Required positional arguments:
  %   n1: refractive index of layer 1
  %   n2: refractive index of layer 2
  % Named parameters:
  %   wavelength: wavelength to reflect
  %   t1: thickness of layer 1
  %   t2: thickness of layer 2
  %   a: thickness of a unit-cell (layer 1 + layer 2)
  %
  % Note: The bot/mid/top-gap values are normalized, i.e. omega/(2pi*c0/a) = a/lambda.
  %
  % TODO: create GUI
  % TODO: support more parameter sets
  % TODO: return normalized t1,t2, etc + bot/mid/top-gap values in real+normalized freqs+wavelengths (maybe as list for easy use with vline)
  
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

  info.epsilon1 = (info.n1).^2;
  info.epsilon2 = (info.n2).^2;
  info.delta_epsilon = abs(info.epsilon2 - info.epsilon1);
  info.approximate.criteria1 = info.delta_epsilon ./ min(info.epsilon1, info.epsilon2); % This should be << 1.

  % check if general DBR
  general_DBR = true;
  if ~isnan(info.t1) && ~isnan(info.t2)
    info.a = info.t1 + info.t2;
  elseif ~isnan(info.t1) && ~isnan(info.a)
    info.t2 = info.a - info.t1;
  elseif ~isnan(info.t2) && ~isnan(info.a)
    info.t1 = info.a - info.t2;
  else
    general_DBR = false;
  end

  if general_DBR
    info.approximate.midgap = info.a ./ ( 2*(info.n1 .* info.t1 + info.n2 .* info.t2) );
    info.approximate.criteria2 = min(info.t1, info.t2) ./ info.a; % This should be "small", but logically will always be in [0,1] or even [0,0.5] with current definition.
    info.approximate.gapsize_relative = info.approximate.criteria1 * sin(pi.*(info.t1)./(info.a)) ./ pi;
    info.approximate.wavelength = info.a ./ info.approximate.midgap;
  elseif isnan(info.t1) && isnan(info.t2)
    % quarter-wave stack
    info.approximate.midgap = (info.n1 + info.n2) ./ (4 * info.n1 .* info.n2);
    info.approximate.gapsize_relative = (4/pi) * asin(abs( (info.n1 - info.n2) ./ (info.n1 + info.n2) ));
    if ~isnan(info.wavelength)
      info.t1 = info.wavelength ./ (4*info.n1);
      info.t2 = info.wavelength ./ (4*info.n2);
      info.a = info.t1 + info.t2;
    elseif ~isnan(info.a)
      info.wavelength = info.a ./ ( (1 ./ (4*info.n1)) + (1 ./ (4*info.n2)) );
      info.t1 = info.wavelength ./ (4*info.n1);
      info.t2 = info.wavelength ./ (4*info.n2);
    end
  else
    error('unsupported parameter set');
  end
  info.approximate.gapsize_absolute = info.approximate.gapsize_relative .* info.approximate.midgap;
  info.approximate.botgap = info.approximate.midgap - 0.5*info.approximate.gapsize_absolute;
  info.approximate.topgap = info.approximate.midgap + 0.5*info.approximate.gapsize_absolute;
  info.approximate.gap_points_wavelength = [info.a./info.approximate.topgap, info.a./info.approximate.midgap, info.a./info.approximate.botgap];
  info.t1_over_a = info.t1/info.a;
  info.t2_over_a = info.t2/info.a;
  
  % if info.approximate.criteria1 >= 1
      % warning('Criteria 1 not met: delta(epsilon)/epsilon > 1. Approximation only valid for delta(epsilon)/epsilon << 1.\ndelta(epsilon)/epsilon=%.2f', info.approximate.criteria1);
  % end
  if ~any(isnan([info.n1, info.n2, info.t1, info.t2]))
    % new gap edge values, found by solving the exact equation numerically
    info.solved.botgap = DBR_bands_getOmega(pi./(info.t1+info.t2), info.n1, info.n2, info.t1, info.t2, 1);
    info.solved.topgap = DBR_bands_getOmega(pi./(info.t1+info.t2), info.n1, info.n2, info.t1, info.t2, 2);
    info.solved.midgap = (info.solved.botgap + info.solved.topgap)./2;
    info.solved.gap_points_wavelength = [info.a./info.solved.topgap, info.a./info.solved.midgap, info.a./info.solved.botgap];
    info.solved.gapsize_absolute = info.solved.topgap - info.solved.botgap;
    info.solved.gapsize_relative = info.solved.gapsize_absolute ./ info.solved.midgap;
    info.solved.wavelength = info.a./info.solved.midgap;
  end

end
