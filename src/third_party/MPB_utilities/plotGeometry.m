%w=plotGeometry(item, r, name)
%-----------------------------
%
%Plots the crystal geometry.
%
% item      epsilon structure
% r         repetitions [x y]
% name      window title
% w         figure handle
%
function w=plotGeometry(item, r, name)
l=item.lattice(1:2,1:2);
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
         w.Name='Geometry';
      end;
   end;
end;
w.MenuBar='none';
w.NextPlot='replacechildren';
w.NumberTitle='off';
w.Position=[100 100 100 100];
w.Tag='Geometry';
w=figure(w);
colormap(gray(16));        % draw
project(w,l,item.data,r);
