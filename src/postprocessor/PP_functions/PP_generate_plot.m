function [ handles, ok ] = PP_generate_plot(handles)
  disp('function pushbutton_generate_plot_Callback(hObject, eventdata, handles)')
  % hObject    handle to pushbutton_generate_plot (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % default return value
  ok = 0;

  if ~handles.isLoaded
    disp('WARNING: Please load a file first');
    uiwait(warndlg('WARNING: Please load a file first', 'No data loaded'));
    ok = 0;
    return;
  end
  
  col = handles.col;
  handles.dataname = handles.AllHeaders(col);
  zlimits = [ handles.minplotvalue, handles.maxplotvalue ];
  
  if handles.Type == 1 % probe file
    if handles.FFT_f_or_lambda==1
      FFT_x_axis_type = 'frequency';
    else
      FFT_x_axis_type = 'wavelength';
    end
    plotProbe('filename', handles.ProbeFile,...
              'column', handles.col,...
              'DoAnalysis', logical(handles.DoAnalysis),...
              'tlim', [handles.tmin_mus, handles.tmax_mus],...
              'harminv_range', [handles.harminv_lambdaLow_mum, handles.harminv_lambdaHigh_mum],...
              'harminv_range_type', 'wavelength',...
              'FFT_x_axis_type', FFT_x_axis_type,...
              'FFT_xlabel', handles.FFT_xlabel,...
              'FFT_scalingFactor', handles.FFT_scalingFactor,...
              'handles', handles);
  %elseif handles.Type == 2
    %handles.snapfile = handles.TimeSnapshotFile;
    %plotSnapshot(handles.snapfile, col, zlimits, handles);
  %elseif handles.Type == 3
    %handles.snapfile = handles.FrequencySnapshotFile;
    %plotSnapshot(handles.snapfile, col, zlimits, handles);
  %elseif handles.Type == 4
    %handles.snapfile = handles.ExcitationTemplateFile;
    %plotSnapshot(handles.snapfile, col, zlimits, handles);
  %elseif handles.Type == 5
    %handles.snapfile = handles.SnapshotFile;
    %plotSnapshot(handles.snapfile, col, zlimits, handles);
  else % snapshot file assumed by default
    %plotSnapshot(handles.snapfile, col, zlimits, handles);
    PP_plotSnapshot(handles);
    %error('Unknown data type');
    %ok = 0;
    %return;
  end
  
  ok = 1;
end
