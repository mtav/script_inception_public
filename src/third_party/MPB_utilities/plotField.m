%w=plotField(item, r, name)
%--------------------------
%
%Plots an electric or magnetic field.
%
% item      field structure
% r         repetitions [x y]
% name      window title
% w         figure handle
%
function w=plotField(item, r, name)
l=item.lattice(1:2,1:2);
e=0;
if isfield(item,'x')       % collect fields
   e=abs(item.x).^2;
end;
if isfield(item,'y')
   e=e+abs(item.y).^2;
end;
if isfield(item,'z')
   e=e+abs(item.z).^2;
end;
if nargin > 1 & isequal(size(r),[1 2])
   l=l.*[r;r]';
else
   r=[1 1];
end;
w.IntegerHandle='off';     % open figure
if nargin > 2 & ischar(name)
   w.Name=name;
else
   if isfield(item,'info')
      w.Name=item.info;
   else
      if isfield(item,'description')
         w.Name=item.description;
      else
         w.Name='Field';
      end;
   end;
end;
w.MenuBar='none';
w.NextPlot='replacechildren';
w.NumberTitle='off';
w.Position=[100 100 100 100];
w.Tag='Field';
w=figure(w);
colormap(jet(64));         % draw
project(w,l,sqrt(e),r);
