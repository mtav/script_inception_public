function h = waitbarSmart(varargin)
  % A smart waitbar wrapper, printing text if no GUI is available.
  h = waitbar(varargin{:});
  if ~is_gui_mode()
    progress = varargin{1};
    msg = '';
    if nargin>=2 && ischar(varargin{2})
      msg = varargin{2};
    elseif nargin>=3 && ischar(varargin{3})
      msg = varargin{3};
    end
    fprintf('%.2f%% %s\n', 100*progress, msg);
  end
end
