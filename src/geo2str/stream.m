clear all
%constants
pixel = 0.00742;
dwellt = 800;
dw = num2str(dwellt);

%open file for use
fstr = fopen('rough1.str','wt');

%write preamble in stream file
fprintf(fstr,'s\n');
fprintf(fstr,'10\n');

%extract positions of objects and convert to streamfile units
tab = readtextfile('w1.geo');
dim = size(tab);
ii = 1; block = 0; size = 0;

while size == 0
    if strcmp(tab(ii,1:44), 'BLOCK **Block Definition (XL,YL,ZL,XU,YU,ZU)')
        ii=ii+2;
        xl = str2double(tab(ii,1:13)); ii=ii+2;
        yl = str2double(tab(ii,1:13)); ii=ii+1;
        xu = str2double(tab(ii,1:13)); ii=ii+2;
        yu = str2double(tab(ii,1:13));
        xmod = xu-xl;
        ymod = yu-yl;
        size = 1;
    end
    ii=ii+1;
end

clear xl yl xu yu
ii = 1;

while ii <= dim(1)
    if strcmp(tab(ii,1:44), 'BLOCK **Block Definition (XL,YL,ZL,XU,YU,ZU)')
        block=block+1;
        ii=ii+2;
        xx(block) = str2double(tab(ii,1:13)); ii=ii+2;
        yy(block) = str2double(tab(ii,1:13)); ii=ii+6;
    end
    ii=ii+1;
end

xx = xx';
yy = yy';
xx = round(xx./pixel);
yy = round(yy./pixel);

%write positions into stream file
lines = num2str(round(length(xx)*((round((xmod/pixel)+1)^2))));
fprintf(fstr,lines);
fprintf(fstr,'\n');

for jj=1:length(xx)
    for kk=0:round(xmod/pixel)
        for ll=0:round(xmod/pixel)
            pixx = num2str(xx(jj)+ll);
            pixy = num2str(yy(jj)+kk+280);
            pos = [dw ' ' pixx ' ' pixy];
            fprintf(fstr,pos);
            fprintf(fstr,'\n');
        end
    end
end

%close file
fclose(fstr);