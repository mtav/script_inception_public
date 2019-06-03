function test_save_structure(mystruct, outfilebase)
  printStructure(mystruct);
  fprintf('%s\n', printStructure(mystruct));
  
  [header, data] = struct2prn(mystruct);
  
  writePrnFile([outfilebase, '.prn'], header, data, 'delimiter', ';');
  
  csvfile = [outfilebase, '.csv'];
  fid = fopen(csvfile, 'w');
  fprintf(fid, '%s\n', strjoin(header, ';'));
  fclose(fid);
  dlmwrite(csvfile, data, '-append', 'delimiter', ';');
  dlmwrite(csvfile, data, '-append', 'delimiter', ';');
  dlmwrite(csvfile, data, '-append', 'delimiter', ';');
end
