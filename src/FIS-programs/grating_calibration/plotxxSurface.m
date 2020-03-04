close all;
clear all;
Xini = 3.3;
Xend = 9.3;
Xres = 0.1;

Name_Sample = "C:\Development\script_inception_public\data\FIS-Measurements\FIS-IR\REF_Iris3ScanIllu105Obj40CUSTOM\Sample.txt";
Name_Wavelength = "C:\Development\script_inception_public\data\FIS-Measurements\FIS-IR\REF_Iris3ScanIllu105Obj40CUSTOM\W.txt";

Data_Sample = load(Name_Sample);
Data_Wavelength = load(Name_Wavelength);

Xposition = Xini:Xres:Xend;
midpoint = (Xposition(end)+Xposition(1))/2;
Ylambda = Data_Wavelength;
Xangle1 = FIS_PositionToAngle(Xposition, midpoint, 1.88*10, false);
Xangle2 = FIS_PositionToAngle(Xposition, midpoint, tan(deg2rad(1.88*10*3))/3, true);

% subplot(1,3,1);
% imagesc(Xposition, Data_Wavelength, Data_Sample);
subplot(1,2,1);
imagesc(Xangle1, Data_Wavelength, Data_Sample);
subplot(1,2,2);
imagesc(Xangle2, Data_Wavelength, Data_Sample);
% colorbar();

% xlabel('Position (mm)');
% ylabel('Wavelength (nm)');
vline(midpoint);

ax1 = gca(); % current axes
ax1_pos = ax1.Position; % position of first axes
ax2 = axes('Position',ax1_pos,...
    'XAxisLocation','top',...
    'YAxisLocation','right',...
    'Color','none', 'YColor', 'none');
xlim(getRange(Xangle1));
% title('Data Sample', 'Units', 'normalized', 'Position', [0.5, -0.2, 0]);
