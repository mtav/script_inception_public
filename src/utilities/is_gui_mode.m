function gui_mode = is_gui_mode()
  % return true, if GUI available
  % Matlab-only at the moment
  %
  % cf http://stackoverflow.com/questions/6754430/determine-if-matlab-has-a-display-available
  if inoctave()
    % gui_mode = isguirunning(); % Return true if Octave is running in GUI mode and false otherwise. 
    gui_mode = have_window_system(); % Return true if a window system is available (X11, Windows, or Apple OS X) and false otherwise. 
  else
    gui_mode = ( ~usejava('jvm') || feature('ShowFigureWindows') );
  end
end
