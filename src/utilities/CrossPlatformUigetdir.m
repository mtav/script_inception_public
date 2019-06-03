function DIR = CrossPlatformUigetdir(dir)
  % Created for versions of GNU octave not supporting uigetdir.
  % uigetdir is supported in GNU Octave version 3.6.1 and later. (at least on a GNU/Linux system)
  % Requires the zenity package for GNU Octave.
  if inoctave()
    pkg load zenity;
    DIR = zenity_file_selection('hello', dir, 'directory');
  else
    DIR = uigetdir(dir);
  end
end

% REFERENCE:
%Function File: zenity_file_selection (title, option1, ...)

    %Opens a file selection dialog. The variable title sets the title of the file selection window. The optional string arguments can be

    %‘save’
        %The file selection dialog is a dialog for saving files.
    %‘multiple’
        %It is possible to select multiple files.
    %‘directory’
        %It is possible to select directories as well as files.
    %‘Anything else’
        %The argument will be the default selected file. 

    %and error. 
