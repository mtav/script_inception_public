function colorbarLabel(handle_colorbar, txt, varargin)
  % function colorbarLabel(handle_colorbar, txt, varargin)
  %   labels the colorbar in an appropriate location (mainly because Octave does not yet support 'colorbar.Label')
  loc = lower(get(handle_colorbar, 'Location'));
  switch loc
    case 'eastoutside'
      %disp('Place the colorbar outside the plot to the right.  This is the default.');
      ylabel(handle_colorbar, txt, varargin{:});
    case 'east'
      %disp('Place the colorbar inside the plot to the right.');
      ylabel(handle_colorbar, txt, varargin{:});
    case 'westoutside'
      %disp('Place the colorbar outside the plot to the left.');
      ylabel(handle_colorbar, txt, varargin{:});
    case 'west'
      %disp('Place the colorbar inside the plot to the left.');
      ylabel(handle_colorbar, txt, varargin{:});
    case 'northoutside'
      %disp('Place the colorbar above the plot.');
      xlabel(handle_colorbar, txt, varargin{:});
    case 'north'
      %disp('Place the colorbar at the top of the plot.');
      xlabel(handle_colorbar, txt, varargin{:});
    case 'southoutside'
      %disp('Place the colorbar under the plot.');
      xlabel(handle_colorbar, txt, varargin{:});
    case 'south'
      %disp('Place the colorbar at the bottom of the plot.');
      xlabel(handle_colorbar, txt, varargin{:});
    otherwise
      error ('invalid value: loc = %s', loc);
  end
end
