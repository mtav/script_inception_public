function [Data_Sample, zrange] = FIS_quickview_linescan(Name_Sample, do_save, overwrite, suffix, logfile, Wfile)
    
  if ~exist('do_save', 'var')
		do_save = false;
	end
    if ~exist('overwrite', 'var')
		overwrite = false;
	end
    if ~exist('suffix', 'var')
		suffix = '';
	end
	
    if ~exist('Name_Sample', 'var')
      [FileName_Sample, PathName_Sample] = uigetfile('*.txt','Select the Sample file');
      if isequal(FileName_Sample, 0)
        disp('User selected Cancel');
        return
      end
      Name_Sample = [PathName_Sample, FileName_Sample];
    end

    if ~exist('logfile', 'var')
      logfile = fullfile(dirname(Name_Sample), 'log.txt');
      if ~exist(logfile, 'file')
          d = dirname(logfile);
          filelist = dir(fullfile(d, '*log.txt'));
          if length(filelist)==1
              logfile = fullfile(filelist(1).folder, filelist(1).name);
              fprintf('Auto-determined logfile: %s\n', logfile);
          else
              filelist
              error('Failed to determine logfile.');
          end
      end
      FIS_info = FIS_readLogFile(logfile);
      Xres = FIS_info.Spatial_Resolution_mm;
      Xini = FIS_info.Initial_Position_mm(1);
      Xend = FIS_info.Final_position_mm(1);      
    end
    if ~exist('Wfile', 'var')
      Wfile = fullfile(dirname(Name_Sample), 'W.txt');
    end

    fprintf('Name_Sample = %s\n', Name_Sample);

    Data_Sample = load(Name_Sample);
    wavelength = load(Wfile);
    wavelength = unique(wavelength); % because data gets appended to W.txt on repeated measurements
    Xposition = Xini:Xres:Xend;
    if length(Xposition)==1
        Xposition(end+1) = Xend; % for dark background measurements, where only 1-2 positions are measured to save time
    end
    
    % if the measurement was cancelled, truncate the position vector
    if length(Xposition) > size(Data_Sample, 2)
        Xposition = Xposition(1:size(Data_Sample, 2));
    end
    
    figure();
    try
        pcolor(Xposition, wavelength, Data_Sample);
        %surf(Xposition, wavelength, Data_Sample); view(2);
        shading interp;
    catch
        disp('size(Xposition)'); size(Xposition)
        disp('size(wavelength)'); size(wavelength)
        disp('size(Data_Sample)'); size(Data_Sample)
        error('Data dimensions must agree.');
    end
    xlabel('X Position (mm)');
    ylabel('Wavelength (nm)');
    title(Name_Sample, 'Interpreter', 'None');

    colorbar;
    zrange = getRange(Data_Sample);
    
	if do_save
		[filepath, name, ext] = fileparts(Name_Sample);
		outfile = fullfile(filepath, sprintf('%s%s.png', name, suffix));
		if isfile(outfile) && ~overwrite
			warning('File exists: %s', outfile);
		else
			saveas(gcf, outfile);
		end
	end
	
end
