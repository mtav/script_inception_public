function tdtreat(infilename,outfilename,imgbasename,label)
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % Creates reflection/transmission diagrams based on probe output using tdtreat.
  % Usage:
  % GetS21(infilename,outfilename)
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
  % TODO: pass excitation direction as argument (fixed to Ey at the moment)
  
  % argument processing
  if nargin==0
      %[InFileName,InPathName] = uigetfile('*.prn','Select input prn-file',getuserdir());
      [InFileName,InPathName] = uigetfile('*.prn','Select input prn-file',pwd);
      [OutFileName,OutPathName] = uigetfile('*.prn','Select the output prn-file',InPathName);
  
      infilename=[InPathName,InFileName];
      outfilename=[OutPathName,OutFileName];
  elseif nargin==1
      ind=max(strfind(infilename,filesep));
      InPathName=infilename(1:ind);
      InFileName=infilename(ind+1:end);
      [OutFileName,OutPathName] = uigetfile('*.prn','Select the output prn-file',InPathName);
      outfilename=[OutPathName,OutFileName];
  else
      ind=max(strfind(infilename,filesep));
      InPathName=infilename(1:ind);
      InFileName=infilename(ind+1:end);
      ind=max(strfind(outfilename,filesep));
      OutPathName=outfilename(1:ind);
      OutFileName=outfilename(ind+1:end);
  end

  if strfind(infilename,' ')
      disp('ERROR: Input file path ccontains space character');
      return;
  end
  if strfind(outfilename,' ')
      disp('ERROR: Input file path ccontains space character');
      return;
  end
  
  disp(['Processing in output directory ',OutPathName])
  S21folder=[OutPathName,'S21',filesep];
  if (~isdir(S21folder))
      mkdir(S21folder);
  end
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  infilename
  outfilename
  S21folder
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % hack to get BLOB in /gfdgfd/gfdgfdg/dfgdfgd/BLOB/
  ind=strfind(InPathName, filesep);
  if length(ind)>1
    start = ind(end-1)+1;
  else
    start = 1;
  end
  inProjName = InPathName(start:end-1);
  ind=strfind(OutPathName, filesep);
  if length(ind)>1
    start = ind(end-1)+1;
  else
    start = 1;
  end
  outProjName=OutPathName(start:end-1);
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  InPathName
  inProjName
  
  OutPathName
  outProjName
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %inSnapFile=[inProjName,filesep,InFileName(1:end-4),'_inc.prn'];
  %outSnapFile=[outProjName,filesep,OutFileName(1:end-4),'_out.prn'];
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  %commands to run:
  %sed 's/^#//' infilename > infilename.fixed
  %sed 's/^#//' outfilename > outfilename.fixed
  %cmd = ['harminv -t ',num2str(dt,'%2.8e'),' ',num2str(get_c0()/lambdaHigh,'%2.8e'),'-',num2str(get_c0()/lambdaLow,'%2.8e'),' < ',dataFile,' > ',outFile];
  cmd = ['sed ''s/^#//'' ',infilename,' > ',S21folder,filesep,'infilename.fixed']
  [status,result] = system(cmd);
  cmd = ['sed ''s/^#//'' ',outfilename,' > ',S21folder,filesep,'outfilename.fixed']
  [status,result] = system(cmd);

  % store original dir
  origdir = pwd()
  % cd into S21folder
  cd(S21folder)

  %IN file generation
  disp('Writing IN file...');

  %open file
  out = fopen('tdtreat.in','wt');

  %write file
  fprintf(out, '2\r\n'); % Get Data
  fprintf(out, '1\r\n'); % ASCII file
  fprintf(out, '2\r\n'); % number of files/data components
  fprintf(out, 'infilename.fixed\r\n'); % data filename (including any directory path needed)
  fprintf(out, '2\r\n'); % field components: Ex, Ey, Ez, Hx, Hy, Hz
  fprintf(out, 'y\r\n'); % confirm field component
  fprintf(out, 'outfilename.fixed\r\n'); % data filename (including any directory path needed)
  fprintf(out, '2\r\n'); % field components: Ex, Ey, Ez, Hx, Hy, Hz
  fprintf(out, 'y\r\n'); % confirm field component
  fprintf(out, '4\r\n'); % Processing data
  fprintf(out, '8\r\n'); % Dataset operations (+,-,*,/,average)
  fprintf(out, '1\r\n'); % Subtraction
  fprintf(out, '1\r\n'); % Enter probe no. for first variable
  fprintf(out, '2\r\n'); % Enter probe no. for second variable
  fprintf(out, '2\r\n'); % Enter probe no. for result to work inside program
  fprintf(out, 'y\r\n'); % Confirm default output file name (tdtreat1.dat)
  fprintf(out, '3\r\n'); % Fourier Transforms
  fprintf(out, '3\r\n'); % Select Fourier Transform Type : FFT
  fprintf(out, '16\r\n'); % Enter order of transform max 17
  fprintf(out, '0\r\n'); % Enter starting sample
  fprintf(out, '4\r\n'); % Processing data
  fprintf(out, '5\r\n'); % S parameters of a one to n port structure
  fprintf(out, '0 1\r\n'); % Enter start and stop frequencies (in GHz)
  fprintf(out, 'y\r\n'); % Results in dB ? (y/n)
  fprintf(out, 'n\r\n'); % Do you need the input impedance ? (y/n)
  fprintf(out, 'n\r\n'); % Extra run performed for a reference ? (y/n)
  fprintf(out, 'n\r\n'); % Shall we dump only /S11/ (dB or not) to the output file ? (y/n)
  fprintf(out, '-1 1\r\n');
  fprintf(out, 'q\r\n');
  fprintf(out, 'q\r\n');

  %close file
  fclose(out);
  disp('...done');

  % dosify files
  cmd = 'todos infilename.fixed outfilename.fixed tdtreat.in'
  [status,result] = system(cmd);

  %command to run:
  cmd = 'tdtreat < tdtreat.in'
  [status,result] = system(cmd)

  % plot
  [header,data] = readPrnFile('tdtreat1.dat');
  %figure; plot(data(:,1),data(:,2));%xlim([0.500 0.700])
  figure; plot((get_c0()*1e-6)./data(:,1),data(:,2));xlim([500 700]) % mum?
  %figure; plot((get_c0()*1e-3)./data(:,1),data(:,2));xlim([500 700]) % nm?

  xlabel(['wavelength lambda (nm?)']);
  ylabel([label,' (dB)']);
  title(strrep([infilename,' - ',outfilename],'_','\_'));

  % return to original dir
  cd(origdir)

  % save figure
  saveas(gcf,[imgbasename,'.png'],'png');
  saveas(gcf,[imgbasename,'.fig']);

end
