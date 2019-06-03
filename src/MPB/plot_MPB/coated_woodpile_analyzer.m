function ret = coated_woodpile_analyzer()
  %datadir = '~/Downloads/resolution=128/';
  datadir = './resolution=128';
  datafilename = fullfile(datadir, 'non-coated', 'BCC-coated-woodpiles.out.uniq.dat');
  
  data_info = mpb_DataInfo('a', 1.1);
  mpbdata = read_MPB_CSV(datafilename, 'data_info', data_info, 'klabels', {'U','L','K'}, 'GuessCsvDelimiter', false);
  
  ret.non_coated.data = mpbdata.data.normalized_frequency;
  
  ret.non_coated.header = {'k index', 'band index'};
  
  ret.coated.data = [];
  
  ret.coated.n_list = [3.1];
  ret.coated.t_list = cat(2, 0.001:0.001:0.009, 0.010:0.010:0.150);
  
  ret.coated.header = {'coating index', 'coating thickness', 'k index', 'band index'};
  
  for n_idx = 1:length(ret.coated.n_list)
    n = ret.coated.n_list(n_idx);
    
    for t_idx = 1:length(ret.coated.t_list)
      t = ret.coated.t_list(t_idx);
      datafilename = fullfile(datadir, sprintf('coating_index=%.2f', n), sprintf('thickness_mum=%.3f', t), 'BCC-coated-woodpiles.out.uniq.dat');
      printf('n=%.2f t=%.3f datafilename=%s\n', n, t, datafilename);
      mpbdata = read_MPB_CSV(datafilename, 'data_info', data_info, 'klabels', {'U','L','K'}, 'GuessCsvDelimiter', false);
      
      ret.coated.data(n_idx, t_idx, :, :) = mpbdata.data.normalized_frequency;
      
      %thickness, n, k-point, band -> freq
    end
  end
end

%plot(omega0, thickness, n=2.1, k='U', band=1);

% cf MV_convergence_plot_function_xy
