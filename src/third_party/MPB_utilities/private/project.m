%project(w, l, f, r)
%-------------------
%
%Draws and project the geometry or a field.
%
% w      figure handle
% l      lattice vectors
% f      geometry or field
% r      repetition [x y]
%
function project(w, l, f, r)
rotate3d on;
n=size(f).*r;
x=repmat((0:1/n(1):1-1/n(1)),n(2),1)';
y=repmat((0:1/n(2):1-1/n(2)),n(1),1);
surf(x*l(1,1)+y*l(2,1),x*l(1,2)+y*l(2,2),repmat(f,r),'EdgeColor','none');
grid off;                  % modify axis
a.Box='off';
a.Color=[0.75 0.75 0.75];
a.CameraUpVector=[0 1 0];
a.Layer='top';
a.NextPlot='replacechildren';
a.Position=[0 0 1 1];
a.TickDir='out';
a.XTickLabel={};
a.YTickLabel={};
x=l(1:2,1:2)'*[0 0 1 1;0 1 0 1];
a.XLim=[min(x(1,:)) max(x(1,:))];
a.YLim=[min(x(2,:)) max(x(2,:))];
a.CameraPosition=[mean(a.XLim) mean(a.YLim) 16];
set(get(w,'CurrentAxes'),a);
set(w,'Position',[100 100 100*(a.XLim(2)-a.XLim(1)) 100*max(a.YLim(2)-a.YLim(1))]);
