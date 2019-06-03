function plotAllSum(directory, maxplotvalue, Probe_patternCellArray, TimeSnapshot_patternCellArray, FrequencySnapshot_patternCellArray)

  % ex: Probe_patternCellArray = {'pxx.prn','ptyruytue.prn',etc}
  % ex: plotAll('~/Labortablo/nano_meeting/',1,{'p01id.prn','p001id.prn'},{'y.*id.*\.prn'},{'y.*id.*\.prn'})
  % TODO: Make it work with relative path too (i.e. '.' for example)
  
  if exist('directory','var')==0
    directory = pwd();
  end

  if exist('maxplotvalue','var')==0
    maxplotvalue = NaN;
  end

  % loop through .sh files
  % TODO: Leave looping through files to bash or python :P (externalize it at least)
  [Files,Bytes,Names] = dirr(directory,'\.in\>$','name');
  %length(Names)
  %for script_idx = 1:length(Names)
    %disp(char(Names(script_idx)))
  %end
  %return
  for script_idx = 1:length(Names)
    script_filename = char(Names(script_idx));
    [ script_folder, script_basename, script_ext ] = fileparts(script_filename);

    geofile = [ script_folder, filesep, script_basename, '.geo' ];
    inpfile = [ script_folder, filesep, script_basename, '.inp' ];
    
    %disp(geofile)
    %inpfile
    %continue
    %which GEO_INP_reader
    
    disp(['Processing script_folder = ', script_folder]);
    [entries,FDTDobj] = GEO_INP_reader({geofile,inpfile});
    excitation = FDTDobj.excitations(1);
    excitation_direction = excitation.E;
    
    measurement_direction = '';
    
    %excitation_direction
    %class(excitation_direction)
    if excitation_direction == [1,0,0]
      measurement_direction = 'x';
    elseif excitation_direction == [0,1,0]
      measurement_direction = 'y';
    elseif excitation_direction == [0,0,1]
      measurement_direction = 'z';
    elseif excitation_direction == [1,1,1]
      excitation.template_filename
      [header,data]=readPrnFile([script_folder, filesep, excitation.template_filename]);
      for j=3:length(header);
        val = max(data(:,j));
        if ( val~=0 );
          header(j)
          header{j}
          if header{j}=='Exre'
            measurement_direction = 'x';
          elseif header{j}=='Eyre'
            measurement_direction = 'y';
          elseif header{j}=='Ezre'
            measurement_direction = 'z';
          else
            error('Unsupported template direction');
          end
        end;
      end;
    else
      error('Unknown excitation_direction');
    end

    if measurement_direction == 'x'
      probe_col = 2;
      TimeSnapshot_col = 3;
      FrequencySnapshot_col = 3;
    elseif measurement_direction == 'y'
      probe_col = 3;
      TimeSnapshot_col = 4;
      FrequencySnapshot_col = 6;
    elseif measurement_direction == 'z'
      probe_col = 4;
      TimeSnapshot_col = 5;
      FrequencySnapshot_col = 9;
    else
      error('Unknown measurement_direction');
    end
    %measurement_direction
    %return

    % store workdir
    workdir = pwd();

    % loop through .prn files
    automax_time_list = [];
    automax_freq_list = [];
    cd(script_folder);
    prnFiles = dir('*.prn');
    for prn_idx = 1:length(prnFiles)
    
      handles = struct;
      handles.geofile = geofile;
      handles.inpfile = inpfile;
    
      prn_filename = prnFiles(prn_idx).name;
      [ prn_filename_folder, prn_filename_basenameNoExt, prn_filename_ext ] = fileparts(prn_filename);
      prn_filename_basename = [prn_filename_basenameNoExt, prn_filename_ext];
      disp(['Processing ', prn_filename]);
      [type_ID, type_name] = getDataType(prn_filename);
      if strcmp(type_name, 'Probe')
        %if ( exist('Probe_patternCellArray','var')==0 ) | ( exist('Probe_patternCellArray','var')==1 & max(strcmp(prn_filename_basename,Probe_patternCellArray)) )
        if ( exist('Probe_patternCellArray','var')==0 ) | ( exist('Probe_patternCellArray','var')==1 & max(cellfun(@length,regexp(prn_filename_basename, Probe_patternCellArray))) )
          disp('plotting Probe');
          plotProbe(prn_filename, probe_col, false, [ prn_filename_folder, prn_filename_basenameNoExt, '.eps' ],true);
        end
      elseif strcmp(type_name, 'TimeSnapshot')
        if ( exist('TimeSnapshot_patternCellArray','var')==0 ) | ( exist('TimeSnapshot_patternCellArray','var')==1 & max(cellfun(@length,regexp(prn_filename_basename, TimeSnapshot_patternCellArray))) )
          disp('plotting TimeSnapshot');
          
          % loading
          handles.snapfile = fullfile(script_folder,prn_filename);
          [handles.header, handles.data] = readPrnFile(handles.snapfile);
          handles.dataSize = size(handles.data);
          columns = handles.header(:);
          if strcmp(columns(1),'y') && strcmp(columns(2),'z')
            handles.plane = 1;
          elseif strcmp(columns(1),'x') && strcmp(columns(2),'z')
            handles.plane = 2;
          else
            handles.plane = 3;
          end
          handles.AllHeaders = columns; % all headers
          
          % setting up the handles structure:
          handles.autosave = 0;
          handles.colour = 1;
          %handles.geometry = 0;
          handles.geometry = 1;
          %handles.interpolate = 0;
          handles.interpolate = 1;
          %handles.modulus = 1;
          handles.modulus = 0;
          handles.surface = 1;
  
          % time snapshot specific
          handles.Type = 2;
          col = TimeSnapshot_col;
          imageSaveName = '%BASENAME.%FIELD.max_%MAX.png';
  
          % finally plotting
          automax_time_list(end+1) = plotSnapshotSum(handles.snapfile, col, maxplotvalue, handles, false, true, imageSaveName);
        end

      elseif strcmp(type_name, 'FrequencySnapshot')
        if ( exist('FrequencySnapshot_patternCellArray','var')==0 ) | ( exist('FrequencySnapshot_patternCellArray','var')==1 & max(cellfun(@length,regexp(prn_filename_basename, FrequencySnapshot_patternCellArray))) )
          disp('plotting FrequencySnapshot');
          
          % loading
          handles.snapfile = fullfile(script_folder,prn_filename);
          [handles.header, handles.data] = readPrnFile(handles.snapfile);
          handles.dataSize = size(handles.data);
          columns = handles.header(:);
          if strcmp(columns(1),'y') && strcmp(columns(2),'z')
            handles.plane = 1;
            rotate90 = false;
            handles.drawColorBar = true;
          elseif strcmp(columns(1),'x') && strcmp(columns(2),'z')
            handles.plane = 2;
            rotate90 = true;
            handles.drawColorBar = false;
          else
            handles.plane = 3;
            rotate90 = false;
            handles.drawColorBar = true;
          end
          handles.AllHeaders = columns; % all headers
          
          % setting up the handles structure:
          handles.autosave = 0;
          handles.colour = 1;
          handles.geometry = 1;
          handles.interpolate = 0;
          handles.modulus = 0;
          handles.surface = 1;
  
          % frequency snapshot specific
          handles.Type = 3;
          col = FrequencySnapshot_col;
          imageSaveName = '%BASENAME.%FIELD.max_%MAX.lambda(nm)_%LAMBDA_SNAP_NM.freq(Mhz)_%FREQ_SNAP_MHZ.pos(mum)_%POS_MUM.png';
  
          % finally plotting
          automax_freq_list(end+1) = plotSnapshotSum(handles.snapfile, col, maxplotvalue, handles, rotate90, true, imageSaveName);
        end
      elseif strcmp(type_name, 'Reference')
        disp('skipping Reference');
      else
        warning('Unknown data type');
      end
    
      clear handles;
      clearvars handles;
    
    end % end of loop through prn files

    automax_time_avg = mean(automax_time_list);
    disp(['automax_time_avg = ',num2str(automax_time_avg)]);
    automax_freq_avg = mean(automax_freq_list);
    disp(['automax_freq_avg = ',num2str(automax_freq_avg)]);

    % restore workdir
    cd(workdir);
    
  end
  
  clear all;

end
