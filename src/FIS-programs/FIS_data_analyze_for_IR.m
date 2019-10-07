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

Name_Dark = [PathName_Dark, FileName_Dark];
Name_Mirror = [PathName_Mirror, FileName_Mirror];
Name_Sample = [PathName_Sample, FileName_Sample];
Name_Wavelength = [PathName_Wavelength, FileName_Wavelength];

Data_Dark = load(Name_Dark);
Data_Mirror = load(Name_Mirror);
Data_Sample = load(Name_Sample);
Data_Wavelength = load(Name_Wavelength);

Data_Dark_Processed = repmat(Data_Dark(:,1),1,size(Data_Mirror,2));

Data_Ref = (Data_Sample - Data_Dark_Processed)./(Data_Mirror - Data_Dark_Processed);

Xposition = Xini:Xres:Xend;
Ylambda = Data_Wavelength;

figure();
imagesc(Data_Dark_Processed);
figure();
imagesc(Data_Mirror);
figure();
imagesc(Data_Sample);
figure();
imagesc(Xposition, Ylambda, Data_Ref, [0,1]);
figure();
plot(Ylambda, Data_Ref(:,int64((Plot_position - Xini)/Xres)));
ylim([0,1]);

%  fid=fopen('p23.5_2_50_position8.5_spol_2.txt','w');
%  fprintf(fid, '%f %f \n', [Ylambda, Data_Ref(:,int64((Plot_position - Xini)/Xres))]');
%  fclose(fid);
