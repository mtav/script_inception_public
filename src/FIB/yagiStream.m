function filename_cellarray = yagiStream(folder,prefix)

    filename_cellarray = {};
    mag = 36000;
    dwell = 2400;             %unit: 0.1us
    [res, HFW] = getResolution(mag);
    disp(['Resolution = ',num2str(res),' mum/pxl']);
    
    holes_x_pxl = linspace(-2000,2000,400);
    holes_y_pxl = repmat(400*ones(1,length(holes_x_pxl)),1,2);
    rep = ones(1,length(holes_x_pxl));
    height_pxl = 400*ones(1,length(holes_x_pxl));
    width_pxl = 400*ones(1,length(holes_x_pxl));
    
    size(holes_x_pxl)
    size(holes_y_pxl)
    size(height_pxl)
    size(width_pxl)
    size(rep)
    
    for idx=1:length(holes_x_pxl)
        
        x = []
        y = []
        for i=1:height_pxl(idx)
            for j=1:width_pxl(idx)
                
            end
        end

        mkdir(folder);
        filename = [folder,filesep,prefix,'.idx_',num2str(idx),'.rep_',num2str(rep(idx)),'.str'];
        disp(['length(x) = ',num2str(length(x))]);
        disp(['Writing to ',filename]);
        fid = fopen(filename,'w');
        fprintf(fid,'s\r\n%i\r\n%i\r\n',rep(idx),length(x));
        fprintf(fid,'%i %i %i\r\n',[dwell;x;y]);
        fclose(fid);
        filename_cellarray{end+1} = filename;
    end

end
