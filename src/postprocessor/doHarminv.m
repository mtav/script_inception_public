function [ status, lambda, Q, outFile, err, minErrInd, frequency, decay_constant, amplitude, phase ] = doHarminv(inFile, dt, lambdaLow, lambdaHigh, outFile, cmdFile, verbose)
  % function [ status, lambda, Q, outFile, err, minErrInd, frequency, decay_constant, amplitude, phase ] = doHarminv(inFile, dt, lambdaLow, lambdaHigh, outFile, cmdFile, verbose)
  %
  % Wrapper around the harminv command. Should be cross-platform and work as long as "harminv" is on the system path.
  %
  % inFile : file to be used as standard input for the harminv command
  % dt : Specify the sampling interval dt; this determines the units of time used throughout the input and output.  Defaults to 0.01.
  % lambdaLow - lambdaHigh : wavelength range to search
  % outFile : file to which to save the command output
  % cmdFile : file to which to save the used command
  % verbose : be verbose or not
  %  
  % TODO: Document and use a sane order. This should be a simple wrapper for harminv, with same input/output order, nothing more. (will require changes to all occurences of doHarminv elsewhere)
  % TODO: IMPORTANT: Harminv supports searching in one or more frequency ranges, i.e. you can specify a list of min-max ranges in a single run!!! Use this to find the Q factors of the peaks selected by postprocessor!!!
  % TODO: Switch to frequency ranges instead of wavelength ranges...?
  % TODO: add SSH support so people don't have to install/setup harminv locally? Pass executable/command?
  % TODO: Make writing out files optional.
  % TODO: Make it work with raw probe .prn file instead of pre-processed .prn file (requires selecting the right column...)?
  %
  % In case of library issues, add this in front of the harmin command:
  % LD_LIBRARY_PATH=/usr/lib
  % TODO: Executable specification...
  % TODO: Find way to run system commands from Matlab with the usual environment.
  %
  % new naming standards:
  %  *.harminv.stdin : command standard input
  %  *.harminv.stdout : command standard output
  %  *.harminv.cmd : harminv command which was run

  %%%

  original_pwd = pwd;
  [ inFile_dir, inFile_base, inFile_ext ] = fileparts(inFile);
  [ outFile_dir, outFile_base, outFile_ext ] = fileparts(outFile);
  [ cmdFile_dir, cmdFile_base, cmdFile_ext ] = fileparts(cmdFile);
  inFile = [inFile_base, inFile_ext];
  outFile = [outFile_base, outFile_ext];
  cmdFile = [cmdFile_base, cmdFile_ext];
  cd(inFile_dir);
  
  % set up default variables
  if exist('verbose','var')==0; verbose=false; end
  if exist('dt','var')==0; dt=0.01; end
  if exist('lambdaLow','var')==0; lambdaLow=0.75*get_c0(); end
  if exist('lambdaHigh','var')==0; lambdaHigh=1.2*get_c0(); end
  
  % ask user for input file if unspecified or not found
  if ( exist('inFile','var')==0 ) | ( exist(inFile, 'file')==0 )
    disp('>>>>>>>>')
    disp('Is inFile a variable?:')
    exist('inFile','var')
    disp('Is inFile a file?:')
    exist(inFile, 'file')
    disp('>>>>>>>>')
    warning('No file specified or specified file not found.');
    [fileBasenameWithExtension, path_str] = uigetfile('*');
    if fileBasenameWithExtension == 0
      cd(original_pwd)
      error('doHarminv:NoInputFile', 'No file selected. Exiting.');
    end
    inFile = [path_str, fileBasenameWithExtension];
  end
  
  % set up filenames
  [fileBasenameWithoutExtension, path_str, fileBasenameWithExtension] = basename(inFile, '.harminv.stdin');
  if exist('outFile','var')==0; outFile = [path_str,filesep,fileBasenameWithoutExtension,'.harminv.stdout']; end
  if exist('cmdFile','var')==0; cmdFile = [path_str,filesep,fileBasenameWithoutExtension,'.harminv.cmd']; end
  %%%

  % set up command string  
  if ispc % On Windows
    hcommand = ['harminv -t ',num2str(dt,'%2.8e'),' ',num2str(get_c0()/lambdaHigh,'%2.8e'),'-',num2str(get_c0()/lambdaLow,'%2.8e'),' < ',inFile,' > ',outFile];
  else % On GNU/Linux, when there are out of date libs in /usr/local like at the university...
    hcommand = ['LD_LIBRARY_PATH=/usr/lib harminv -t ',num2str(dt,'%2.8e'),' ',num2str(get_c0()/lambdaHigh,'%2.8e'),'-',num2str(get_c0()/lambdaLow,'%2.8e'),' < ',inFile,' > ',outFile];
  end

  hcommand = regexprep(hcommand,'\\','\\\\');
  
  % save command to file
  fid = fopen(cmdFile,'w');
  fprintf(fid,[hcommand,'\r\n']);
  fclose(fid);
 
  %%%
  % run command
  if(verbose)
    disp('==========================================');
    disp(['inFile = ',inFile]);
    disp(['outFile = ',outFile]);
    disp(['cmdFile = ',cmdFile]);
    disp('============ Command to run ==============');
    disp(hcommand);
    disp('============ Command output ==============');
  end
  [status, result] = system(hcommand, '-echo');
  if(verbose)
    disp('==========================================');
  end

  % exit on error
  if (status ~= 0)
	error('doHarminv:CommandFail', ['harminv run failed with status:\n%d',...
			'\nThe executed command was:\n%s',...
			'\nRunning from directory:\n%s',...
			'\nHere is the output again:\n%s'],...
			status, hcommand, pwd, result);
  end
  %%%
  
  %%%
  % process output
  if ~(exist(outFile,'file'))
    error('doHarminv:NoOutputFile', ['ERROR: File ', outFile, ' does not exist.']);
  end

  % TODO: GNU Octave compatibility: Handle empty output file case (i.e. when there is only a header and no data) (and/or report bug to GNU Octave devs if it applies)
  % read contents of file into "C"
  fid = fopen(outFile,'r');
  tline = fgetl(fid);
  numCol = length(strfind(tline,','));
  str = repmat('%f, ',1,numCol);
  str = [str,'%f'];
  C = textscan(fid, str);
  fclose(fid);

  % fill output variables    
  frequency = C{1};
  decay_constant = C{2};
  Q = C{3};
  amplitude = C{4};
  phase = C{5};
  err = C{6};
  lambda = get_c0()./C{1};
  
  % sort everything by lambda
  [lambda,k] = sort(lambda);

  frequency = frequency(k);
  decay_constant = decay_constant(k);
  Q = Q(k);
  amplitude = amplitude(k);
  phase = phase(k);
  err = err(k);
  
  minErrInd = find(err==min(err));
  %%%

  cd(original_pwd);

end
