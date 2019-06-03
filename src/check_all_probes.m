function check_all_probes(SEARCHSTR)
    listing = dir(SEARCHSTR);
    for i=1:length(listing);
        if listing(i).isdir==1;
        fullpath=listing(i).name;
        [ folder, basename, ext ] = fileparts(fullpath);
        check_probes(fullpath,[basename,'.minmax.txt']);
        end;
    end
end
