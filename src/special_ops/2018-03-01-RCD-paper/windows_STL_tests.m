%-- 29/01/2018 12:59 --%
ls
get_c0
userpath#
userpath
startup
edit startup
%-- 30/01/2018 11:20 --%
get_c0
startup
get_c0
calculateModeVolume_plotMaxDebug
edit calculateModeVolume_plotMaxDebug
%-- 30/01/2018 15:47 --%
get_c0
postprocessor
test_calculateModeVolume_plotMaxDebug
filesep
['*/part_*', '/*.inp']
['*', filesep, 'part_*', filesep, '*.inp']
fullfile('*', 'part_*', '*.inp')
help fullfile
fullfile('*', 'part_*', '*.inp')
test_calculateModeVolume_plotMaxDebug
a=0
isempty(a)
isfloat(a)
isscalar(a)
edit uipickfiles
type(a)
class(a)
test_calculateModeVolume_plotMaxDebug
cd C:\Development\script_inception_public\data\MV-test\
test_calculateModeVolume_plotMaxDebug
%-- 30/01/2018 16:21 --%
test_calculateModeVolume_plotMaxDebug
cd C:\Development\script_inception_public\data\MV-test\
test_calculateModeVolume_plotMaxDebug
get_c0
postprocessor
%-- 02/02/2018 16:24 --%
cd E:\RCD-paper-2018-02-01\FIGs-4ANONYMIZED\Data\09102017\RCD111-size=10x10x10-n_defect=3.30.n_crystal=1.00.n_backfill=3.30-defectPos=2.0-sphere\0.100a\Emod2
which print
help saveas_fig_and_png
edit saveas_fig_and_png
saveas_fig_and_png(gcf, 'Emode2_defect_mask_z.v3')
%-- 05/02/2018 10:37 --%
cd E:\RCD-paper-2018-02-01\FIGs-4ANONYMIZED\Data\09102017\RCD111-size=10x10x10-n_defect=3.30.n_crystal=1.00.n_backfill=3.30-defectPos=2.0-sphere\0.100a\Emod2
view(2)
%-- 05/02/2018 18:05 --%
get_co
get_c0
postprocessor
%-- 14/02/2018 12:28 --%
get_c0
stlwrite
surftostl
stlwrite
startup
stlwrite
stlwrite2
surf2stl
help stlwrite
tmpvol = false(20,20,20);
tmpvol(8:12,8:12,5:15) = 1;
fv = isosurface(~tmpvol, 0.5);
stlwrite('test.stl',fv)
p = patch(fv)
lighting gouraud
camlight
p.FaceColor = 'red';
p.EdgeColor = 'none';
view(2)
12.5-7.5
view([0,0,1])
view([0,1,0])
15.5-4.5
zlabel('z')
help stlwrite
%8:12,8:12,5:15
12-8
15-5
(8+12)/2
(5+15)/2
[X,Y] = deal(1:40);
Z = peaks(40);
stlwrite('test.stl',X,Y,Z,'mode','ascii')
surf(X,Y,Z)
help stlwrite
cVals = fv.vertices(fv.faces(:,1),3);
cLims = [min(cVals) max(cVals)];
nCols = 255;  cMap = jet(nCols);
fColsDbl = interp1(linspace(cLims(1),cLims(2),nCols),cMap,cVals);
fCols8bit = fColsDbl*255;
stlwrite('testCol.stl',fv,'FaceColor',fCols8bit)
patch(fv)
lighting gouraud
camlight
stlwrite2
help stlwrite2
help stlwrite
help stlwrite2
tmpvol = zeros(20,20,20);
tmpvol(8:12,8:12,5:15) = 1;
fv = isosurface(tmpvol, 0.99);
stlwrite('test.stl',fv)
help stlwrite
help stlwrite2
[X,Y] = deal(1:40);
Z = peaks(40);
stlwrite('test.stl',X,Y,Z,'mode','ascii')
help surf2stl
surf2stl('test.stl',1,1,peaks)
peaks
48/6
doc peaks
cd E:\RCD-paper-2018-02-01\FIGs-4ANONYMIZED\Data\09102017\RCD111-size=10x10x10-n_defect=3.30.n_crystal=1.00.n_backfill=3.30-defectPos=2.0-sphere\0.100a\Emod2
f=gcf
findobj('Type', 'patch');
findobj('Type', 'line');
a=gca
findall(a,'-property','xdata')
[p1,p2,p3,p4]=findall(a,'-property','xdata');
p1,p2,p3,p4=findall(a,'-property','xdata');
p=findall(a,'-property','xdata');
p
p[1]
p(1)
p(2)
p(3)
p(4)
p(1)
p(1).FaceColor=[0,0,0]
p(1).FaceColor=[1,0,0]
p(2)
help surf2stl
help stlwrite2
stlwrite('Emode2_defect_mask_x.p1.stl',p(1))
tmpvol = zeros(20,20,20);
tmpvol(8:12,8:12,5:15) = 1;
fv = isosurface(tmpvol, 0.99);
class(fv)
fv
p(1)
class(p(1))
help stlwrite2
help stlwrite
stlwrite('Emode2_defect_mask_x.p1.stl',p(1))
stlwrite2('Emode2_defect_mask_x.p1.stl',p(1))
p1=p(1)
p1
p1.Vertices;
p1.Faces;
p1.Face;
p1.Fa;
p1.Face
fv
fv{:}
parseInputs
stlwrite2('Emode2_defect_mask_x.p1.stl',p(1))
p3=p(3)
fv.faces=p3.Faces;
fv.vertices=p3.Vertices;
stlwrite2('Emode2_defect_mask_x.p3.stl',fv)
fv1.faces=p1.Faces;
fv1.vertices=p1.Vertices;
stlwrite2('Emode2_defect_mask_x.p1.stl',fv1)
fv2.faces=p(2).Faces;fv2.vertices=p(2).Vertices;
fv3.faces=p(3).Faces;fv3.vertices=p(3).Vertices;
fv4.faces=p(4).Faces;fv4.vertices=p(4).Vertices;
fv1.faces=p(1).Faces;fv1.vertices=p(1).Vertices;
stlwrite2('Emode2_defect_mask_x.p1.stl',fv1)
stlwrite2('Emode2_defect_mask_x.p2.stl',fv2)
stlwrite2('Emode2_defect_mask_x.p3.stl',fv3)
stlwrite2('Emode2_defect_mask_x.p4.stl',fv4)
p1
isstruct(p1)
doc isstruct
class(p1)
isa(p1,'Patch')
isa(p1,'matlab.graphics.primitive.Patch
')
isa(p1,'matlab.graphics.primitive.Patch')
isstruct(p1)
isobject(p1)
stlwrite2('test.stl',p1)
isfield(p1,{'vertices','faces'})
isfield(p1,{'vertices','Faces'})
isfield(p1,{'Vertices','Faces'})
p1.Vertices
stlwrite2('test.stl',p1)
stlwrite2('p1.stl',p(1))
stlwrite2('p2.stl',p(2))
stlwrite2('p3.stl',p(3))
stlwrite2('p4.stl',p(4))
p=findall(a,'-property','xdata');
stlwrite2('Emode2_defect_mask_x.p1.stl',fv1)
stlwrite2('Emode2_defect_mask_x.p1.stl',p(1))
stlwrite2('Emode2_defect_mask_x.p2.stl',p(2))
stlwrite2('Emode2_defect_mask_x.p3.stl',p(3))
stlwrite2('Emode2_defect_mask_x.p4.stl',p(4))
%saveas_fig_and_png(gcf, 'Emode2_defect_mask_z.v3')
view([0,0,1])
view([1,0,0])
view([0,0,1])
doc lightning
camlight('headlight')
camlight('right')
camlight('left')
delete(findall(gcf,'Type','light'))
camlight('headlight')
delete(findall(gcf,'Type','light'))
camlight('right')
delete(findall(gcf,'Type','light'))
%-- 17/02/2018 14:57 --%
