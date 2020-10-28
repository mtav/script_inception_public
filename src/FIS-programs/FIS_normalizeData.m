function processed_data = FIS_normalizeData(data_sample, data_reference, data_darkBackground)

  if ~exist('data_darkBackground', 'var')
	data_darkBackground = data_sample;
	data_darkBackground.Intensity = zeros(size(data_sample.Intensity));
  end

  processed_data.Sample = data_sample;
  processed_data.Reference = data_reference;
  processed_data.DarkBackground = data_darkBackground;

  processed_data.Sample_noDB = struct();
  processed_data.Sample_noDB.Position = processed_data.Sample.Position;
  processed_data.Sample_noDB.Lambda = processed_data.Sample.Lambda;
  processed_data.Sample_noDB.Intensity = processed_data.Sample.Intensity - processed_data.DarkBackground.Intensity;
  
  processed_data.Reference_noDB = struct();
  processed_data.Reference_noDB.Position = processed_data.Reference.Position;
  processed_data.Reference_noDB.Lambda = processed_data.Reference.Lambda;
  processed_data.Reference_noDB.Intensity = processed_data.Reference.Intensity - processed_data.DarkBackground.Intensity;
  
  processed_data.Normalized = struct();
  processed_data.Normalized.Position = processed_data.Sample.Position;
  processed_data.Normalized.Lambda = processed_data.Sample.Lambda;
  processed_data.Normalized.Intensity = processed_data.Sample_noDB.Intensity ./ processed_data.Reference_noDB.Intensity;
end
