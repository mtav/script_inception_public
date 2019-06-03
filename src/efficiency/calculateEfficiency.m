function [ret, total_power, total_X_in, total_X_out, total_Y_in, total_Y_out, total_Z_in, total_Z_out] = calculateEfficiency(X_in, X_out, Y_in, Y_out, Z_in, Z_out)
  % function [ret, total_power, total_X_in, total_X_out, total_Y_in, total_Y_out, total_Z_in, total_Z_out] = calculateEfficiency(X_in, X_out, Y_in, Y_out, Z_in, Z_out)
  %
  % Calculates the "efficiency", i.e. how much power goes out in a specific direction, relative to the others.
  % It requires a simulation with at least 6 frequency snapshots forming a box.
  %
  % The 6 snapshots should be passed in this order:
  %
  %   * X_in: lower X face of the box
  %   * X_out: upper X face of the box
  %
  %   * Y_in: lower Y face of the box
  %   * Y_out: upper Y face of the box
  %
  %   * Z_in: lower Z face of the box
  %   * Z_out: upper Z face of the box
  % 
  % Example usage and output:
  %   >> ret = calculateEfficiency('xd_id_00.prn', 'xe_id_00.prn', 'yf_id_00.prn', 'yg_id_00.prn', 'zh_id_00.prn', 'zi_id_00.prn');
  %      Total power output (proportional to Watts): 6.22
  %      X_in: 25.83 %
  %      X_out: 54.99 %
  %      Y_in: 2.55 %
  %      Y_out: 2.55 %
  %      Z_in: 7.04 %
  %      Z_out: 7.04 %
  %   >> ret =
  %      scalar structure containing the fields:
  %        total_power =  6.2203
  %        X_in =  0.25827
  %        X_out =  0.54992
  %        Y_in =  0.025543
  %        Y_out =  0.025543
  %        Z_in =  0.070361
  %        Z_out =  0.070362  

  [new_header, new_data, outfile, total_X_in] = createPoyntingSnapshot(X_in, true);
  [new_header, new_data, outfile, total_X_out] = createPoyntingSnapshot(X_out, true);
  [new_header, new_data, outfile, total_Y_in] = createPoyntingSnapshot(Y_in, true);
  [new_header, new_data, outfile, total_Y_out] = createPoyntingSnapshot(Y_out, true);
  [new_header, new_data, outfile, total_Z_in] = createPoyntingSnapshot(Z_in, true);
  [new_header, new_data, outfile, total_Z_out] = createPoyntingSnapshot(Z_out, true);

  total_power = (total_X_out.Sx - total_X_in.Sx) + (total_Y_out.Sy - total_Y_in.Sy) + (total_Z_out.Sz - total_Z_in.Sz);

  ret.total_power = total_power;
  ret.X_in = -total_X_in.Sx / total_power;
  ret.X_out = total_X_out.Sx / total_power;
  ret.Y_in = -total_Y_in.Sy / total_power;
  ret.Y_out = total_Y_out.Sy / total_power;
  ret.Z_in = -total_Z_in.Sz / total_power;
  ret.Z_out = total_Z_out.Sz / total_power;

  fprintf('Total power output (proportional to Watts): %.2f\n', ret.total_power);
  fprintf('X_in: %.2f %%\n', 100*ret.X_in);
  fprintf('X_out: %.2f %%\n', 100*ret.X_out);
  fprintf('Y_in: %.2f %%\n', 100*ret.Y_in);
  fprintf('Y_out: %.2f %%\n', 100*ret.Y_out);
  fprintf('Z_in: %.2f %%\n', 100*ret.Z_in);
  fprintf('Z_out: %.2f %%\n', 100*ret.Z_out);

  % Problem with arbitrary list: Need to know which "component/projection" of the poynting vectors to use....
  %nVarargs = length(varargin);
  %total_list = zeros(nVarargs, 1);
  %fprintf('Inputs in varargin(%d):\n',nVarargs);
  %for k = 1:nVarargs
    %fsnap = varargin{k};
    %disp(['Processing fsnap = ', fsnap]);
    %[new_header, new_data, outfile, total] = createPoyntingSnapshot(fsnap, true);
    %total
  %end
  
  %% create parser
  %p = inputParser();
  %p = inputParserWrapper(p, 'addRequired', 'inpfile_list', @iscellstr);
  %p = inputParserWrapper(p, 'addParamValue', 'fsnap_folder', '.', @isdir);
  %p = inputParserWrapper(p, 'addParamValue', 'eps_folder', '.', @isdir);
  %p = inputParserWrapper(p, 'addParamValue', 'snap_plane', 'z', @(x) any(validatestring(x, {'x','y','z'})));
  %p = inputParserWrapper(p, 'addParamValue', 'snap_time_number', NaN, @isnumeric); % if not given, we use getLastSnapTimeNumber()
  %p = inputParserWrapper(p, 'addParamValue', 'refractive_index_defect', 1, @isnumeric);
  %p = inputParserWrapper(p, 'addParamValue', 'is_half_sim', false, @islogical);
  %p = inputParserWrapper(p, 'addParamValue', 'numID_list', [], @isnumeric);
  %p = inputParserWrapper(p, 'addParamValue', 'justCheck', false, @islogical);
  %p = inputParserWrapper(p, 'addParamValue', 'BFDTD_version', '2013', @(x) any(validatestring(x, {'2003','2008','2013'})));
  %p = inputParserWrapper(p, 'addParamValue', 'mode_index', 1, @isnumeric);
  %p = inputParserWrapper(p, 'addParamValue', 'Nmodes', 1, @isnumeric);
  %p = inputParserWrapper(p, 'addParamValue', 'logfile_bool', false, @islogical);
  %p = inputParserWrapper(p, 'addParamValue', 'incorrectAlgorithm_bool', false, @islogical); % Incorrect mode volume calculation used in JQE paper. Only re-implemented for comparison purposes. Should always be left false otherwise!
  %p = inputParserWrapper(p, 'addParamValue', 'logfile', '', @ischar);
  %p = inputParserWrapper(p, 'addParamValue', 'integration_direction', 0, @(x) isnumeric(x) && size(x)==1 && any(x==[-1,0,1]));
  %p = inputParserWrapper(p, 'parse', inpfile_list, varargin{:});

  %efficiency = 0;
  
  %PrnFileNameList_xm = findPrnByName(inputFileList,'Box frequency snapshot X-')
  %PrnFileNameList_xp = findPrnByName(inputFileList,'Box frequency snapshot X+')
  %PrnFileNameList_ym = findPrnByName(inputFileList,'Box frequency snapshot Y-')
  %PrnFileNameList_yp = findPrnByName(inputFileList,'Box frequency snapshot Y+')
  %PrnFileNameList_zm = findPrnByName(inputFileList,'Box frequency snapshot Z-')
  %PrnFileNameList_zp = findPrnByName(inputFileList,'Box frequency snapshot Z+')

end
