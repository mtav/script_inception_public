function probe = check_probes(FOLDER,OUTFILE)
    probe=dir([FOLDER,filesep,'p*id.prn']);
    min_list = [];
    max_list = [];
    superfile = fopen(OUTFILE,'w');
    workingdir=pwd();
    for i=1:length(probe)
        fullpath = [ FOLDER, filesep, probe(i).name ];
        [ vEnd, vStart, dt, fmin, fmax, peak_frequency_vector, data_min, data_max ] = analyzePRN(fullpath, 'peak_file.txt');
        cd(workingdir);
        disp([fullpath,' : min = ',num2str(data_min),' max = ',num2str(data_max)]);
        fprintf(superfile, '%s : min = %E max = %E\n', fullpath,data_min,data_max);
        min_list = [ min_list, data_min ];
        max_list = [ max_list, data_max ];
    end
    fprintf(superfile, 'TOTAL : min = %E max = %E\n',min(min_list),max(max_list));
  fclose(superfile);
end
