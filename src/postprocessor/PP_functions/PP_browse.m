function [handles, dirChosen] = PP_browse(handles)
  disp('function [handles, dirChosen] = PP_browse(handles)');
  % --- Executes on button press in pushbutton_browse.
  % hObject    handle to pushbutton_browse (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  handles.isLoaded = 0;

  new_dir = CrossPlatformUigetdir(handles.workdir);
  disp(['new_dir = ',new_dir])
  if new_dir == 0
    dirChosen = 0;
    return;
  end
  handles.workdir = new_dir;
  dirChosen = 1;
end
