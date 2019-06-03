function MEEP_shellscript(filename, BASENAME, EXE, WORKDIR)
  disp('Writing shellscript...')

  %open file
  out = fopen(strcat(filename,'.sh'),'wt');


  if exist('EXE','var')==0
    disp('EXE not given');
    % EXE = '$HOME/bin/fdtd64_2003';
    EXE = '$HOME/bin/fdtd';
  end

  if exist('WORKDIR','var')==0
    disp('WORKDIR not given');
      % WORKDIR = '$(dirname "$0")';
    %TODO: Is WORKDIR even necessary in the script? O.o
      WORKDIR = '$JOBDIR';
  end
  
  %write file
  fprintf(out,'#!/bin/bash\n');
  fprintf(out,'#\n');
  fprintf(out,'#PBS -l walltime=360:00:00\n');
  fprintf(out,'#PBS -mabe\n');
  fprintf(out,'#PBS -joe\n');
  fprintf(out,'#PBS -l nodes=1:ppn=8\n');
  fprintf(out,'#\n');
  fprintf(out,'\n');
  fprintf(out,'\n');
  fprintf(out,'export WORKDIR=%s\n',WORKDIR);
  fprintf(out,'export EXE=%s\n',EXE);
  fprintf(out,'\n');
  fprintf(out,'cd $WORKDIR\n');
  fprintf(out,'\n');
  fprintf(out,'$EXE %s.in > %s.out\n', BASENAME, BASENAME);

  %close file
  fclose(out);
  disp('...done')
end
