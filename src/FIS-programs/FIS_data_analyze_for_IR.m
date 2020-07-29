function FIS_structure = FIS_data_analyze_for_IR(FIS_structure)

    if ~exist('FIS_structure', 'var')
		FIS_structure = struct();
				
		[FileName_Dark,PathName_Dark] = uigetfile('*.txt','Select the Dark file');
		[FileName_Mirror,PathName_Mirror] = uigetfile('*.txt','Select the Mirror file');
		[FileName_Sample,PathName_Sample] = uigetfile('*.txt','Select the Sample file');
		[FileName_Wavelength,PathName_Wavelength] = uigetfile('*.txt','Select the Wavelength file');

		FIS_structure.Name_Dark = [PathName_Dark, FileName_Dark];
		FIS_structure.Name_Mirror = [PathName_Mirror, FileName_Mirror];
		FIS_structure.Name_Sample = [PathName_Sample, FileName_Sample];
		FIS_structure.Name_Wavelength = [PathName_Wavelength, FileName_Wavelength];
	end

	if ~isfield(FIS_structure, 'Xini'); FIS_structure.Xini = 3.3; end;
	if ~isfield(FIS_structure, 'Xend'); FIS_structure.Xend = 9.3; end;
	if ~isfield(FIS_structure, 'Xres'); FIS_structure.Xres = 0.1; end;
	if ~isfield(FIS_structure, 'Plot_position'); FIS_structure.Plot_position = 8.5; end;
	if ~isfield(FIS_structure, 'plot_mode'); FIS_structure.plot_mode = 1; end;

	FIS_structure.data.Data_Dark = load(FIS_structure.Name_Dark);
	FIS_structure.data.Data_Mirror = load(FIS_structure.Name_Mirror);
	FIS_structure.data.Data_Sample = load(FIS_structure.Name_Sample);
	FIS_structure.data.Data_Wavelength = load(FIS_structure.Name_Wavelength);
	FIS_structure.data.Data_Wavelength = unique(FIS_structure.data.Data_Wavelength); % Labview currently adds to the existing W.txt file instead of replacing it.

	FIS_structure.data.Data_Dark_Processed = repmat(FIS_structure.data.Data_Dark(:, 1), 1, size(FIS_structure.data.Data_Mirror, 2) );

	FIS_structure.data.Data_normalized = (FIS_structure.data.Data_Sample - FIS_structure.data.Data_Dark_Processed)./(FIS_structure.data.Data_Mirror - FIS_structure.data.Data_Dark_Processed);

	FIS_structure.data.Xposition = FIS_structure.Xini:FIS_structure.Xres:FIS_structure.Xend;

	if FIS_structure.plot_mode == 0
		figure();
		imagesc(FIS_structure.data.Data_Dark_Processed);
		colorbar();
		title('Data Dark Processed');

		figure();
		imagesc(FIS_structure.data.Data_Mirror);
		colorbar();
		title('Data Mirror');

		figure();
		imagesc(FIS_structure.data.Data_Sample);
		colorbar();
		title('Data Sample');

		figure();
		imagesc(FIS_structure.data.Xposition, FIS_structure.data.Data_Wavelength, FIS_structure.data.Data_normalized, [0, 1]);
		colorbar();
		title('Normalized');

		figure();
		FIS_structure.data.cross_section = FIS_structure.data.Data_normalized(:, int64((FIS_structure.Plot_position - FIS_structure.Xini)/FIS_structure.Xres));
		plot(FIS_structure.data.Data_Wavelength, FIS_structure.data.cross_section);
		title(sprintf('Cross-section at x=%.3fmm', FIS_structure.Plot_position));
	else
		figure(); hold on;
		subplot(2,2,1);
		imagesc(FIS_structure.data.Data_Dark_Processed);
		colorbar();
		title('Data Dark Processed');

		subplot(2,2,2);
		imagesc(FIS_structure.data.Data_Mirror);
		colorbar();
		title('Data Mirror');

		subplot(2,2,3);
		imagesc(FIS_structure.data.Data_Sample);
		colorbar();
		title('Data Sample');

		subplot(2,2,4);
		imagesc(FIS_structure.data.Xposition, FIS_structure.data.Data_Wavelength, FIS_structure.data.Data_normalized, [0, 1]);
		colorbar();
		title('Normalized');
	end

end
