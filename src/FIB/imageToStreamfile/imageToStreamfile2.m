function [x, y, dwell] = imageToStreamfile2(BW)
  % FIBetch test script 1 - Written by Nathan Ahmad
  % Original filename: Fibetch_na2
  %
  % Example usage:
  %   BW = rgb2gray(imread('ngc6543a.jpg'));
  %   [x, y, dwell] = imageToStreamfile2(BW);
  %
  % TODO: image flipping, cropping, spot size, etc...
  
  image_height = size(BW, 1);
  image_width = size(BW, 2);
  
  screen_height = 884;
  screen_width = 1024;
  
  % fit the image onto the screen
  A1 = zeros(screen_height, screen_width);
  A1(1:image_height, 1:image_width) = BW;
  A1 = A1(1:screen_height, 1:screen_width);
  
  A1 = double(A1);
  
  R = getRange(A1);
  
  A2 = A1 - min(A1(:));
  
  %pxtest = A1(1, 1); % take red value of the top left corner of the image
  %A2 = repmat(pxtest, 884, 1024);
  %b = A1(1,:);
  %pxval= A2-A1;
  
  %[row, col, value] = find(pxval); % The main part of the script is simply a find command returning non-zero elements of the image array...
  [row, col, value] = find(A2); % The main part of the script is simply a find command returning non-zero elements of the image array...
  
  % scale coordinates and dwelltimes 
  x = 4.*col;
  y = 4.*row + 280;
  %x = 1.*col;
  %y = 1.*row + 280;
  %dwell = abs(value.*100);
  dwell = abs(value);
  
  %% file output: Can be handled by writeStrFile()
  %%set number of loops of points
  %numloops = 25;
  
  %%number of values (no need to set)
  %numval = length(ROW3);
  
  %%for set dell time for every pixel use this (comment out if you want dwell
  %%time related to pixel greyscale value)
  %%dwelltime=96;
  %%dwelltimemat=repmat(dwelltime,numval,1);
  %%fileID = fopen('FIBStream\stream.txt','w');
  %%fprintf(fileID,'%1c','s');
  %%fprintf(fileID,'\r\n');
  %%fprintf(fileID,'%1g',numloops);
  %%fprintf(fileID,'\r\n');
  %%fprintf(fileID,'%1g',numval);
  %%for i=1:numval
  %%    fprintf(fileID,'\r\n');
  %%    fprintf(fileID,'%1g',dwelltimemat(i));
  %%    fprintf(fileID,'% 2g',COL3(i));
  %%    fprintf(fileID,'% 3g',ROW3(i));
  %%end;
  %%fclose(fileID);
  
  %%%for dell time dictated by picture use this
  %fileID = fopen('FIBSTREAM\stream.txt','w');
  %fprintf(fileID, '%1c', 's');
  %fprintf(fileID, '\r\n');
  %fprintf(fileID, '%1g', numloops);
  %fprintf(fileID, '\r\n');
  %fprintf(fileID, '%1g', numval);
  %for i=1:numval
      %fprintf(fileID, '\r\n');
      %fprintf(fileID, '%1g', v(i));
      %fprintf(fileID, '% 2g', COL3(i));
      %fprintf(fileID, '% 3g', ROW3(i));
  %end;
  %fclose(fileID);
end
