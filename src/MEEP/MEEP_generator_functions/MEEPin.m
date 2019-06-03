function MEEP_in(filename, file_list)

  %IN file generation
  disp('Writing IN file...');

  %open file
  out = fopen(filename,'wt');

  %write file
    for idx = 1:length(file_list)
        fprintf(out, '%s\n', file_list{idx});
    end

  %close file
  fclose(out);
  disp('...done');
end
