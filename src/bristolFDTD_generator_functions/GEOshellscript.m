function GEOshellscript(filename, BASENAME, EXE, WORKDIR, WALLTIME)
  disp('Writing shellscript...')

  %open file
  out = fopen(filename,'wt');

  if exist('EXE','var')==0
    % disp('EXE not given');
    % EXE = '$HOME/bin/fdtd64_2003';
    % EXE = '$HOME/bin/fdtd';
    EXE = 'fdtd';
    disp(['EXE not given. Using default: EXE=',EXE]);
  end

  if exist('WORKDIR','var')==0
    % disp('WORKDIR not given');
      % WORKDIR = '$(dirname "$0")';
    %TODO: Is WORKDIR even necessary in the script? O.o
      WORKDIR = '$JOBDIR';
    disp(['WORKDIR not given. Using default: WORKDIR=',WORKDIR]);
  end
  
  if exist('WALLTIME','var')==0
      WALLTIME = 12;
    disp(['WALLTIME not given. Using default: WALLTIME=',WALLTIME]);
  end

  %write file
  fprintf(out,'#!/bin/bash\n');
  fprintf(out,'#\n');
  fprintf(out,'#PBS -l walltime=%d:00:00\n',WALLTIME);
  fprintf(out,'#PBS -mabe\n');
  fprintf(out,'#PBS -joe\n');
  fprintf(out,'#\n');
  fprintf(out,'\n');
  fprintf(out,'\n');
  fprintf(out,'export WORKDIR=%s\n',WORKDIR);
  fprintf(out,'export EXE=%s\n',EXE);
  fprintf(out,'\n');
  fprintf(out,'cd $WORKDIR\n');
  fprintf(out,'\n');
  fprintf(out,'$EXE %s.in > %s.out\n', BASENAME, BASENAME);
  fprintf(out,'fix_filenames.py -v .\n');

  %close file
  fclose(out);
  disp('...done')
end
