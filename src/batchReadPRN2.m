function batchReadPRN2(folder, id_list, snapshot_col, probe_col)

% DEPRECATED. Replaced by analyzePRN.

% batchReadPRN(folder, id_list, snapshot_col, probe_col)
% ex: batchReadPRN2('pillar_M2754_0_10', [62,71,80,89], 3, 2)
%
% invalid: batchReadPRN2(folder,infilename, 3, 2)
% invalid: batchReadPRN2('pillar_M2754_0_10', ['p62id.prn','p71id.prn','p80id.prn','p89id.prn'], 3, 2)
%
% snapshot_col:
%1 x
%2 z
%3 Exmod
%4 Exre
%5 Exim
%6 Eymod
%7 Eyre
%8 Eyim
%9 Ezmod
%10 Ezre
%11 Ezim
%12 Hxmod
%13 Hxre
%14 Hxim
%15 Hymod
%16 Hyre
%17 Hyim
%18 Hzmod
%19 Hzre
%20 Hzim
% probe_col:
%1 Time
%2 Ex
%3 Ey
%4 Ez
%5 Hx
%6 Hy
%7 Hz

TEOnly=0;

if nargin==0
    folder=uigetdir('D:\Simulations\BFDTD');
  snapshot_col=3;
  probe_col=2;
  id_list=[62,71,80,89];

end

clf

isRecord=0;
colnum = snapshot_col;  %3 Exmod 6Eymod 15HyMod 

files=[];
%snapshot files
% files=[files;dir([folder,'\x*.prn'])];
% files=[files,;dir([folder,'\y*.prn'])];
% files=[files,;dir([folder,'\z*.prn'])];

numFiles=length(files);
figure(1)
if (isRecord)
    mov=avifile([projectFolder,filePrefix,'6.avi'],'fps',4,'quality',100,'compression','Cinepak');
end

for m=1:1:numFiles
    filename=[folder,'\',files(m).name];
    [header, data]=readPrnFile(filename);
    
    colx=data(:,1);
    u=unique(colx);
    nx=length(u);
    ny=length(colx)/nx;

    x=data(1:ny:end,1);
    y=data(1:ny,2);
    
    
    Field=(reshape(data(:,colnum),ny,nx));
%     figure(1)
%     set(gcf,'Position',[0,0, 2*size(Field,2)/size(Field,1)*800, 800 ])
    dx=x(2)-x(1);
    if TEOnly && files(m).name(1)~='x'
        xAx=[x,x+max(x)+dx]; xAx=xAx(1:end-1);
        imagesc(y,xAx,[Field,fliplr(Field(:,1:end-1))]');
        colorbar
    else
        if files(m).name(1)=='x'
            imagesc(y,x,Field');
        else
            imagesc(x,y,Field);
        end
    end
%     axis equal
%     imagesc(Field);
    
    title([files(m).name,'  ',header{colnum}]);
    xlabel('microns')
    ylabel('microns')
    set(gca,'YDir','normal')
    
    imageName=[filename,'_',header{colnum},'.png'];
    saveas(gcf,imageName,'png');
    
    pause(.2)
    if (isRecord)
        F = getframe(gca);
        mov = addframe(mov,F);
        imageName=[filename,'.png'];
        
    end
end

if (isRecord)
    mov=close(mov);
end

clf

%probe files
filesP=dir([folder,'\p*id.prn']);
  % id_list
  % p+id_list+id.prn
  % for i=1:length(id_list)
  % ['p',num2str(id_list(2)),'id.prn']

%Time Ex Ey Ez Hx Hy Hz
colnumP = probe_col; % 

% for m=1:length(filesP)
for m=1:length(id_list)
    % filename=[folder,'\',filesP(m).name];
  basename=['p',num2str(id_list(m)),'id'];
    filebasename=[folder,'\\',basename];
    [header, data]=readPrnFile([filebasename,'.prn']);    

  disp(['processing ',filebasename,'.prn'])

    disp('	figure 1')
    figure(1);hold off;
    plot(data(:,1)*1e-9,data(:,colnumP));
    title([basename,'  ',header{colnumP}]);
    xlabel('time (ns)');
    imageName=[folder,'\\',basename,'_',header{colnumP}];
    saveas(gcf,[imageName,'.png'],'png');
    saveas(gcf,[imageName,'.fig'],'fig');
    
  %WARNING: The timestep is considered to be constant here!!!
    dt=1e-12*(data(2,1)-data(1,1));  % Normally the data in probe file is in values of 1e*18 seconds
    disp('	fourier transform start')
    [bFFT_output,b_lambda] = bFFT(data(:,colnumP),dt);
    [cFFT_output,c_lambda] = calcFFT(data(:,colnumP),dt,2^19);
    disp('	fourier transform end')

    %calculate magnitude of fft
    b_y_mag = abs(bFFT_output);
    %calculate power of fft
    b_y_pow = bFFT_output.* conj(bFFT_output);

    % b_Mag=2*abs(bFFT_output);
    % b_Mag=b_y_mag;
    b_Mag=b_y_pow;

    %calculate magnitude of fft
    c_y_mag = abs(cFFT_output);
    %calculate power of fft
    c_y_pow = cFFT_output.* conj(cFFT_output);

    % c_Mag=2*abs(cFFT_output);
    % c_Mag=c_y_mag;
    c_Mag=c_y_pow;
  
    disp('	figure 2')
    figure(2);hold off;
    plot(1e3*b_lambda,b_Mag,'-ro');
  hold on;
    plot(1e3*c_lambda,c_Mag,'-b+');
  
  b_wavelength=1e3*b_lambda;
  c_wavelength=1e3*c_lambda;
  
  fprintf('length(b_wavelength)=%d\n',length(b_wavelength));
  fprintf('length(c_wavelength)=%d\n',length(c_wavelength));
  fprintf('min(b_wavelength)=%E\n',min(b_wavelength));
  fprintf('min(c_wavelength)=%E\n',min(c_wavelength));
  fprintf('max(b_wavelength)=%E\n',max(b_wavelength));
  fprintf('max(c_wavelength)=%E\n',max(c_wavelength));

    title([basename,' ',header{colnumP},'  Spectrum at Timestep:',num2str(length(data))])
    xlabel('Wavelength (nm)');
    ylabel('Mag');

  filebasenameFFT=[folder,'\\',basename,'_probeFFT_',header{colnumP},'_full'];
    saveas(gcf,[filebasenameFFT,'.png'],'png');
    saveas(gcf,[filebasenameFFT,'.fig'],'fig');
    
  %===============================
  
    b_aver=sum(b_Mag)/length(b_Mag);
    b_delta=(max(b_Mag)-b_aver)/3;

  fprintf('b_delta=%E\n',b_delta);
  
    if (b_delta<0)
        return;
    end

  disp('	search for peaks')
  peaks = peakdet(b_Mag, b_delta/3);
  index_peaks = peaks(:,1);
  fprintf('index_peaks=%E\n',index_peaks);
    b_indMin = max(index_peaks(1)-150,1);
    b_indMax = min(index_peaks(length(index_peaks))+150,length(b_lambda));
  disp('	peaks located')

  % disp('	search for peaks')
    % peaks=peakdet(b_Mag, b_delta/3,b_lambda);
  % disp('	peaks located')

  %lambda is inverted!!! (sorted from big to small)
    % b_indMax=min(find(b_lambda==min(peaks(:,1)))+150,length(b_lambda));
    % b_indMin=max(find(b_lambda==max(peaks(:,1)))-150,1);
  
    b_wavelength=1e3*b_lambda(b_indMin:b_indMax); %Unit of wavelength is nm.
  b_wavelength=b_wavelength';
  
    b_Mag_zoom_1 = b_Mag(b_indMin:b_indMax);
  %===============================
  
    c_aver=sum(c_Mag)/length(c_Mag);
    c_delta=(max(c_Mag)-c_aver)/3;

  fprintf('c_delta=%E\n',c_delta);
  fprintf('c_delta-b_delta=%E\n',c_delta-b_delta);
  

    if (c_delta<0)
        return;
    end

  disp('	search for peaks')
  peaks = peakdet(c_Mag, c_delta/3);
  index_peaks = peaks(:,1);
  fprintf('index_peaks=%E\n',index_peaks);
    c_indMin = max(index_peaks(1)-150,1);
    c_indMax = min(index_peaks(length(index_peaks))+150,length(c_lambda));
  disp('	peaks located')

  % disp('	search for peaks')
    % peaks=peakdet(c_Mag, c_delta/3,c_lambda);
  % disp('	peaks located')

  %lambda is inverted!!! (sorted from big to small)	
    % c_indMax=min(find(c_lambda==min(peaks(:,1)))+150,length(c_lambda));
    % c_indMin=max(find(c_lambda==max(peaks(:,1)))-150,1);
  
    c_wavelength=1e3*c_lambda(c_indMin:c_indMax); %Unit of wavelength is nm.
  c_wavelength=c_wavelength';
  
    c_Mag_zoom_1 = c_Mag(c_indMin:c_indMax);
  %===============================
  
    figure(3);hold off;
    plot(b_wavelength,b_Mag_zoom_1,'-ro');
  hold on;
    plot(c_wavelength,c_Mag_zoom_1,'-b+');

  fprintf('length(b_wavelength)=%d\n',length(b_wavelength));
  fprintf('length(c_wavelength)=%d\n',length(c_wavelength));
  fprintf('min(b_wavelength)=%E\n',min(b_wavelength));
  fprintf('min(c_wavelength)=%E\n',min(c_wavelength));
  fprintf('max(b_wavelength)=%E\n',max(b_wavelength));
  fprintf('max(c_wavelength)=%E\n',max(c_wavelength));
    
    title([basename,' ',header{colnumP},'  Spectrum at Timestep:',num2str(length(data))]);
    xlabel('Wavelength (nm)');
    ylabel('Mag');
    
  filebasenameFFT=[folder,'\\',basename,'_probeFFT_',header{colnumP}];
    saveas(gcf,[filebasenameFFT,'.png'],'png');
    saveas(gcf,[filebasenameFFT,'.fig'],'fig');
  
  writePrnFile([filebasenameFFT,'.prn'],'wavelength Mag',[ b_wavelength, b_Mag_zoom_1 ]);

  
  %===============================
  disp('	search for peaks')
  peaks = peakdet(b_Mag, b_delta/3);
  disp('	peaks located')

  index_peaks = peaks(:,1);
  % lowest energy peak = highest lambda peak = lowest peak index = index_peaks(1)
    b_indMin = max(index_peaks(1)-150,1);
    b_indMax = min(index_peaks(1)+150,length(b_lambda));
    % indMax = min(index_peaks(length(index_peaks))+150,length(lambda));
  % indMin
  % indMax
  
    b_wavelength = 1e3*b_lambda(b_indMin:b_indMax); %Unit of wavelength is nm. (lambda is in mum)
  b_wavelength = b_wavelength';
  
    b_Mag_zoom_2 = b_Mag(b_indMin:b_indMax);
  %===============================
  disp('	search for peaks')
  peaks = peakdet(c_Mag, c_delta/3);
  disp('	peaks located')
  
  index_peaks = peaks(:,1);
  % lowest energy peak = highest lambda peak = lowest peak index = index_peaks(1)
    c_indMin = max(index_peaks(1)-150,1);
    c_indMax = min(index_peaks(1)+150,length(c_lambda));
    % indMax = min(index_peaks(length(index_peaks))+150,length(lambda));
  % indMin
  % indMax
  
    c_wavelength = 1e3*c_lambda(c_indMin:c_indMax); %Unit of wavelength is nm. (lambda is in mum)
  c_wavelength = c_wavelength';
  
    c_Mag_zoom_2 = c_Mag(c_indMin:c_indMax);
  %===============================
  
    figure(4);hold off;
    plot(b_wavelength,b_Mag_zoom_2,'-ro');
  hold on;
    plot(c_wavelength,c_Mag_zoom_2,'-b+');
    
    title([basename,' ',header{colnumP},'  Spectrum at Timestep:',num2str(length(data))]);
    xlabel('Wavelength (nm)');
    ylabel('Mag');
    
  % filebasenameFFT=[folder,'\\',basename,'_probeFFT_',header{colnumP}];
    % saveas(gcf,[filebasenameFFT,'.png'],'png');
    % saveas(gcf,[filebasenameFFT,'.fig'],'fig');
  
  % [basenameFFT,'.prn']
  % 'wavelength Mag'
  % wavelength
  % Mag
  % [ wavelength, Mag ]
  % writePrnFile([filebasenameFFT,'.prn'],'wavelength Mag',[ wavelength, Mag_zoom_1 ]);
  
  % length(data(:,colnumP))
  % data(2,1)-data(1,1)
  % dt
  
end

% if (exist('infilename'))
%     ind=max(strfind(infilename,'\'));
% %     InPathName=infilename(1:ind);
% %     [InFileName,InPathName] = uigetfile('*.prn','Select input prn-file',InPathName); 
% %     infilename=[InPathName,InFileName];
%     S21=GetS21(infilename,[folder,'\i3a00.prn']);
% else
%     [InFileName,InPathName] = uigetfile('*.prn','Select input prn-file','D:\fdtd');
%     infilename=[InPathName,InFileName];
% %     GetS21(infilename);
% end
%
