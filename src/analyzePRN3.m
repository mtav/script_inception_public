% this is getting out of hand... Oh well, things need to get done. Code can be cleaned up later...

    %if excitation_direction == 'x'
      %probe_col = 2;
    %elseif excitation_direction == 'y'
      %probe_col = 3;
    %elseif excitation_direction == 'z'
      %probe_col = 4;

function analyzePRN3(prn_file, logfile, logfile_summary, probe_col)

  [ folder, basename, ext ] = fileparts(prn_file);
  WORKDIR = dirname(prn_file);

  autosave = false;
  plotNothing = true;

  %logfile = '~/tmpQ.txt';
  %probe_col = 3; % mike diamond
  %probe_col = 2; % daniel latest 0/1/2

  iterations = parseBFDTDTime([WORKDIR, filesep, 'time.txt']);

  [ wavelength_nm, Q_lorentz, Q_harminv_local, Q_harminv_global ] = plotProbe(prn_file, probe_col, autosave, '', true, plotNothing);

  fid = fopen(logfile, 'at');
  fprintf(fid,'\n');
  %fprintf(fid, 'File\tIterations\tWavelength(nm)\tQ-factor(harminv)\tQ-factor(fitting)\n');
  %fprintf(fid, '%s\t%d\t%0.0f\t%0.0f\t%0.0f\n', prn_file, iterations, wavelength_nm(i), Q_lorentz(i), Q_harminv_local(i), Q_harminv_global(i));
  fprintf(fid, 'File\tIterations\n');
  fprintf(fid, '%s\t%d\n', GetFullPath(prn_file), iterations);
  fprintf(fid, 'File\tIterations\twavelength_nm\tQ_lorentz\tQ_harminv_local\tQ_harminv_global\n')
  for i=1:length(wavelength_nm)
    fprintf(fid, '%s\t%d\t%0.0f\t%0.0f\t%0.0f\t%0.0f\n', folder, iterations, wavelength_nm(i), Q_lorentz(i), Q_harminv_local(i), Q_harminv_global(i));
  end
  fprintf(fid,'\n');
  fclose(fid);

  fid = fopen(logfile_summary, 'at');
  for i=1:length(wavelength_nm)
    if Q_lorentz(i)>0 & Q_harminv_local(i)>0 & Q_harminv_global(i)>0
      fprintf(fid, '%s\t%d\t%0.0f\t%0.0f\t%0.0f\t%0.0f\n', folder, iterations, wavelength_nm(i), Q_lorentz(i), Q_harminv_local(i), Q_harminv_global(i));
      break;
    end
  end
  fclose(fid);

end
