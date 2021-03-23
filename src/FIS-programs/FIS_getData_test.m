% script to test FIS data collection
close all;
clear all;

DATADIR = fullfile(dirname(which('FIS_getData_test')), '../../data/FIS-Measurements/');
cd(DATADIR);
fprintf('working directory: %s\n', pwd);

cd(fullfile(DATADIR, 'FIS-VIS'));
fprintf('working directory: %s\n', pwd);
disp('=====');
data1 = FIS_getData_VIS('_Iris3Scan200Illu105Obj40Sample2_NoPol', 'Sample');
disp('=====');
data2 = FIS_getData_VIS('_Iris3Scan200Illu105Obj40Sample2_NoPol', 'Mirror');
disp('=====');
data3 = FIS_getData_VIS('_Iris3Scan200Illu105Obj40Sample2_NoPol', 'DarkBackground');

% plotTriplet(data1);
% plotTriplet(data2);
% plotTriplet(data3);
% plot123(data1, data2, data3);

cd(fullfile(DATADIR, 'FIS-IR'));
fprintf('working directory: %s\n', pwd);
disp('=====');
data4 = FIS_getData_IR_LineScan_SingleFileForLine('_Iris3ScanIllu105Obj40SingleFileForLine-LineScan/Sample.txt');
% plotTriplet(data4);
%FIS_plot2D(data4);
disp('=====');
data5 = FIS_getData_IR_LineScan_SingleFileForPoint('_Iris3ScanIllu105Obj40SingleFileForPoint-LineScan/SampleSingleFileForPoint-LineScanlog.txt');
% plotTriplet(data5);

disp('=====');
data6 = FIS_getData_IR_FullScan('_Iris3ScanIllu105Obj40SingleFileForPoint-FullScan/SampleSingleFileForPoint-LineScanlog.txt');
disp('=====');
data7 = FIS_getData_IR_FullScan('_Iris3ScanIllu105Obj40SingleFileForLine-FullScan/SampleSingleFileForPoint-LineScanlog.txt');

function commonsettings()
    xlim([3,9]);
    ylim([400, 800]);
    %caxis([0,1]);
    set(gca,'ColorScale', 'log');
    set(gca, 'YDir','normal');
    %set(gca, 'YDir','reverse');
end

function plot123(data1, data2, data3)
    figure;
    subplot(3,3,1);
    FIS_plot2D(data1, 'pcolor'); commonsettings();
    subplot(3,3,2);
    FIS_plot2D(data1, 'contour'); commonsettings();
    subplot(3,3,3);
    FIS_plot2D(data1, 'surf'); commonsettings();
    subplot(3,3,4);
    FIS_plot2D(data2, 'pcolor'); commonsettings();
    subplot(3,3,5);
    FIS_plot2D(data2, 'contour'); commonsettings();
    subplot(3,3,6);
    FIS_plot2D(data2, 'surf'); commonsettings();
    subplot(3,3,7);
    FIS_plot2D(data3, 'pcolor'); commonsettings();
    subplot(3,3,8);
    FIS_plot2D(data3, 'contour'); commonsettings();
    subplot(3,3,9);
    FIS_plot2D(data3, 'surf'); commonsettings();
end

function plotTriplet(data)
    figure;
    subplot(1,3,1);
    FIS_plot2D(data, 'pcolor');
    subplot(1,3,2);
    FIS_plot2D(data, 'contour');
    subplot(1,3,3);
    FIS_plot2D(data, 'surf');
end
