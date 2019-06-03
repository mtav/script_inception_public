%h=plotBands(data, name)
%-----------------------
%
%Plot the frequency bands.
%
% data   band structure (see 'readBands')
% name   window title
% w      figure handle
%
function w=plotBands(data, name)
if ~nargin
   error('Unknown or undefined argument.');
end;
flag=isbands(data);
if flag > 7
   error('Band structure is corrupt.');
end;
if flag > 3
   fprintf('Band structure is damaged.\n');
end;
data=scale(data);          % scale k axis
a.Box='on';                % open figure
a.FontSize=15;
a.Layer='top';
a.LineStyleOrder='-';
a.NextPlot='replacechildren';
a.Position=[0.13 0.08 0.84 0.88];
a.TickDir='out';
a.TickDirMode='manual';
a.XLimMode='manual';
a.XTickLabelMode='manual';
a.XTickMode='manual';
w.IntegerHandle='off';
w.MinColormap=4;
w.NextPlot='replacechildren';
w.NumberTitle='off';
w.Position=[100 100 500 400];
w.Tag='Frequency bands';
if nargin < 2 | ~ischar(name)
   w.Name=w.Tag;
else
   w.Name=name;
end;
w=figure(w);
a=axes(a,'Parent',w);
ylabel('f [c/a]','Parent',a); % draw
set(a,'XLim',[data.scale(data.edges(1)) data.scale(data.edges(length(data.edges)))],'XTick',data.scale(data.edges),'XTickLabel',data.ticks,'YLimMode','auto');
h=line(data.scale,data.bands,'Parent',a,'Color',[0.75 0 0]);
t=line(repmat(data.scale(data.edges(2:length(data.edges)-1)),1,2)',repmat(get(a,'YLim'),length(data.edges)-2,1)','Parent',a,'Color',[0.75 0.75 0.75]);
set(a,'Children',[h;t],'UserData',t);
