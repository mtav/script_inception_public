close all;
clear all;

swap_axes = false;

% test geometry drawing
cd('~/TEST/geometry_drawing');
plotSnapshot('filename', 'x1_id_01.prn', 'column', 3, 'drawGeometry', true, 'geofile', 'sim.geo', 'inpfile', 'sim.inp', 'swap_axes', swap_axes);

%cd('~/Pictures/snapshot-picture-test');
cd('~/Development/script_inception_public/testing/snapshot-picture-test');

% test plot types
%ret = plotSnapshot('filename', 'XY-small.prn', 'column', 3, 'createFigure', true, 'MainContourZposition', 42);
%ret = plotSnapshot('filename', 'XY-small.prn', 'column', 3, 'MainPlotType', 'surface', 'createFigure', true, 'MainContourZposition', 42);
%ret = plotSnapshot('filename', 'XY-small.prn', 'column', 3, 'MainPlotType', 'contour', 'createFigure', true, 'MainContourZposition', 42);
%ret = plotSnapshot('filename', 'XY-small.prn', 'column', 3, 'MainPlotType', 'contourAtZ', 'createFigure', true, 'MainContourZposition', 42);

% test surface and then contour plotting using two calls
ret_surface = plotSnapshot('filename', 'XY-small.prn', 'column', 3, 'createFigure', true, 'MainPlotType', 'surface', 'updateCaxis', true, 'swap_axes', swap_axes);
hold on;
ret_contour = plotSnapshot('filename', 'smiley-small.prn', 'column', 3, 'createFigure', false, 'MainPlotType', 'contourAtZ', 'MainContourZposition', 300, 'updateCaxis', false, 'swap_axes', swap_axes);

% reverse
ret_contour = plotSnapshot('filename', 'smiley-small.prn', 'column', 3, 'createFigure', true, 'MainPlotType', 'contourAtZ', 'MainContourZposition', 300, 'updateCaxis', false, 'swap_axes', swap_axes);
hold on;
ret_surface = plotSnapshot('filename', 'XY-small.prn', 'column', 3, 'createFigure', false, 'MainPlotType', 'surface', 'updateCaxis', true, 'swap_axes', swap_axes);

STOP

%  DIR='~/TEST/UniverseIsFullOfBalls/Z/'
%  snapshot_filename = 'zao_id_00.prn';

DIR='~/TEST/test_central_snapshots';

xsnap='x1_id_01.prn';
ysnap='y2_id_01.prn';
zsnap='z3_id_01.prn';

cd(DIR);

%  plotSnapshot(snapshot_filename, column, zlimits, handles, azimuth, hide_figures, imageSaveName, varargin)

% TODO: subplot support
%plotSnapshot(xsnap, 'column', 3, 'contourFile', xsnap);
%plotSnapshot(ysnap, 'column', 3, 'contourFile', ysnap);
%plotSnapshot(zsnap, 'column', 3, 'contourFile', zsnap);

%  plotSnapshot(snapshot_filename, 'column', 3, 'contourFile', esnap);

%  [esnap, esnap_basename] = fsnap_to_esnap(snapshot_filename);
%  [header, data, ux, uy] = readPrnFile(esnap);

DIR='~/TEST/mode_volume_validation/UniverseIsFullOfBalls/X';
esnap='x:1_id_01.prn';
fsnap='xcw_id_00.prn';

cd(DIR);
%plotSnapshot(esnap, 'column', 3, 'contourFile', esnap);
%plotSnapshot(fsnap, 'column', 3, 'contourFile', fsnap);

snapshot_filename = '';
DIR='~/TEST/mode_volume_validation/UniverseIsFullOfBalls/Y';
DIR='~/TEST/mode_volume_validation/UniverseIsFullOfBalls/Z';

cd('~/TEST/dipole+block');

esnap='x1_id_01.prn'
fsnap='xa_id_00.prn'
plotSnapshot(esnap, 'column', 3, 'contourFile', esnap);
plotSnapshot(fsnap, 'column', 3, 'contourFile', fsnap);

esnap='y2_id_01.prn'
fsnap='yb_id_00.prn'
plotSnapshot(esnap, 'column', 3, 'contourFile', esnap);
plotSnapshot(fsnap, 'column', 3, 'contourFile', fsnap);

esnap='z3_id_01.prn'
fsnap='zc_id_00.prn'
plotSnapshot(esnap, 'column', 3, 'contourFile', esnap);
plotSnapshot(fsnap, 'column', 3, 'contourFile', fsnap);

plotProbe_CLI('p01_id_.prn', 2);
