function userDir = getuserdir()
  % GETUSERDIR   return the user "home directory".
  %
  % On Windows: returns the user's "My Documents" folder.
  % On GNU/Linux: returns the user's "$HOME" folder.
  %
  % Works with Matlab and GNU Octave.
  %
  % Example:
  %   getuserdir() returns on windows XP
  %     C:\Documents and Settings\MyName\Eigene Dateien
  %
  % TODO: Test to see if getenv() works in all cases, to simplify the code.

  if ispc()
    userDir = getenv('MYDOCUMENTS');
    if isempty(userDir)
      userDir = winqueryreg('HKEY_CURRENT_USER', ['Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'], 'Personal');
    end
  else
    userDir = getenv('HOME');
    if isempty(userDir)
      userDir = char(java.lang.System.getProperty('user.home'));
    end
  end
  if isempty(userDir)
    error('Could not determine userDir.');
  end
end
