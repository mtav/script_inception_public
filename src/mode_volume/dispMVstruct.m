function dispMVstruct(logfile_fid_list, MVstruct, prefix)

  if ~exist('prefix', 'var'); prefix=''; end;

  disp_and_log(logfile_fid_list, [prefix, 'Mode volume:']);

  disp_and_log(logfile_fid_list, [prefix, '  mode_volume_mum3 = ', num2str(MVstruct.mode_volume_mum3)]);
  disp_and_log(logfile_fid_list, [prefix, '  mode_length_mum = mode_volume_mum3^(1/3) = ', num2str(MVstruct.mode_length_mum)]);
  disp_and_log(logfile_fid_list, [prefix, '  Lambda_mum = ', num2str(MVstruct.wavelength_mum)]);
  disp_and_log(logfile_fid_list, [prefix, '  n = ', num2str(MVstruct.refractive_index_defect)]);
  
  disp_and_log(logfile_fid_list, [prefix, 'Normalization:']);
  
  disp_and_log(logfile_fid_list, [prefix, '  Lambda_mum/n:']);
  disp_and_log(logfile_fid_list, [prefix, '    normalization_length_1_mum = ', num2str(MVstruct.normalization_length_1_mum)]);
  disp_and_log(logfile_fid_list, [prefix, '    normalization_volume_1_mum3 = ', num2str(MVstruct.normalization_volume_1_mum3)]);
  disp_and_log(logfile_fid_list, [prefix, '    normalized_mode_volume_1 = ', num2str(MVstruct.normalized_mode_volume_1)]);
  disp_and_log(logfile_fid_list, [prefix, '    normalized_mode_length_1 = ', num2str(MVstruct.normalized_mode_length_1)]);

  disp_and_log(logfile_fid_list, [prefix, '  Lambda_mum/(2*n):']);
  disp_and_log(logfile_fid_list, [prefix, '    normalization_length_2_mum = ', num2str(MVstruct.normalization_length_2_mum)]);
  disp_and_log(logfile_fid_list, [prefix, '    normalization_volume_2_mum3 = ', num2str(MVstruct.normalization_volume_2_mum3)]);
  disp_and_log(logfile_fid_list, [prefix, '    normalized_mode_volume_2 = ', num2str(MVstruct.normalized_mode_volume_2)]);
  disp_and_log(logfile_fid_list, [prefix, '    normalized_mode_length_2 = ', num2str(MVstruct.normalized_mode_length_2)]);
end
