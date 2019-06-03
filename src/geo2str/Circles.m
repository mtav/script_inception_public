clear all
magnification=35000
pixel=74.3/magnification %pixel size, is roughly 74.3/(magnification)

dw=20000 %dwell in 10ths of a microsecond
r=[];d=[];

fstr = fopen('membrane1_24_07.str','wt');
%write preamble in stream file
fprintf(fstr,'s\n');
fprintf(fstr,'15\n');%number of repetitions

%extract positions of objects and convert to streamfile units using the
%funtion readtextfile

tab = readtextfile('H:\membrane1_24_07.geo');
dim = size(tab);
ii = 1; block = 0;
while ii <= dim(1)
    tf=[]
    tf= strcmp(tab(ii,1:8),'CYLINDER')
    if tf,
        block=block+1;
        ii=ii+2;
        xc(block) = str2double(tab(ii,1:8)); ii=ii+2;
        zc(block) = str2double(tab(ii,1:8)); ii=ii+1;
        r(block) = str2double(tab(ii,1:8)); ii=ii+5;
    end
    ii=ii+1;
end

% put x and y coordinates in order of size
c2=[]
c2(:,1)=xc(1,:)'
c2(:,2)=zc(1,:)'
c2(:,3)=r(1,:)'
c2=sortrows(c2,1)

xc=c2(:,1)'
zc=c2(:,2)'
r=c2(:,3)'

xc=round(xc./pixel)+1000; %convert to pixel coordinates
zc=round(zc./pixel)+1000; %put pattern near centre of screen

%find repeated radii
ir=1
r2=[r(1,1)]
r2(2,:)=0
for q=1:length(r)-1
    
    if r(1,q)==r(1,q+1)
        r2(2,ir)=r2(2,ir)+1
    else
        r2(1,ir+1)=r(1,q+1);
        ir=ir+1;
    end
end
r2(2,:)=r2(2,:)+1
%The second row in r2 shows the number of repeated radii
%for various radii in row 1 of r2

%create circle template
f=1;b=1;
for rad=1:numel(r2)./2
    a=1;c=[];
    pixelx=round(r2(1,rad)./pixel);
    radius2=pixelx^2
    for y=-pixelx:pixelx;
        for x=-pixelx:pixelx;
            if x^2+y^2<radius2, c(a,1)=x;c(a,2)=y;
               a=a+1;
            end
        end
    end

%create x and y coordinates
    for t=1:r2(2,rad)
        for g=1:length(c)
        d(b,2) = c(g,1)+xc(1,f);
        d(b,1) = c(g,2)+zc(1,f);
        %fprintf(fstr,'%1g% 1g% 1g\n',dw,pixx,pixy);
        b=b+1;
        end
        f=f+1% number of obj
    end
end
%print info contained in d
fprintf(fstr,'%2g\n',length(d));
for p=1:length(d)
    fprintf(fstr,'%1g% 1g% 1g\n',dw,d(p,1),d(p,2));
end

fclose(fstr);
%plot etching positions
plot(d(1:length(d),1),d(1:length(d),2),'o')
                   
                    