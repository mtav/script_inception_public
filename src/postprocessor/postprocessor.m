function varargout = postprocessor(varargin)
  % Note: This function is called on almost every change in the GUI.
  % TODO: Add dimensions auto-detect feature (or manual dimension entering) to enable plotting of .prn files without .geo or .inp files.
  
  %
  % usage examples:
  % postprocessor
  % postprocessor({'H:\DATA\IN\loncar_test_4'})
  %
  % postprocessor v4, written by Ian Buss 2007
  %
  % POSTPROCESSOR M-file for postprocessor.fig
  %      POSTPROCESSOR, by itself, creates a new POSTPROCESSOR or raises the existing
  %      singleton*.
  %
  %      H = POSTPROCESSOR returns the handle to a new POSTPROCESSOR or the handle to
  %      the existing singleton*.
  %
  %      POSTPROCESSOR('CALLBACK',hObject,eventData,handles,...) calls the local
  %      function named CALLBACK in POSTPROCESSOR.M with the given input arguments.
  %
  %      POSTPROCESSOR('Property', 'Value',...) creates a new POSTPROCESSOR or raises the
  %      existing singleton*.  Starting from the left, property value pairs are
  %      applied to the GUI before postprocessor_OpeningFunction gets called.  An
  %      unrecognized property name or invalid value makes property application
  %      stop.  All inputs are passed to postprocessor_OpeningFcn via varargin.
  %
  %      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
  %      instance to run (singleton)".
  %
  % See also: GUIDE, GUIDATA, GUIHANDLES
  
  % Copyright 2002-2003 The MathWorks, Inc.
  
  % Edit the above text to modify the response to help postprocessor
  
  % Last Modified by GUIDE v2.5 07-Nov-2016 16:13:38
  
  % Begin initialization code - DO NOT EDIT
  gui_Singleton = 1;
  gui_State = struct('gui_Name',       mfilename, ...
                     'gui_Singleton',  gui_Singleton, ...
                     'gui_OpeningFcn', @postprocessor_OpeningFcn, ...
                     'gui_OutputFcn',  @postprocessor_OutputFcn, ...
                     'gui_LayoutFcn',  [] , ...
                     'gui_Callback',   []);
  if nargin && ischar(varargin{1})
      gui_State.gui_Callback = str2func(varargin{1});
  end
  
  if nargout
      [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
  else
      gui_mainfcn(gui_State, varargin{:});
  end
  % End initialization code - DO NOT EDIT
end

function postprocessor_OpeningFcn(hObject, eventdata, handles, varargin)
  % --- Executes just before postprocessor is made visible.
  % This function has no output args, see OutputFcn.
  % hObject    handle to figure
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  % varargin   command line arguments to postprocessor (see VARARGIN)

  % Choose default command line output for postprocessor
  handles.output = hObject;

  % to prevent errors on attempts to plot before loading
  handles.isLoaded = 0;

  disp('=== ARGUMENT INFO ===')
  disp(['nargin = ',num2str(nargin)]);
  disp(['nargout = ',num2str(nargout)]);
  for k = 1:length(varargin)
    disp(varargin{k});
  end
  disp('=====================')
  
  if nargin>4
    disp('We have input');
  end
  
  % set default value
  handles.workdir = pwd();
  
  % set GUI default values
  set(handles.radiobutton_TimeSnapshot, 'Value', 1);
  set(handles.checkbox_geometry, 'Value', 0);
  set(handles.checkbox_epsilon_contour, 'Value', 0);
  set(handles.radiobutton_surface, 'Value', 1);
  
  set(handles.checkbox_useAdaptedMaxIfIsNaN, 'Value', 1);
  set(handles.checkbox_symmetricRange, 'Value', 0);
  set(handles.checkbox_LimitToBox, 'Value', 1);
  
  set(handles.edit_tmin_mus, 'String', 6e-8);
  
  set(handles.edit_FFTrange_min_mum, 'String', '');
  set(handles.edit_FFTrange_max_mum, 'String', '');
  
  set(handles.checkbox_useFFTrange, 'Value', 0);
  set(handles.checkbox_autoZoomFFT, 'Value', 1);
  
  set(handles.checkbox_DoAnalysis, 'Value', 1);
  
  set(handles.checkbox_pre_2008_BFDTD_version, 'Value', 0);
  
  % TODO: Proper unit management system, but this GUI is scheduled for full replacement at some point anyway...
  set(handles.popupmenu_FFT_f_or_lambda, 'Value',2);
  set(handles.edit_FFT_xlabel,'String', '\lambda (nm)');
  set(handles.edit_FFT_scalingFactor,'String', 1000);
  
  % CLI input arg handling
  if nargin > 3
    if exist(varargin{1}{1},'dir')
      handles.workdir = varargin{1}{1};
    else
      %errordlg({'Input argument must be a valid folder'},'Input Argument Error!');
      disp('WARNING: Input Argument Error!: Input argument must be a valid folder');
      guidata(hObject, handles);
    end
  end

  [handles] = setupListsGUI(handles);

  % Update handles structure
  guidata(hObject, handles);

  % UIWAIT makes postprocessor wait for user response (see UIRESUME)
  % uiwait(handles.figure1);
end

function varargout = postprocessor_OutputFcn(hObject, eventdata, handles)
  % --- Outputs from this function are returned to the command line.
  % varargout  cell array for returning output args (see VARARGOUT);
  % hObject    handle to figure
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Get default command line output from handles structure
  varargout{1} = handles.output;
end

function popupmenu_Probe_Callback(hObject, eventdata, handles)
  % --- Executes on selection change in popupmenu_Probe.
  % hObject    handle to popupmenu_Probe (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hints: contents = get(hObject,'String') returns popupmenu_Probe contents as cell array
  %        contents{get(hObject, 'Value')} returns selected item from popupmenu_Probe
end

function popupmenu_Probe_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to popupmenu_Probe (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called
  
  % Hint: popupmenu controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function popupmenu_inputfile_Callback(hObject, eventdata, handles)
  % --- Executes on selection change in popupmenu_inputfile.
  % hObject    handle to popupmenu_inputfile (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hints: contents = get(hObject,'String') returns popupmenu_inputfile contents as cell array
  %        contents{get(hObject, 'Value')} returns selected item from popupmenu_inputfile
end

function popupmenu_inputfile_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to popupmenu_inputfile (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called
  
  % Hint: popupmenu controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function pushbutton_load_data_Callback(hObject, eventdata, handles)
  % get from GUI
  if get(handles.radiobutton_Probe, 'Value')
    handles.Type = 1;
  end
  if get(handles.radiobutton_TimeSnapshot, 'Value');
    handles.Type = 2;
  end
  if get(handles.radiobutton_FrequencySnapshot, 'Value');
    handles.Type = 3;
  end
  if get(handles.radiobutton_ExcitationTemplate, 'Value');
    handles.Type = 4;
  end
  if get(handles.radiobutton_Snapshot, 'Value');
    handles.Type = 5;
  end
  if get(handles.radiobutton_EnergySnapshot, 'Value');
    handles.Type = 6;
  end
  
  handles.ProbeID = get(handles.popupmenu_Probe, 'Value');
  handles.TimeSnapshotID = get(handles.popupmenu_TimeSnapshot, 'Value');
  handles.FrequencySnapshotID = get(handles.popupmenu_FrequencySnapshot, 'Value');
  handles.ExcitationTemplateID = get(handles.popupmenu_ExcitationTemplate, 'Value');
  handles.SnapshotID = get(handles.popupmenu_Snapshot, 'Value');
  handles.geometryfile = get(handles.popupmenu_geometryfile, 'Value');
  handles.inputfile = get(handles.popupmenu_inputfile, 'Value');
  
  handles.SaveEnergySnapshot = logical(get(handles.checkbox_SaveEnergySnapshot, 'Value'));
  handles.epsilon0_factor = logical(get(handles.checkbox_epsilon0_factor, 'Value'));
  handles.epsilon_only = logical(get(handles.checkbox_epsilon_only, 'Value'));
  
  handles.pre_2008_BFDTD_version = logical(get(handles.checkbox_pre_2008_BFDTD_version, 'Value'));
  
  handles.epsilon_dir = get(handles.edit_epsilon_directory,'String');
  
  % load data
  [ handles ] = PP_load_data(handles);
  
  % set to GUI
  if handles.isLoaded
    setPopup(handles.popupmenu_plotcolumn, handles.HeadersForPopupList);
    set(handles.text11, 'String', ['Loaded data: ', handles.snapfile]);
  else
    setPopup(handles.popupmenu_plotcolumn, {''});
    set(handles.text11, 'String', ['Loaded data: ', {''}]);
  end

  guidata(hObject, handles);
end

function popupmenu_geometryfile_Callback(hObject, eventdata, handles)
  % --- Executes on selection change in popupmenu_geometryfile.
  % hObject    handle to popupmenu_geometryfile (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hints: contents = get(hObject,'String') returns popupmenu_geometryfile contents as cell array
  %        contents{get(hObject, 'Value')} returns selected item from popupmenu_geometryfile
end

function popupmenu_geometryfile_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to popupmenu_geometryfile (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called
  
  % Hint: popupmenu controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function popupmenu_plotcolumn_Callback(hObject, eventdata, handles)
  % --- Executes on selection change in popupmenu_plotcolumn.
  % hObject    handle to popupmenu_plotcolumn (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hints: contents = get(hObject,'String') returns popupmenu_plotcolumn contents as cell array
  %        contents{get(hObject, 'Value')} returns selected item from popupmenu_plotcolumn
  
  
  % --- Executes during object creation, after setting all properties.
end

function popupmenu_plotcolumn_CreateFcn(hObject, eventdata, handles)
  % hObject    handle to popupmenu_plotcolumn (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called
  
  % Hint: popupmenu controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function pushbutton_generate_plot_Callback(hObject, eventdata, handles)
  % hObject    handle to pushbutton_generate_plot (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % get from GUI
  handles.col = get(handles.popupmenu_plotcolumn, 'Value');
  %if get(handles.radiobutton_Probe, 'Value')
    %handles.col = get(handles.popupmenu_plotcolumn, 'Value')+1;
  %end
  %if get(handles.radiobutton_TimeSnapshot, 'Value');
    %handles.col = get(handles.popupmenu_plotcolumn, 'Value')+2;
  %end
  %if get(handles.radiobutton_FrequencySnapshot, 'Value');
    %handles.col = get(handles.popupmenu_plotcolumn, 'Value')+2;
  %end
  %if get(handles.radiobutton_ExcitationTemplate, 'Value');
    %handles.col = get(handles.popupmenu_plotcolumn, 'Value')+2;
  %end
  %if get(handles.radiobutton_Snapshot, 'Value');
    %handles.col = get(handles.popupmenu_plotcolumn, 'Value')+2;
  %end
  
  handles.minplotvalue = str2double(get(handles.edit_minplotvalue,'String'));
  handles.maxplotvalue = str2double(get(handles.edit_maxplotvalue,'String'));
  
  handles.interpolate = get(handles.checkbox_interpolate, 'Value');
  handles.autosave = logical(get(handles.checkbox_autosave, 'Value'));
  handles.geometry = get(handles.checkbox_geometry, 'Value');
  handles.epsilon_contour = get(handles.checkbox_epsilon_contour, 'Value');
  handles.modulus = get(handles.checkbox_modulus, 'Value');

  handles.symmetricRange = get(handles.checkbox_symmetricRange, 'Value');
  handles.useAdaptedMaxIfIsNaN = get(handles.checkbox_useAdaptedMaxIfIsNaN, 'Value');

  handles.LimitToBox = get(handles.checkbox_LimitToBox, 'Value');

  handles.colour = get(handles.radiobutton_colour, 'Value');
  handles.surface = get(handles.radiobutton_surface, 'Value');

  handles.tmin_mus = str2double(get(handles.edit_tmin_mus, 'String'));
  handles.tmax_mus = str2double(get(handles.edit_tmax_mus, 'String'));

  handles.harminv_lambdaLow_mum = str2double(get(handles.edit_harminv_lambdaLow_mum, 'String'));
  handles.harminv_lambdaHigh_mum = str2double(get(handles.edit_harminv_lambdaHigh_mum, 'String'));

  handles.FFTrange_min_mum = str2double(get(handles.edit_FFTrange_min_mum, 'String'));
  handles.FFTrange_max_mum = str2double(get(handles.edit_FFTrange_max_mum, 'String'));

  handles.plot_time_Xmin = str2double(get(handles.edit_time_Xmin, 'String'));
  handles.plot_time_Xmax = str2double(get(handles.edit_time_Xmax, 'String'));
  handles.plot_time_Ymin = str2double(get(handles.edit_time_Ymin, 'String'));
  handles.plot_time_Ymax = str2double(get(handles.edit_time_Ymax, 'String'));

  handles.plot_FFT_Xmin = str2double(get(handles.edit_FFT_Xmin, 'String'));
  handles.plot_FFT_Xmax = str2double(get(handles.edit_FFT_Xmax, 'String'));
  handles.plot_FFT_Ymin = str2double(get(handles.edit_FFT_Ymin, 'String'));
  handles.plot_FFT_Ymax = str2double(get(handles.edit_FFT_Ymax, 'String'));
  
  handles.useFFTrange = get(handles.checkbox_useFFTrange, 'Value');
  handles.autoZoomFFT = get(handles.checkbox_autoZoomFFT, 'Value');
  handles.autoZoomTime = get(handles.checkbox_autoZoomTime, 'Value');

  handles.DoAnalysis = get(handles.checkbox_DoAnalysis, 'Value');

  handles.FFT_f_or_lambda = get(handles.popupmenu_FFT_f_or_lambda, 'Value');
  handles.FFT_xlabel = get(handles.edit_FFT_xlabel,'String');
  handles.FFT_scalingFactor = str2double(get(handles.edit_FFT_scalingFactor,'String'));

  % generate plot
  [ handles, ok ] = PP_generate_plot(handles);

  guidata(hObject,handles);
end

function setPopup(popup, value_list)

  % populate the popup list
  if length(value_list) > 0
    set(popup, 'String', value_list);
  else
    set(popup, 'String', {''});
  end
    
  % make sure that the current index is within the popup range
  val = get(popup, 'Value');
  if ( val < 1 ) | ( length(value_list) < val )
    set(popup, 'Value', 1);
  end

end

function [handles] = setupListsGUI(handles)
  [handles, ok] = PP_setupLists(handles);
  if ok
    set(handles.label_working_directory,'String',handles.workdir);
    setPopup(handles.popupmenu_Probe, handles.ProbeList);
    setPopup(handles.popupmenu_TimeSnapshot, handles.TimeSnapshotList);
    setPopup(handles.popupmenu_FrequencySnapshot, handles.FrequencySnapshotList);
    setPopup(handles.popupmenu_ExcitationTemplate, handles.ExcitationTemplateList);
    setPopup(handles.popupmenu_Snapshot, handles.SnapshotList);
    setPopup(handles.popupmenu_geometryfile, handles.geolist);    
    setPopup(handles.popupmenu_inputfile, handles.inplist);
  end
end

function pushbutton_browse_Callback(hObject, eventdata, handles)
  % --- Executes on button press in pushbutton_browse.
  % hObject    handle to pushbutton_browse (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % get from GUI
  handles.workdir = get(handles.label_working_directory,'String');
  
  % browse
  [handles, dirChosen] = PP_browse(handles);

  if ~dirChosen
    return;
  end
  
  % set to GUI
  [handles] = setupListsGUI(handles); % calls PP_setupLists at start

  guidata(hObject,handles);
end

function checkbox_interpolate_Callback(hObject, eventdata, handles)
  % --- Executes on button press in checkbox_interpolate.
  % hObject    handle to checkbox_interpolate (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hint: get(hObject, 'Value') returns toggle state of checkbox_interpolate
end

function checkbox_autosave_Callback(hObject, eventdata, handles)
  % --- Executes on button press in checkbox_autosave.
  % hObject    handle to checkbox_autosave (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hint: get(hObject, 'Value') returns toggle state of checkbox_autosave
end

function checkbox_geometry_Callback(hObject, eventdata, handles)
  % --- Executes on button press in checkbox_geometry.
  % hObject    handle to checkbox_geometry (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hint: get(hObject, 'Value') returns toggle state of checkbox_geometry
end

function checkbox_modulus_Callback(hObject, eventdata, handles)
  % --- Executes on button press in checkbox_modulus.
  % hObject    handle to checkbox_modulus (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hint: get(hObject, 'Value') returns toggle state of checkbox_modulus
end

function popupmenu_FrequencySnapshot_Callback(hObject, eventdata, handles)
  % --- Executes on selection change in popupmenu_FrequencySnapshot.
  % hObject    handle to popupmenu_FrequencySnapshot (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hints: contents = get(hObject,'String') returns popupmenu_FrequencySnapshot contents as cell array
  %        contents{get(hObject, 'Value')} returns selected item from popupmenu_FrequencySnapshot
end

function popupmenu_FrequencySnapshot_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to popupmenu_FrequencySnapshot (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called
  
  % Hint: popupmenu controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function popupmenu_TimeSnapshot_Callback(hObject, eventdata, handles)
  % --- Executes on selection change in popupmenu_TimeSnapshot.
  % hObject    handle to popupmenu_TimeSnapshot (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hints: contents = get(hObject,'String') returns popupmenu_TimeSnapshot contents as cell array
  %        contents{get(hObject, 'Value')} returns selected item from popupmenu_TimeSnapshot
end

function popupmenu_TimeSnapshot_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to popupmenu_TimeSnapshot (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called
  
  % Hint: popupmenu controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function radiobutton_Probe_Callback(hObject, eventdata, handles)
  % --- Executes on button press in radiobutton_Probe.
  % hObject    handle to radiobutton_Probe (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hint: get(hObject, 'Value') returns toggle state of radiobutton_Probe
end

function radiobutton_TimeSnapshot_Callback(hObject, eventdata, handles)
  % --- Executes on button press in radiobutton_TimeSnapshot.
  % hObject    handle to radiobutton_TimeSnapshot (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hint: get(hObject, 'Value') returns toggle state of radiobutton_TimeSnapshot
end

function radiobutton_FrequencySnapshot_Callback(hObject, eventdata, handles)
  % --- Executes on button press in radiobutton_FrequencySnapshot.
  % hObject    handle to radiobutton_FrequencySnapshot (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  % Hint: get(hObject, 'Value') returns toggle state of radiobutton_FrequencySnapshot
end


function popupmenu_ExcitationTemplate_Callback(hObject, eventdata, handles)
  % --- Executes on selection change in popupmenu_ExcitationTemplate.
  % hObject    handle to popupmenu_ExcitationTemplate (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hints: contents = get(hObject,'String') returns popupmenu_ExcitationTemplate contents as cell array
  %        contents{get(hObject, 'Value')} returns selected item from popupmenu_ExcitationTemplate
end

function popupmenu_ExcitationTemplate_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to popupmenu_ExcitationTemplate (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called
  
  % Hint: popupmenu controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function popupmenu_Snapshot_Callback(hObject, eventdata, handles)
  % --- Executes on selection change in popupmenu_Snapshot.
  % hObject    handle to popupmenu_Snapshot (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hints: contents = get(hObject,'String') returns popupmenu_Snapshot contents as cell array
  %        contents{get(hObject, 'Value')} returns selected item from popupmenu_Snapshot
end

function popupmenu_Snapshot_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to popupmenu_Snapshot (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called
  
  % Hint: popupmenu controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function edit_minplotvalue_Callback(hObject, eventdata, handles)
  % hObject    handle to edit_minplotvalue (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hints: get(hObject,'String') returns contents of edit_minplotvalue as text
  %        str2double(get(hObject,'String')) returns contents of edit_minplotvalue as a double
end

function edit_minplotvalue_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to edit_minplotvalue (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called

  % Hint: edit controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function edit_maxplotvalue_Callback(hObject, eventdata, handles)
  % hObject    handle to edit_maxplotvalue (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hints: get(hObject,'String') returns contents of edit_maxplotvalue as text
  %        str2double(get(hObject,'String')) returns contents of edit_maxplotvalue as a double
end

function edit_maxplotvalue_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to edit_maxplotvalue (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called
  
  % Hint: edit controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end


function checkbox_useAdaptedMaxIfIsNaN_Callback(hObject, eventdata, handles)
  % --- Executes on button press in checkbox_useAdaptedMaxIfIsNaN.
  % hObject    handle to checkbox_useAdaptedMaxIfIsNaN (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hint: get(hObject, 'Value') returns toggle state of checkbox_useAdaptedMaxIfIsNaN
end

function checkbox_symmetricRange_Callback(hObject, eventdata, handles)
  % --- Executes on button press in checkbox_symmetricRange.
  % hObject    handle to checkbox_symmetricRange (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hint: get(hObject, 'Value') returns toggle state of checkbox_symmetricRange
end

function edit_tmin_mus_Callback(hObject, eventdata, handles)
  % hObject    handle to edit_tmin_mus (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hints: get(hObject,'String') returns contents of edit_tmin_mus as text
  %        str2double(get(hObject,'String')) returns contents of edit_tmin_mus as a double
end

function edit_tmin_mus_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to edit_tmin_mus (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called

  % Hint: edit controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function edit_tmax_mus_Callback(hObject, eventdata, handles)
  % hObject    handle to edit_tmax_mus (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hints: get(hObject,'String') returns contents of edit_tmax_mus as text
  %        str2double(get(hObject,'String')) returns contents of edit_tmax_mus as a double


  % --- Executes during object creation, after setting all properties.
end

function edit_tmax_mus_CreateFcn(hObject, eventdata, handles)
  % hObject    handle to edit_tmax_mus (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called

  % Hint: edit controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function checkbox_LimitToBox_Callback(hObject, eventdata, handles)
  % --- Executes on button press in checkbox_LimitToBox.
  % hObject    handle to checkbox_LimitToBox (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hint: get(hObject, 'Value') returns toggle state of checkbox_LimitToBox
end

function checkbox_autoZoomFFT_Callback(hObject, eventdata, handles)
  % --- Executes on button press in checkbox_autoZoomFFT.
  % hObject    handle to checkbox_autoZoomFFT (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hint: get(hObject, 'Value') returns toggle state of checkbox_autoZoomFFT
end

function edit_harminv_lambdaLow_mum_Callback(hObject, eventdata, handles)
  % hObject    handle to edit_harminv_lambdaLow_mum (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hints: get(hObject,'String') returns contents of edit_harminv_lambdaLow_mum as text
  %        str2double(get(hObject,'String')) returns contents of edit_harminv_lambdaLow_mum as a double
end

function edit_harminv_lambdaLow_mum_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to edit_harminv_lambdaLow_mum (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called

  % Hint: edit controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function edit_harminv_lambdaHigh_mum_Callback(hObject, eventdata, handles)
  % hObject    handle to edit_harminv_lambdaHigh_mum (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hints: get(hObject,'String') returns contents of edit_harminv_lambdaHigh_mum as text
  %        str2double(get(hObject,'String')) returns contents of edit_harminv_lambdaHigh_mum as a double
end

function edit_harminv_lambdaHigh_mum_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to edit_harminv_lambdaHigh_mum (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called

  % Hint: edit controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function edit_FFTrange_min_mum_Callback(hObject, eventdata, handles)
  % hObject    handle to edit_FFTrange_min_mum (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hints: get(hObject,'String') returns contents of edit_FFTrange_min_mum as text
  %        str2double(get(hObject,'String')) returns contents of edit_FFTrange_min_mum as a double
end

function edit_FFTrange_min_mum_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to edit_FFTrange_min_mum (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called

  % Hint: edit controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function edit_FFTrange_max_mum_Callback(hObject, eventdata, handles)
  % hObject    handle to edit_FFTrange_max_mum (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hints: get(hObject,'String') returns contents of edit_FFTrange_max_mum as text
  %        str2double(get(hObject,'String')) returns contents of edit_FFTrange_max_mum as a double
end

function edit_FFTrange_max_mum_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to edit_FFTrange_max_mum (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called

  % Hint: edit controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function checkbox_useFFTrange_Callback(hObject, eventdata, handles)
  % --- Executes on button press in checkbox_useFFTrange.
  % hObject    handle to checkbox_useFFTrange (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hint: get(hObject, 'Value') returns toggle state of checkbox_useFFTrange
end

function checkbox_DoAnalysis_Callback(hObject, eventdata, handles)
  % --- Executes on button press in checkbox_DoAnalysis.
  % hObject    handle to checkbox_DoAnalysis (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hint: get(hObject, 'Value') returns toggle state of checkbox_DoAnalysis
end

function popupmenu_FFT_f_or_lambda_Callback(hObject, eventdata, handles)
  % --- Executes on selection change in popupmenu_FFT_f_or_lambda.
  % hObject    handle to popupmenu_FFT_f_or_lambda (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hints: contents = cellstr(get(hObject,'String')) returns popupmenu_FFT_f_or_lambda contents as cell array
  %        contents{get(hObject, 'Value')} returns selected item from popupmenu_FFT_f_or_lambda
end

function popupmenu_FFT_f_or_lambda_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to popupmenu_FFT_f_or_lambda (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called

  % Hint: popupmenu controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function edit_FFT_scalingFactor_Callback(hObject, eventdata, handles)
  % hObject    handle to edit_FFT_scalingFactor (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hints: get(hObject,'String') returns contents of edit_FFT_scalingFactor as text
  %        str2double(get(hObject,'String')) returns contents of edit_FFT_scalingFactor as a double
end

function edit_FFT_scalingFactor_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to edit_FFT_scalingFactor (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called

  % Hint: edit controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function edit_FFT_xlabel_Callback(hObject, eventdata, handles)
  % hObject    handle to edit_FFT_xlabel (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hints: get(hObject,'String') returns contents of edit_FFT_xlabel as text
  %        str2double(get(hObject,'String')) returns contents of edit_FFT_xlabel as a double
end

function edit_FFT_xlabel_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to edit_FFT_xlabel (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called

  % Hint: edit controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function edit_time_Xmin_Callback(hObject, eventdata, handles)
  % hObject    handle to edit_time_Xmin (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hints: get(hObject,'String') returns contents of edit_time_Xmin as text
  %        str2double(get(hObject,'String')) returns contents of edit_time_Xmin as a double
end

function edit_time_Xmin_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to edit_time_Xmin (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called

  % Hint: edit controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function edit_time_Xmax_Callback(hObject, eventdata, handles)
  % hObject    handle to edit_time_Xmax (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hints: get(hObject,'String') returns contents of edit_time_Xmax as text
  %        str2double(get(hObject,'String')) returns contents of edit_time_Xmax as a double
end

function edit_time_Xmax_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to edit_time_Xmax (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called

  % Hint: edit controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function edit_time_Ymin_Callback(hObject, eventdata, handles)
  % hObject    handle to edit_time_Ymin (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hints: get(hObject,'String') returns contents of edit_time_Ymin as text
  %        str2double(get(hObject,'String')) returns contents of edit_time_Ymin as a double
end

function edit_time_Ymin_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to edit_time_Ymin (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called

  % Hint: edit controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function edit_time_Ymax_Callback(hObject, eventdata, handles)
  % hObject    handle to edit_time_Ymax (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hints: get(hObject,'String') returns contents of edit_time_Ymax as text
  %        str2double(get(hObject,'String')) returns contents of edit_time_Ymax as a double
end

function edit_time_Ymax_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to edit_time_Ymax (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called

  % Hint: edit controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function edit_FFT_Xmin_Callback(hObject, eventdata, handles)
  % hObject    handle to edit_FFT_Xmin (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hints: get(hObject,'String') returns contents of edit_FFT_Xmin as text
  %        str2double(get(hObject,'String')) returns contents of edit_FFT_Xmin as a double
end

function edit_FFT_Xmin_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to edit_FFT_Xmin (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called

  % Hint: edit controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function edit_FFT_Xmax_Callback(hObject, eventdata, handles)
  % hObject    handle to edit_FFT_Xmax (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hints: get(hObject,'String') returns contents of edit_FFT_Xmax as text
  %        str2double(get(hObject,'String')) returns contents of edit_FFT_Xmax as a double
end

function edit_FFT_Xmax_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to edit_FFT_Xmax (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called

  % Hint: edit controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function edit_FFT_Ymin_Callback(hObject, eventdata, handles)
  % hObject    handle to edit_FFT_Ymin (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hints: get(hObject,'String') returns contents of edit_FFT_Ymin as text
  %        str2double(get(hObject,'String')) returns contents of edit_FFT_Ymin as a double
end

function edit_FFT_Ymin_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to edit_FFT_Ymin (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called

  % Hint: edit controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function edit_FFT_Ymax_Callback(hObject, eventdata, handles)
  % hObject    handle to edit_FFT_Ymax (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hints: get(hObject,'String') returns contents of edit_FFT_Ymax as text
  %        str2double(get(hObject,'String')) returns contents of edit_FFT_Ymax as a double
end

function edit_FFT_Ymax_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to edit_FFT_Ymax (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called

  % Hint: edit controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function checkbox_autoZoomTime_Callback(hObject, eventdata, handles)
  % --- Executes on button press in checkbox_autoZoomTime.
  % hObject    handle to checkbox_autoZoomTime (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hint: get(hObject, 'Value') returns toggle state of checkbox_autoZoomTime
end

function checkbox_SaveEnergySnapshot_Callback(hObject, eventdata, handles)
  % --- Executes on button press in checkbox_SaveEnergySnapshot.
  % hObject    handle to checkbox_SaveEnergySnapshot (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hint: get(hObject, 'Value') returns toggle state of checkbox_SaveEnergySnapshot
end

function checkbox_epsilon0_factor_Callback(hObject, eventdata, handles)
  % --- Executes on button press in checkbox_epsilon0_factor.
  % hObject    handle to checkbox_epsilon0_factor (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hint: get(hObject,'Value') returns toggle state of checkbox_epsilon0_factor
end

function pushbutton_epsilon_directory_Callback(hObject, eventdata, handles)
  % --- Executes on button press in pushbutton_epsilon_directory.
  % hObject    handle to pushbutton_epsilon_directory (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % get from GUI
  handles.epsilon_dir = get(handles.edit_epsilon_directory,'String');
  
  % browse
  new_dir = CrossPlatformUigetdir(handles.epsilon_dir);
  
  % set to GUI
  if new_dir ~= 0
    handles.epsilon_dir = new_dir;
    set(handles.edit_epsilon_directory,'String',handles.epsilon_dir);
  end
  
  % TODO: We should maybe list the epsilon snapshots from the epsilon dir
  % in a dropdown list as well, so the user can choose from them?
  
  guidata(hObject,handles);
end

function edit_epsilon_directory_Callback(hObject, eventdata, handles)
  % hObject    handle to edit_epsilon_directory (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  % Hints: get(hObject,'String') returns contents of edit_epsilon_directory as text
  %        str2double(get(hObject,'String')) returns contents of edit_epsilon_directory as a double
end

function edit_epsilon_directory_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to edit_epsilon_directory (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called
  % Hint: edit controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
  end
end

function checkbox_auto_epsilon_Callback(hObject, eventdata, handles)
  % --- Executes on button press in checkbox_auto_epsilon.
  % hObject    handle to checkbox_auto_epsilon (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  % Hint: get(hObject,'Value') returns toggle state of checkbox_auto_epsilon
end


function checkbox_epsilon_only_Callback(hObject, eventdata, handles)
  % --- Executes on button press in checkbox_epsilon_only.
  % hObject    handle to checkbox_epsilon_only (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hint: get(hObject,'Value') returns toggle state of checkbox_epsilon_only
end

function checkbox_epsilon_contour_Callback(hObject, eventdata, handles)
  % --- Executes on button press in checkbox_epsilon_contour.
  % hObject    handle to checkbox_epsilon_contour (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hint: get(hObject,'Value') returns toggle state of checkbox_epsilon_contour
end

function checkbox_pre_2008_BFDTD_version_Callback(hObject, eventdata, handles)
  % --- Executes on button press in checkbox_pre_2008_BFDTD_version.
  % hObject    handle to checkbox_pre_2008_BFDTD_version (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hint: get(hObject,'Value') returns toggle state of checkbox_pre_2008_BFDTD_version
end
