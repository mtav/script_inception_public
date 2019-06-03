function w = plotDensity(data, varargin)
%function w = plotDensity(data, name, n, varargin)
  %w=plotDensity(data, name, n)
  %----------------------------
  %
  %Plot the density of states.
  %
  % data   band structure (see 'readBands')
  % name   window title
  % n      number of bins or zero for extrapolation
  %           if not specified, extrapolation is choosen
  %           whenever the velocity data is present, the
  %           number of bins is set automatically else.
  % w      figure handle
  %
  
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'data', @isstruct);
  p = inputParserWrapper(p, 'addParamValue', 'name', 'Density of states', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'n', [], @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'new_figure', true, @islogical);
  p = inputParserWrapper(p, 'parse', data, varargin{:});
  
  name = p.Results.name;
  n = p.Results.n;
  
  if ~nargin
     error('Unknown or undefined argument.');
  end;
  flag = isbands(data);
  if flag > 7
     error('Band structure is corrupt.');
  end;
  if flag > 3
     fprintf('Band structure is damaged.\n');
  end;
  %if nargin < 3
     %n=[];
  %end;
  [data, n] = density(data, n);  % compute density
  
  if p.Results.new_figure
    w = figure();
    a = axes('Parent', w);
  else
    w = gcf();
    a = gca();
  end
  %set(w, 'IntegerHandle', 'off');
  %set(w, 'MinColormap', 4);
  %set(w, 'NextPlot', 'replacechildren');
  %set(w, 'NumberTitle', 'off');
  set(w, 'Position', [100, 100, 500, 400]);
  %set(w, 'Tag','Density of states');
  %if nargin < 2 || ~ischar(name)
     %set(w, 'Name', get(w, 'Tag'));
  %else
     %set(w, 'Name', name);
  %end;
  set(w, 'Name', name);
  
  set(a, 'Box', 'on');
  set(a, 'FontSize', 15);
  set(a, 'Layer', 'top');
  set(a, 'LineStyleOrder', '-');
  %set(a, 'NextPlot', 'replacechildren');
  %set(a, 'Position', [0.13, 0.08, 0.84, 0.88]);
  set(a, 'TickDir', 'out');
  set(a, 'TickDirMode', 'manual');
  set(a, 'XLimMode', 'manual');
  set(a, 'XTickLabelMode', 'manual');
  set(a, 'XTickMode', 'manual');
  
  ylabel('f [c/a]','Parent',a); % draw
  if n
     h=barh(data.density(:,1),data.density(:,2),1);
     set(h,'EdgeColor',[0 0 0.5],'FaceColor',[0 0 0.75]);
  else
     j=10^ceil(log10(max(data.density(:,2))));
     i=10^floor(log10(max(0.001,min(data.density(:,2)))));
     set(a, 'XScale', 'log',...
     'XLim',[i j],...
     'XTickMode','auto',...
     'XTickLabelMode','auto');
     %set(a, 'Position',[0.13 0.1 0.84 0.86]);
     line([repmat(i,size(data.density,1),1) data.density(:,2)]',repmat(data.density(:,1),1,2)','Parent',a,'Color',[0 0 0.75]);
  end;
end
