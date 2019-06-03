function [new_header, new_data, esnap, outfile] = createEnergySnapshot(fsnap, varargin)
  % function [new_header, new_data, esnap, outfile] = createEnergySnapshot(fsnap, varargin)
  %
  % Usage:
  %  [new_header, new_data, esnap, outfile] = createEnergySnapshot(fsnap)
  %  [new_header, new_data, esnap, outfile] = createEnergySnapshot(fsnap, esnap)
  %  [new_header, new_data, esnap, outfile] = createEnergySnapshot(fsnap, esnap, 'outfile.prn') % save to 'outfile.prn'
  %  [new_header, new_data, esnap, outfile] = createEnergySnapshot('fsnap.prn', esnap, true) % auto-save to 'fsnap_energy.prn'
  %  [new_header, new_data, esnap, outfile] = createEnergySnapshot(fsnap, esnap, outfile, 'epsilon0_factor', true, ...)
  %  [new_header, new_data, esnap, outfile] = createEnergySnapshot(fsnap, '', '', 'epsilon0_factor', true, ...)
  %  [new_header, new_data, esnap, outfile] = createEnergySnapshot(fsnap, '', false, 'epsilon0_factor', true, ...)
  %  [new_header, new_data, esnap, outfile] = createEnergySnapshot('zct_id_03.prn', '','', 'epsilon_dir', '../../epsilon/')
  %
  % Arguments:
  %   Required:
  %     fsnap: path to frequency snapshot
  %  Optional:
  %    esnap: path to epsilon snapshot. If esnap='', a default epsilon snapshot will be determined based on fsnap. Default=''.
  %    save: Boolean or string value. Default=false.
  %          * If false, the energy data is not saved.
  %          * If true, the energy data is saved to a file of the form '***_energy.prn'.
  %          * If it is a non-empty string, the energy data is saved to a file corresponding to that string.
  %          * Else (i.e. empty string '' for example) the energy data is not saved.
  %  Parameter-value pairs:
  %    'pre_2008_BFDTD_version': Default=false.
  %    'probe_ident': Default='_id_'.
  %    'epsilon0_factor': Whether or not to multiply by epsilon0. Default=false.
  %    'epsilon_dir': Directory containing the epsilon snapshot. It is only used if esnap=''. If it is an empty string, the epsilon snapshots will be searched for in the directory containing fsnap. Default=''.
  %
  % TODO: default should be to save? And disable auto-save in PP&co?
  % TODO: option to disable warnings?
  % TODO: Evaluate best option for Emod2 output:
  %         -Switch between Emod2 and epsilon*Emod2
  %         -Always output Emod2 at the same time
  %         -Optionally output Emod2 at the same time
  %         -Create separate function to output Emod2
  %         -Just use some eval trick in future proper plotting software... (i.e. calculate from raw data when requested)
  %         -Output Emod2 in an additional column! (with option to enable/disable)
  % TODO: return newly generated columns (and upgrade postprocessor, etc accordingly)
  
  %%%%%%%%
  % create parser
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'fsnap', @ischar);
  p = inputParserWrapper(p, 'addOptional', 'esnap', '', @ischar);
  p = inputParserWrapper(p, 'addOptional', 'save', false, @(x) islogical(x) || ischar(x));
  p = inputParserWrapper(p, 'addParamValue', 'pre_2008_BFDTD_version', false, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'probe_ident', '_id_', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'epsilon0_factor', false, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'save_energy_density', true, @islogical); % save epsilon*|E|^2
  p = inputParserWrapper(p, 'addParamValue', 'save_epsilon', true, @islogical); % save epsilon in an additional column
  p = inputParserWrapper(p, 'addParamValue', 'save_Emod2', true, @islogical); % save |E|^2 in an additional column
  p = inputParserWrapper(p, 'addParamValue', 'epsilon_dir', '', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'nowarning', false, @islogical);
  
  % parse arguments
  p = inputParserWrapper(p, 'parse', fsnap, varargin{:});
  %%%%%%%%

  % determine epsilon snapshot to use
  if isempty(p.Results.esnap)
    [esnap, esnap_basename] = fsnap_to_esnap(p.Results.fsnap, 'probe_ident', p.Results.probe_ident, 'pre_2008_BFDTD_version', p.Results.pre_2008_BFDTD_version, 'epsilon_dir', p.Results.epsilon_dir);
    if ~p.Results.nowarning
      warn_message = ['No epsilon snapshot specified. Using automatically determined snapshot: ', esnap_basename, ' - full path: ', esnap];
      warn_title = 'No epsilon snapshot specified.';
      if inoctave() % TODO: Should probably check if called from a GUI or not, but this will do for now.
        warndlg(warn_message, warn_title);
      else
        uiwait(warndlg(warn_message, warn_title));
      end
    end
  else
    esnap = p.Results.esnap;
  end
  
  % check that the files exist
  if ~exist(esnap, 'file')
    error('createEnergySnapshot:FileNotFound', ['File not found: ', esnap]);
  end
  if ~exist(fsnap, 'file')
    error('createEnergySnapshot:FileNotFound', ['File not found: ', fsnap]);
  end
  
  % read in data
  [header_esnap, data_esnap] = readPrnFile(esnap);
  [header_fsnap, data_fsnap] = readPrnFile(fsnap);
  
  % prepare new header and data
  new_header = {header_esnap{1}, header_esnap{2}};
  new_data = [data_esnap(:,1), data_esnap(:,2)];
  
  epsilon_relative = data_esnap(:,3);
  Emod2 = (data_fsnap(:,3).^2+data_fsnap(:,6).^2+data_fsnap(:,9).^2);
  
  if p.Results.save_energy_density
    new_header{end+1} = 'epsilon*(Ex^2+Ey^2+Ez^2)';
    if p.Results.epsilon0_factor
      % The epsilon snapshots give epsilon_relative. We therefore multiply by epsilon0 to get a real energy density.
      new_data = [new_data, get_epsilon0().*epsilon_relative.*Emod2];
    else
      new_data = [new_data, epsilon_relative.*Emod2];
    end
  end
  
  if p.Results.save_epsilon
    new_header{end+1} = 'epsilon_relative';
    new_data = [new_data, epsilon_relative];
  end
  if p.Results.save_Emod2
    new_header{end+1} = 'Emod2';
    new_data = [new_data, Emod2];
  end
  
  % write energy snapshot to outfile
  outfile = '';
  if ( islogical(p.Results.save) && p.Results.save == true )
    outfile = fullfile( dirname(fsnap), [basename(fsnap, '.prn'), '_energy.prn']);
  elseif ischar(p.Results.save) && ~isempty(p.Results.save)
    outfile = p.Results.save;
  end
  if ~isempty(outfile)
    disp(['Saving energy snapshot as ', basename(outfile)]);
    writePrnFile(outfile, new_header, new_data);
  end
  
end
