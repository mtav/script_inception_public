function [Data_Sample, zrange] = FIS_quickview_linescan(Name_Sample)
    
    Xini = 3.3;
    Xend = 9.3;
    Xres = 0.1;

    Plot_position = 8.5;

    if ~exist('Name_Sample', 'var')
      [FileName_Sample, PathName_Sample] = uigetfile('*.txt','Select the Sample file');
      if isequal(FileName_Sample, 0)
        disp('User selected Cancel');
        return
      end
      Name_Sample = [PathName_Sample, FileName_Sample];
    end

    fprintf('Name_Sample = %s\n', Name_Sample);

    Data_Sample = load(Name_Sample);

    Xposition = Xini:Xres:Xend;

    figure();
    imagesc(Data_Sample);
    title(Name_Sample, 'Interpreter', 'None');

    colorbar;
    zrange = getRange(Data_Sample);
    
end
