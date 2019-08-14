% TODO: copy/paste-able min/max values
% TODO: return usable data for manual processing
% TODO: image/figure saving
% TODO: tab interface, ability to view as external figure, to maximize, etc
% TODO: break free from Matlab by using python, octave, etc
% TODO: make it easy to install

function varargout = FIS_data_viewer(varargin)
  % FIS_DATA_VIEWER MATLAB code for FIS_data_viewer.fig
  %      FIS_DATA_VIEWER, by itself, creates a new FIS_DATA_VIEWER or raises the existing
  %      singleton*.
  %
  %      H = FIS_DATA_VIEWER returns the handle to a new FIS_DATA_VIEWER or the handle to
  %      the existing singleton*.
  %
  %      FIS_DATA_VIEWER('CALLBACK',hObject,eventData,handles,...) calls the local
  %      function named CALLBACK in FIS_DATA_VIEWER.M with the given input arguments.
  %
  %      FIS_DATA_VIEWER('Property','Value',...) creates a new FIS_DATA_VIEWER or raises the
  %      existing singleton*.  Starting from the left, property value pairs are
  %      applied to the GUI before FIS_data_viewer_OpeningFcn gets called.  An
  %      unrecognized property name or invalid value makes property application
  %      stop.  All inputs are passed to FIS_data_viewer_OpeningFcn via varargin.
  %
  %      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
  %      instance to run (singleton)".
  %
  % See also: GUIDE, GUIDATA, GUIHANDLES
  
  % Edit the above text to modify the response to help FIS_data_viewer
  
  % Last Modified by GUIDE v2.5 14-Aug-2019 19:20:09
  
  % Begin initialization code - DO NOT EDIT
  gui_Singleton = 1;
  gui_State = struct('gui_Name',       mfilename, ...
                     'gui_Singleton',  gui_Singleton, ...
                     'gui_OpeningFcn', @FIS_data_viewer_OpeningFcn, ...
                     'gui_OutputFcn',  @FIS_data_viewer_OutputFcn, ...
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

function FIS_data_viewer_OpeningFcn(hObject, eventdata, handles, varargin)
  % --- Executes just before FIS_data_viewer is made visible.
  % This function has no output args, see OutputFcn.
  % hObject    handle to figure
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  % varargin   command line arguments to FIS_data_viewer (see VARARGIN)
  
  % Choose default command line output for FIS_data_viewer
  handles.output = hObject;
  
  % Update handles structure
  guidata(hObject, handles);
  
  handles.auto_update = false;
  
  handles.Sample = FIS_getData_Default(0);
  handles.Reference = FIS_getData_Default(1);
  handles.DarkBackground = FIS_getData_Default(0);
  
  axes1D_pushbutton_reset_Callback(hObject, eventdata, handles);
  
  axes2D_Sample_pushbutton_reset_Callback(hObject, eventdata, handles);
  axes2D_Reference_pushbutton_reset_Callback(hObject, eventdata, handles);
  axes2D_DarkBackground_pushbutton_reset_Callback(hObject, eventdata, handles);
  
  update_FIS_plots(hObject, handles);
  handles.auto_update = true;
  
  % Update handles structure
  guidata(hObject, handles);
  
  % UIWAIT makes FIS_data_viewer wait for user response (see UIRESUME)
  % uiwait(handles.figure1);
end


function varargout = FIS_data_viewer_OutputFcn(hObject, eventdata, handles)
  % --- Outputs from this function are returned to the command line.
  % varargout  cell array for returning output args (see VARARGOUT);
  % hObject    handle to figure
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Get default command line output from handles structure
  varargout{1} = handles.output;
  
  % Update handles structure
  guidata(hObject, handles);
  
  %ret = struct();
  %ret.Sample = handles.Sample;
  %ret.Reference = handles.Reference;
  %ret.DarkBackground = handles.DarkBackground;
  %ret.Sample_noDB = handles.Sample_noDB;
  %ret.Reference_noDB = handles.Reference_noDB;
  %ret.Normalized = handles.Normalized;
  
  %varargout{2} = ret;
end

function editSaturationValue_Callback(hObject, eventdata, handles)
  % hObject    handle to editSaturationValue (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % Hints: get(hObject,'String') returns contents of editSaturationValue as text
  %        str2double(get(hObject,'String')) returns contents of editSaturationValue as a double
end


function editSaturationValue_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to editSaturationValue (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called

  % Hint: edit controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function axes2D_DarkBackground_pushbutton_reset_Callback(hObject, eventdata, handles)
  handles.DarkBackground = FIS_getData_Default(0);
  plot2D(handles, handles.axes2D_DarkBackground, handles.axes2D_DarkBackground_text_min, handles.axes2D_DarkBackground_text_max, handles.DarkBackground);
  if handles.auto_update
    update_FIS_plots(hObject, handles);
  end
  guidata(hObject,handles);
end

function axes2D_DarkBackground_pushbutton_load_Callback(hObject, eventdata, handles)
  handles.DarkBackground = FIS_getData();
  if length(handles.DarkBackground.Position) > 0
    plot2D(handles, handles.axes2D_DarkBackground, handles.axes2D_DarkBackground_text_min, handles.axes2D_DarkBackground_text_max, handles.DarkBackground);
    update_FIS_plots(hObject, handles);
  end
  guidata(hObject,handles);
end

function axes2D_Sample_pushbutton_load_Callback(hObject, eventdata, handles)
  handles.Sample = FIS_getData();
  if length(handles.Sample.Position) > 0
    plot2D(handles, handles.axes2D_Sample, handles.axes2D_Sample_text_min, handles.axes2D_Sample_text_max, handles.Sample);
    update_FIS_plots(hObject, handles);
  end
  guidata(hObject,handles);
end

function plot2D(handles, ax, hmin, hmax, data);
  axes(ax);
  cla;
  surf(data.Position, data.Lambda, data.Intensity);
  xlabel('position (mm)');
  ylabel('lambda (nm)');
  zlabel('intensity (AU)');
  colorbar();
  shading interp;
  axis tight;
  view(2);
  
  mini = min(data.Intensity(:));
  maxi = max(data.Intensity(:));
  setValue(handles, hmin, 'min', mini);
  setValue(handles, hmax, 'max', maxi);
  
  drawnow();
end

function axes2D_Sample_pushbutton_reset_Callback(hObject, eventdata, handles)
  handles.Sample = FIS_getData_Default(0);
  plot2D(handles, handles.axes2D_Sample, handles.axes2D_Sample_text_min, handles.axes2D_Sample_text_max, handles.Sample);
  if handles.auto_update
    update_FIS_plots(hObject, handles);
  end
  guidata(hObject,handles);
end

function axes2D_Reference_pushbutton_load_Callback(hObject, eventdata, handles)
  handles.Reference = FIS_getData();
  if length(handles.Reference.Position) > 0
    plot2D(handles, handles.axes2D_Reference, handles.axes2D_Reference_text_min, handles.axes2D_Reference_text_max, handles.Reference);
    update_FIS_plots(hObject, handles);
  end
  guidata(hObject,handles);
end

function axes2D_Reference_pushbutton_reset_Callback(hObject, eventdata, handles)
  handles.Reference = FIS_getData_Default(1);
  plot2D(handles, handles.axes2D_Reference, handles.axes2D_Reference_text_min, handles.axes2D_Reference_text_max, handles.Reference);
  if handles.auto_update
    update_FIS_plots(hObject, handles);
  end
  guidata(hObject,handles);
end

function axes1D_pushbutton_load_Callback(hObject, eventdata, handles)
  % --- Executes on button press in pushbuttonLoadFile.
  % hObject    handle to pushbuttonLoadFile (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  [filename,filepath] = uigetfile('*.txt');
  data = load(fullfile(filepath, filename));
  lambda = data(:,1);
  intensity = data(:,2);
  plot1D(handles, handles.axes1D, lambda, intensity);
end

function setValue(handles, obj, name, value)
  obj.String = sprintf('%s: %.2f', name, value);
  if value >= str2num(handles.editSaturationValue.String)
    obj.BackgroundColor = 'red';
  else
    obj.BackgroundColor = 'white';
  end
end

function axes1D_pushbutton_reset_Callback(hObject, eventdata, handles)
  plot1D(handles, handles.axes1D);
end

function plot1D(handles, ax, lambda, intensity)
  if ~exist('lambda', 'var')
    lambda = linspace(339.6, 1025.3, 2048);
  end
  if ~exist('intensity', 'var')
    intensity = linspace(0, 0, 2048);
  end
  
  axes(ax);
  cla();
  
  plot(lambda, intensity);
  xlabel('lambda (nm)');
  ylabel('intensity (AU)');
  
  mini = min(intensity(:));
  maxi = max(intensity(:));
  setValue(handles, handles.axes1D_text_min, 'min', mini);
  setValue(handles, handles.axes1D_text_max, 'max', maxi);
  
  drawnow();
end

function pushbutton_setWorkingDirectory_Callback(hObject, eventdata, handles)
  % --- Executes on button press in pushbutton_setWorkingDirectory.
  % hObject    handle to pushbutton_setWorkingDirectory (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  selpath = uigetdir();
  if ~isnumeric(selpath)
    cd(selpath);
  end
  handles.text_WorkingDirectory.String = pwd();
end

function update_FIS_plots(hObject, handles)
  
  if any(size(handles.DarkBackground.Intensity)~=size(handles.Sample.Intensity)) || any(size(handles.Reference.Intensity)~=size(handles.Sample.Intensity))
    errordlg('Data sizes do not match');
    disp('handles.Sample.Intensity');
    size(handles.Sample.Intensity)
    disp('handles.Reference.Intensity');
    size(handles.Reference.Intensity)
    disp('handles.DarkBackground.Intensity');
    size(handles.DarkBackground.Intensity)
    return
  end
  
  handles.Sample_noDB = struct();
  handles.Sample_noDB.Position = handles.Sample.Position;
  handles.Sample_noDB.Lambda = handles.Sample.Lambda;
  handles.Sample_noDB.Intensity = handles.Sample.Intensity - handles.DarkBackground.Intensity;
  plot2D(handles, handles.axes2D_Sample_noDB, handles.axes2D_Sample_noDB_text_min, handles.axes2D_Sample_noDB_text_max, handles.Sample_noDB);
  
  handles.Reference_noDB = struct();
  handles.Reference_noDB.Position = handles.Reference.Position;
  handles.Reference_noDB.Lambda = handles.Reference.Lambda;
  handles.Reference_noDB.Intensity = handles.Reference.Intensity - handles.DarkBackground.Intensity;
  plot2D(handles, handles.axes2D_Reference_noDB, handles.axes2D_Reference_noDB_text_min, handles.axes2D_Reference_noDB_text_max, handles.Reference_noDB);
  
  handles.Normalized = struct();
  handles.Normalized.Position = handles.Sample.Position;
  handles.Normalized.Lambda = handles.Sample.Lambda;
  handles.Normalized.Intensity = handles.Sample_noDB.Intensity ./ handles.Reference_noDB.Intensity;
  plot2D(handles, handles.axes2D_Normalized, handles.axes2D_Normalized_text_min, handles.axes2D_Normalized_text_max, handles.Normalized);
  
  guidata(hObject, handles);
end

function data = FIS_getData_Default(value)
  lambda = linspace(339.6, 1025.3, 2048);
  position = linspace(0, 12, 121);
  [data.Position, data.Lambda] = meshgrid(position, lambda);
  data.Intensity = value.*ones(size(data.Position));
end


% --- Executes on button press in axes1D_separate_figure.
function axes1D_separate_figure_Callback(hObject, eventdata, handles)
  % hObject    handle to axes1D_separate_figure (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  %handles.axes1D

    %Some figure you know nothing about
    %plot(rand(10,2)); %click it to make it the active figure
    %Find its handle
    %aH = gca;
    fH = ancestor(handles.axes1D, 'fig');
    fH(2) = figure(); %Figure you want to copy the stuff to
    %Copy axes or see my previous code to copy lines, store its handle
    handles.axes1D(2) = copyobj(handles.axes1D, fH(2));
    %create new axes
    handles.axes1D(3) = axes('Position',get(handles.axes1D(2),'Position'));
    linkaxes(handles.axes1D(2:3),'x');
    %Plot your new stuff
    %plot(1:10);
    %Making them look nice
    set(handles.axes1D(3),'YAxisLocation','right','Color','none');
    set(handles.axes1D(2:3),'box','off');
    xlim(handles.axes1D(1).XLim);

end
