close all;
clear all;
plotProbe_CLI('p01_id_.prn', 2);
subplot(1,2,1);

plotSnapshot('xa_id_00.prn', 'column', 3, 'contourFile', 'x1_id_01.prn');
plotSnapshot('yb_id_00.prn', 'column', 3, 'contourFile', 'y2_id_01.prn');
plotSnapshot('zc_id_00.prn', 'column', 3, 'contourFile', 'z3_id_01.prn');

plotSnapshot('xa_id_05.prn', 'column', 3, 'contourFile', 'x1_id_01.prn');
plotSnapshot('yb_id_05.prn', 'column', 3, 'contourFile', 'y2_id_01.prn');
plotSnapshot('zc_id_05.prn', 'column', 3, 'contourFile', 'z3_id_01.prn');

plotSnapshot('xa_id_09.prn', 'column', 3, 'contourFile', 'x1_id_01.prn');
plotSnapshot('yb_id_09.prn', 'column', 3, 'contourFile', 'y2_id_01.prn');
plotSnapshot('zc_id_09.prn', 'column', 3, 'contourFile', 'z3_id_01.prn');
