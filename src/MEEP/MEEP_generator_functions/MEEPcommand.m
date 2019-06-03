function MEEP_command(filename, BASENAME)
  %CMD file generation
  disp('Writing CMD file...');

  %open file
  out = fopen(strcat(filename,'.cmd'),'wt');

  % Executable = 'D:\fdtd\source\latestfdtd02_03\subgrid\Fdtd32.exe';
  Executable = fullfile(getuserdir(),'bin','fdtd.exe');
  
  %write file
  fprintf(out,'Executable = %s\n',Executable);
  fprintf(out,'\n');
  fprintf(out,'input = %s.in\n', BASENAME);
  fprintf(out,'\n');
  fprintf(out,'output = fdtd.out\n');
  fprintf(out,'\n');
  fprintf(out,'error = error.log\n');
  fprintf(out,'\n');
  fprintf(out,'Universe = vanilla\n');
  fprintf(out,'\n');
  fprintf(out,'transfer_files = ALWAYS\n');
  fprintf(out,'\n');
  fprintf(out,'transfer_input_files = entity.lst, %s.geo, %s.inp\n', BASENAME, BASENAME);
  fprintf(out,'\n');
  fprintf(out,'Log = foo.log\n');
  fprintf(out,'\n');
  fprintf(out,'Rank = Memory >= 1000\n');
  fprintf(out,'\n');
  fprintf(out,'LongRunJob = TRUE\n');
  fprintf(out,'\n');
  fprintf(out,'###Requirements = (LongRunMachine =?= TRUE)\n');
  fprintf(out,'\n');
  fprintf(out,'queue\n');

  %close file
  fclose(out);
  disp('...done');
end
