%w=plotGaps(e, name)
%-------------------
%
%Plots the te and tm band gaps for a set of files
%computed at epsilon e and r/a=0.02:0.02:0.48.
%
% e      dielectric constant
% name   window title
% w      figure handle
%
function w=plotGaps(e, name)
if ~nargin
   error('Unknown or undefined argument.');
end;

a.Box='on';                % open figure
a.FontSize=15;
a.Layer='top';
a.LineStyleOrder='-';
a.NextPlot='replacechildren';
a.Position=[0.13 0.14 0.83 0.82];
a.TickDir='out';
a.TickDirMode='manual';
a.XLim=[0 0.5];
a.XLimMode='manual';
w.IntegerHandle='off';
w.MinColormap=4;
w.NextPlot='replacechildren';
w.NumberTitle='off';
w.Position=[100 100 500 400];
w.Tag='Gap map';
if nargin < 2 | ~ischar(name)
   w.Name=w.Tag;
else
   w.Name=name;
end;
w=figure(w);
a=axes(a,'Parent',w);
xlabel('r [a]','Parent',a);   % draw
ylabel('f [c/a]','Parent',a);
for r=1:24
   if r < 5
      data=sprintf('E=%d R=0.0%d',[e 2*r]);
   else
      data=sprintf('E=%d R=0.%d',[e 2*r]);
   end;
   data=readBands(data);
   for s=1:length(data)
      t=bandgaps(data{s});
      switch t.polarity
      case 'te'
         c=[1 0 0];        % red
         h=0.01;           % width
         o=0.01;           % x offset
      case 'tm'
         c=[0 0 1];        % blue
         h=0.01;
         o=0;
      otherwise
         c=[0 1 0];        % green
         h=0.02;
         o=0.01;
      end;
      t=t.gaps;
      for i=1:size(t,2)
         rectangle('EdgeColor','none','FaceColor',c,'Parent',a,'Position',[0.02*r-o t(1,i)*(1-t(2,i)/2) h prod(t(:,i))]);
      end;
   end;
end;
