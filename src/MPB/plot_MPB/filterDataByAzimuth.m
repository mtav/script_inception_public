function mpbdata_selection = filterDataByAzimuth(mpbdata, azimuth_list, tol)

  mpbdata_selection = struct();
  mpbdata_selection.info = mpbdata.info;
  mpbdata_selection.rawdata = mpbdata.rawdata;

  original_data = mpbdata.data;

  selected_indices = [];
  for phi_raw = azimuth_list
    phi = mod(phi_raw + pi, 2*pi) - pi;
    matching_indices = find( abs(original_data.k_azimuth - phi) <= tol );
    selected_indices = [selected_indices; matching_indices];
  end

  selected_indices = unique(selected_indices);

  Nfields = length(fieldnames(original_data));
  for idx = 1:Nfields;
    F_name = char(fieldnames(original_data)(idx));
    F_data = getfield(original_data, F_name);
    F_data_selection = F_data(selected_indices, :);
    mpbdata_selection.data.(F_name) = F_data_selection;
  end

  % update info fields
  mpbdata_selection.info.Nkpoints = size(mpbdata_selection.data.normalized_frequency, 1);
  mpbdata_selection.info.Nbands = size(mpbdata_selection.data.normalized_frequency, 2);

end

%close all; clear all;
%x = linspace(-10*pi,10*pi,20*100);
%y = mod(x + pi, 2*pi) - pi;
%figure;
%plot(x,y);
%hline(-pi);
%hline(pi);
%vline(-pi);
%vline(pi);
%vline(-10*pi);
%vline(0);
%vline(10*pi);
