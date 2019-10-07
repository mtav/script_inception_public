clc;
clear all;
Xini = 3.3;
Xend = 9.3;
Xres = 0.1;

Plot_position = 8.5;

[FileName_Dark,PathName_Dark] = uigetfile('*.txt','Select the Dark file');
[FileName_Mirror,PathName_Mirror] = uigetfile('*.txt','Select the Mirror file');
[FileName_Sample,PathName_Sample] = uigetfile('*.txt','Select the Sample file');
[FileName_Wavelength,PathName_Wavelength] = uigetfile('*.txt','Select the Wavelength file');

Name_Dark = [PathName_Dark, FileName_Dark]
Name_Mirror = [PathName_Mirror, FileName_Mirror]
Name_Sample = [PathName_Sample, FileName_Sample]
Name_Wavelength = [PathName_Wavelength, FileName_Wavelength]

Data_Dark = load(Name_Dark);
Data_Mirror = load(Name_Mirror);
Data_Sample = load(Name_Sample);
Data_Wavelength = load(Name_Wavelength);

Data_Dark_Processed = repmat(Data_Dark(:,1),1,size(Data_Mirror,2));

Data_Ref = (Data_Sample - Data_Dark_Processed)./(Data_Mirror - Data_Dark_Processed);

Xposition = Xini:Xres:Xend;
Ylambda = Data_Wavelength;

figure(); hold on;
subplot(2,2,1);
imagesc(Data_Dark_Processed);
title('Data Dark Processed');

subplot(2,2,2);
imagesc(Data_Mirror);
title('Data Mirror');

subplot(2,2,3);
imagesc(Data_Sample);
title('Data Sample');

subplot(2,2,4);
imagesc(Xposition, Ylambda, Data_Ref, [0,1]);
title('Normalized');
