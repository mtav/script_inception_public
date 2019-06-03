function BMPtoSTR(maxDwell, minDwell, rep, step, INFILE, OUTFILE)
    % function BMPtoSTR(maxDwell=100, minDwell=10, rep=10, step=1, FILE)
    % converts a bitmap file to a streamfile by considering the red values of the image.

  if exist('maxDwell','var')==0
        maxDwell = 100;  % Assigned to Red level of 255
  end
  if exist('minDwell','var')==0
        minDwell = 10;   % Assigned to Red level of 0
  end
  if exist('rep','var')==0
        rep = 10;
  end
  if exist('step','var')==0
        step = 1;
  end
  if exist('INFILE','var')==0
        [fileName,pathName] = uigetfile('*.bmp','Select input BMP-file',getuserdir());
    else
        [ pathName, fileName, ext ] = fileparts(INFILE);
        fileName = [ fileName, ext ];
  end
  if exist('OUTFILE','var')==0
        OUTFILE = [pathName,filesep,fileName,'_rep',num2str(rep),'_step',num2str(step),'_dw',num2str(minDwell),'-',num2str(maxDwell),'.str'];    
    end

    center=1;
    scanType='oneway';
    scanDir='v';

    fid0=fopen([pathName,filesep,fileName],'r');

    A=imread([pathName,filesep,fileName]);
    A=A(:,:,1);
    GS=A;
    [x,y,RR]=ScanIm(GS,scanType,scanDir, step);

    % Example Scaling with maxDwell  and minDwell values.
    dwell = round((RR/255)*(maxDwell-minDwell)+minDwell);
    % dwell = RR;

    % plot3(x,y,dwell);

    if center
        x=x+2048-round((min(x)+max(x))/2);
        y=y+1980-round((min(y)+max(y))/2);
    end
    
    fid = fopen(OUTFILE,'w+');
    fprintf(fid,'s\r\n%i\r\n%i\r\n',rep,length(x));
    fprintf(fid,'%i %i %i\r\n',[dwell;x;y]);
    fclose(fid);
end
