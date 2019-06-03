function calculateModeVolume2_printResult(global_info_struct, global_MV_struct, fid)
  % example usage:
  %   calculateModeVolume2_printResult(ret.info, ret.MV);
  
  % TODO: finish this?
  
  if ~exist('fid', 'var')
    fid = 1; % = stdout also works, but does it work in Matlab?
  end
  
  indent = 1;
  prefix_base = '  ';
  prefix = repmat(prefix_base, 1, indent);
  
  % global info
  fprintf(fid, 'global info:\n');
  printLoaderInfo(global_info_struct, 'prefix', repmat(prefix_base, 1, 1), fid);
  %fprintf(fid, '%srefractive_index_defect = %f\n', prefix, calcMVstruct.refractive_index_defect);
  
  %% regional info (includes total volume/energy + maxima infos)
  %fprintf(fid, 'regional info:\n');
  %printRegionalInfo(calcMVstruct., 'prefix', prefix);
  
  %% mode volume info
  %fprintf(fid, 'mode volume info:\n');
  %printModeVolumeInfo(calcMVstruct., 'prefix', prefix);
  
end
