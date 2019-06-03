function batchReadPRN(folder, snapshot_col, probe_col)

% DEPRECATED. Replaced by analyzePRN.

% batchReadPRN(folder,infilename, snapshot_col, probe_col)
% ex: batchReadPRN(folder,infilename, 3, 2)
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
filesP=dir([folder,'\p*.prn']);

%Time Ex Ey Ez Hx Hy Hz
colnumP = probe_col; % 

for m=1:length(filesP)
    filename=[folder,'\',filesP(m).name];
    [header, data]=readPrnFile(filename);    
    plot(data(:,1)*1e-9,data(:,colnumP))
    title([filesP(m).name,'  ',header{colnumP}]);
    xlabel('time (ns)');
    imageName=[filename,'_',header{colnumP},'.png'];
    saveas(gcf,imageName,'png');
    saveas(gcf,[imageName,'.fig'],'fig');
    
    
    dt=1e-12*(data(2,1)-data(1,1));  % Normally the data in probe file is in values of 1e*18 seconds
    [Y,lambda]=bFFT(data(:,colnumP),dt);
    Mag=2*abs(Y);
    plot(lambda,Mag);
    
    aver=sum(Mag)/length(Mag);
    delta=(max(Mag)-aver)/3;

    if (delta<0)
        return;
    end

    peaks=peakdet(Mag, delta/3,lambda);

    indMax=min(find(lambda==min(peaks(:,1)))+150,length(lambda));
    indMin=max(find(lambda==max(peaks(:,1)))-150,1);

    wavelength=1e3*lambda(indMin:indMax); %Unit of wavelength is nm.
    Mag=Mag(indMin:indMax);
    figure(2);hold off;
    plot(wavelength,Mag);
    
    title([filesP(m).name,' ',header{colnumP},'  Spectrum at Timestep:',num2str(length(data))])
    xlabel('Wavelength (nm)')
    ylabel('Mag')
    
    imageName=[filename,'_probeFFT_',header{colnumP},'.png'];
    saveas(gcf,imageName,'png');
    saveas(gcf,[imageName,'.fig'],'fig');
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