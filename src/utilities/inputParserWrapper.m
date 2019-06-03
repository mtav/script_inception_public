function parser = inputParserWrapper(parser, method, varargin)
  % Note: Octave does not yet support 'addParameter'. Use 'addParamValue' instead, even though it is deprecated in Matlab.
  % Note: addOptional does also not seem to be supported properly by Octave yet... :/
  if strcmp(method, 'addRequired')
    if inoctave() && octaveVersionLessThan(4)
      parser = parser.addRequired(varargin{:});
    else
      parser.addRequired(varargin{:});
    end
  end
  if strcmp(method, 'addOptional')
    if inoctave() && octaveVersionLessThan(4)
      parser = parser.addOptional(varargin{:});
    else
      parser.addOptional(varargin{:});
    end
  end
  if strcmp(method, 'addParamValue')
    if inoctave() && octaveVersionLessThan(4)
      parser = parser.addParamValue(varargin{:});
    else
      parser.addParamValue(varargin{:});
    end
  end
  if strcmp(method, 'addParameter')
    if inoctave() && octaveVersionLessThan(4)
      parser = parser.addParameter(varargin{:});
    else
      parser.addParameter(varargin{:});
    end
  end
  if strcmp(method, 'parse')
    if inoctave() && octaveVersionLessThan(4)
      parser = parser.parse(varargin{:});
    else
      parser.parse(varargin{:});
    end
  end
end
