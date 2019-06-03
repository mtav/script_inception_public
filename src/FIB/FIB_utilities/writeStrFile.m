function writeStrFile(outfile, x, y, dwell, rep)
  % function writeStrFile(outfile, x, y, dwell, rep)
  % TODO: Add automatic splitting and/or warning if number of points is too large for the FIB? (N > 2^15 = 32768 ? To be confirmed...)
  
  % ensure single row format and integer values
  x = round(x(:)');
  y = round(y(:)');
  dwell = round(dwell(:)');
  
  if length(y) ~= length(x) || length(dwell) ~= length(x)
    error(['sizes of x, y and dwell do not match: length(x)=',num2str(length(x)),' length(y)=',num2str(length(y)),' length(dwell)=',num2str(length(dwell))]);
  end
  fid = fopen(outfile,'w');
  fprintf(fid, 's\r\n%i\r\n%i\r\n', rep, length(x));
  fprintf(fid, '%i %i %i\r\n', [dwell; x; y]);
  fclose(fid);
end

% things that could be added:
% strDate=datestr(now, 'ddmmmm');
%if exist('folder','var')==0
  %folder = uigetdir(pwd(),'folder');
%end
%if ~(exist(folder,'dir'))
  %error(['dir not found: ',folder]);
%end
