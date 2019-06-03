function startup(varargin)
    % Script to add the paths to use:
    %  * script_inception_public
    %  * script_inception_private
    %  * OpenEMS
    %
    % This script should be placed into the Matlab userpath.
    % In Matlab, you can get the userpath via the "userpath()" command.
    % Alternatively, you can symlink/place the whole public repo as the Matlab userpath.
    %
    % For GNU Octave, use .octavrc, which calls this script.
    %
    % TODO: Simplify addpath_recurse using genpath and integrate it into this script?
    % TODO: Document installation procedure.
    % TODO: Create "installer/updater", which will create/update a "pathdef.m" file for increased startup speed. git hooks might be used to automatically update pathdef.m eventually. Else manual calls to path_update() or similar will do.
    %
    % This simple solution works for octave in case of problems with this script:
    %   addpath(genpath('~/Development/script_inception_public', '.git'));
    
    % define the default locations
    if ispc()
      userDir = getenv('MYDOCUMENTS');
      if isempty(userDir)
        userDir = winqueryreg('HKEY_CURRENT_USER', ['Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'], 'Personal');
      end
      % PUBLIC_REPO_DIR_DEFAULT = fullfile('C:', 'Development', 'script_inception_public', 'src');
      PUBLIC_REPO_DIR_DEFAULT = getenv('SIP_PATH');
      PRIVATE_REPO_DIR_DEFAULT = fullfile('C:', 'Development', 'script_inception_private');
      OPENEMS_REPO_DIR_DEFAULT = fullfile('C:', 'opt', 'openEMS', 'share');
    else
      userDir = getenv('HOME');
      if isempty(userDir)
        userDir = char(java.lang.System.getProperty('user.home'));
      end
      PUBLIC_REPO_DIR_DEFAULT = fullfile(userDir, 'Development', 'script_inception_public', 'src');
      PRIVATE_REPO_DIR_DEFAULT = fullfile(userDir, 'Development', 'script_inception_private');
      OPENEMS_REPO_DIR_DEFAULT = fullfile(userDir, 'opt', 'openEMS', 'share');
    end

    if exist('OCTAVE_VERSION','builtin') ~= 0 && exist('inputParser') == 0
      error('inputParser function not found. Make sure you are using at least version 3.8.1 of Octave.')
    end

    % parse input arguments
    p = inputParser();
    p.FunctionName = 'startup';
    V = version();
    if exist('OCTAVE_VERSION','builtin') ~= 0 && str2num(V(1)) < 4
      % in GNU Octave < 4.0.0
      p = p.addParamValue('PUBLIC_REPO_DIR', PUBLIC_REPO_DIR_DEFAULT, @isdir);
      p = p.addParamValue('PRIVATE_REPO_DIR', PRIVATE_REPO_DIR_DEFAULT);
      p = p.addParamValue('OPENEMS_REPO_DIR', OPENEMS_REPO_DIR_DEFAULT);
      p = p.addParamValue('DEBUG', false, @islogical);
      p = p.parse(varargin{:});
    else
      % in Matlab or GNU Octave >= 4.0.0
      p.addParamValue('PUBLIC_REPO_DIR', PUBLIC_REPO_DIR_DEFAULT, @isdir);
      p.addParamValue('PRIVATE_REPO_DIR', PRIVATE_REPO_DIR_DEFAULT);
      p.addParamValue('OPENEMS_REPO_DIR', OPENEMS_REPO_DIR_DEFAULT);
      p.addParamValue('DEBUG', false, @islogical);
      p.parse(varargin{:});
    end
    
    % add the paths
    disp('Adding path to inoctave() ...');
    addpath(fullfile(p.Results.PUBLIC_REPO_DIR, 'utilities'));

    disp('Adding path to addpath_recurse() ...');
    addpath(fullfile(p.Results.PUBLIC_REPO_DIR, 'third_party', 'addpath_recurse'));

    disp(['Recursively adding paths from ', p.Results.PUBLIC_REPO_DIR,' ...']);
    addpath_recurse(p.Results.PUBLIC_REPO_DIR, {'.git'}, 'begin', false, p.Results.DEBUG);

    disp(['Recursively adding paths from ', p.Results.PRIVATE_REPO_DIR,' ...']);
    if exist(p.Results.PRIVATE_REPO_DIR, 'dir')
      addpath_recurse(p.Results.PRIVATE_REPO_DIR,{'.git'}, 'begin', false, p.Results.DEBUG);
    else
      disp(['PRIVATE_REPO_DIR = ', p.Results.PRIVATE_REPO_DIR,' not found. Skipping it.']);
    end

    disp(['Recursively adding paths from ', p.Results.OPENEMS_REPO_DIR,' ...']);
    if exist(p.Results.OPENEMS_REPO_DIR, 'dir')
      addpath(fullfile(p.Results.OPENEMS_REPO_DIR, 'openEMS', 'matlab'));
      addpath(fullfile(p.Results.OPENEMS_REPO_DIR, 'CSXCAD', 'matlab'));
      addpath(fullfile(p.Results.OPENEMS_REPO_DIR, 'hyp2mat', 'matlab'));
      addpath(fullfile(p.Results.OPENEMS_REPO_DIR, 'CTB', 'matlab'));
    else
      disp(['OPENEMS_REPO_DIR = ', p.Results.OPENEMS_REPO_DIR,' not found. Skipping it.']);
    end

    disp('...done');
end
