
mD='O:\matlab\Meep\BFDTD';
res=100;

fs=dir([mD,'\*snapshot*.h5']);

dsn1='hz-arg';
dsn2='hz-mag';

Data_arg=[];
Data_mag=[];
 snapNum=[];

for m=1:length(fs)
    f=[mD,'\',fs(m).name];
    
    [match,b]=regexp(f,'snapshot-(-?\d*\.?\d*)','match','tokens');
    str=b{1}{1};
    
    snapNum=[snapNum,str2num(str)];
    
    Data_arg=[Data_arg,hdf5read(f,dsn1)];
    Data_mag=[Data_mag,hdf5read(f,dsn2)];
%     plot(data_arg)
end

[snapNum,k]=sort(snapNum);
Data_arg=Data_arg(:,k);
Data_mag=Data_mag(:,k);

y=(0:size(Data_arg,1)-1)/res;
x=(0:size(Data_arg,2)-1)/res;

imagesc(x,y,Data_mag)
% imagesc(Data_arg)

% axis equal

lambdaLow=0.60 %0.62; %set min lamda  0.90    GaAs or Si ? = 526.39 nm – 549.00 nm
lambdaHigh=1.20; %set max lamda  0.98         GaP:       ? = 505.2892  nm ~ 519.8683 nm
atEvery=0.025;
fieldComp='ex';


locaLoutFile=dir([mD,'\*.out']);
locaLoutFile=[mD,'\',locaLoutFile(1).name];
fulltext = fileread(locaLoutFile);
[a,b]=regexp(fulltext, 'on time step (\d*) (time=(\d*\.?\d*)?','match','tokens','once');
dt=str2num(b{2})/str2num(b{1});
    
atEvery=max(round(atEvery/dt),1)*dt;
atEvery=0.005
dt=0.005;
pfs=dir([mD,'\*probe*.h5']);
for m=1:length(pfs)
    f=[mD,'\',pfs(m).name];
    
%     [match,b]=regexp(f,'snapshot-(-?\d*\.?\d*)','match','tokens');
%     str=b{1}{1};
    
%     snapNum=[snapNum,str2num(str)];
    
    field=hdf5read(f,fieldComp);
    harminvDataFile=[f,'_',fieldComp,'.dat'];
    fid=fopen(harminvDataFile,'w+');
    fprintf(fid,'%2.8e\r\n',field(:));
    fclose(fid);
   
    [lambdaH,Q,outFile,err,minErrInd]=doHarminv(harminvDataFile,dt,lambdaLow*c0,lambdaHigh*c0);
    lambdaH=lambdaH/c0;
    
    [fftin,lambda]=bFFT(field,atEvery/c0);
    Mag=2*abs(fftin);
    
    aver=sum(Mag)/length(Mag);
    delta=(max(Mag)-aver)/3;
    peaks=peakdet(Mag, delta/3,lambda);

    figure(2);clf
    plot(1e3*lambda,Mag,'.-r')
    
    xlim(1e3*[lambdaLow lambdaHigh])
    
    Qs=zeros(size(peaks,1),1);
    for s=1:size(peaks,1)
        try
            figure(2); hold on;
            plot(1e3*peaks(s,1),peaks(s,2),'r*')
            [indS,val]=closestInd(lambdaH,peaks(s,1));
            text(1e3*val,peaks(s,2),[num2str(1e3*val,'%2.2f'),'nm',13,10,'Q=',num2str(Q(indS))],'FontSize',14);
            Qs(s)=Q(indS);
        catch
        end
    end
    
    saveas(gcf,[f,'_',fieldComp,'.png'],'png')
            
end






