function uTest_GetFullPath(doSpeed)  %#ok<INUSD>
% Automatic test: GetFullPath
% This is a routine for automatic testing. It is not needed for processing and
% can be deleted or moved to a folder, where it does not bother.
%
% uTest_GetFullPath(doSpeed)
% INPUT:
%   doSpeed: Optional logical flag to trigger time consuming speed tests.
%            Default: TRUE. If no speed test is defined, this is ignored.
% OUTPUT:
%   On failure the test stops with an error.
%
% Tested: Matlab 6.5, 7.7, 7.8, 7.13, WinXP/32, Win7/64
% Author: Jan Simon, Heidelberg, (C) 2009-2011 matlab.THISYEAR(a)nMINUSsimon.de

% $JRev: R-l V:033 Sum:Gk9Dkqf0xCIU Date:22-Oct-2011 02:45:41 $
% $License: BSD $
% $File: Tools\UnitTests_\uTest_GetFullPath.m $
% History:
% 024: 25-Oct-2009 16:48, BUGFIX: Tests of rejected bad input were too lazy.
% 028: 21-Jul-2010 10:48, Text UNC paths.
% 031: 24-Jan-2011 11:20, Cell string input.

% Initialize: ==================================================================
FuncName = 'uTest_GetFullPath';  % $Managed by AutoFuncPath$
FSep      = filesep;
whichFunc = which('GetFullPath');
ErrID     = ['JSimon:', mfilename, ':Failed'];
% myFunc    = mfilename('fullpath');

[dum1, dum2, funcExt] = fileparts(whichFunc);  %#ok<ASGLU>
isMex = strcmpi(strrep(funcExt, '.', ''), mexext);

% Global Interface: ------------------------------------------------------------
% Do the work: =================================================================
backDir = cd;
disp(['==== Test GetFullPath  ', datestr(now, 0), ...
   char(10), '  Function: ', whichFunc]);

% Check a folder (trailing file separator):
% cd(tempdir);
% cd(fileparts(myFunc));
thisDir = cd;
disp(['  Current path: ', thisDir, char(10)]);

folder = ['Folder', FSep];
cf     = GetFullPath(folder);
if strcmpi(cf, fullfile(thisDir, folder, ''))
   disp(['  ok: ', thisDir, ', Folder: [', folder, ']']);
else
   disp(['Path: ', thisDir, ', Folder: [', folder, '] ==> error']);
   disp(['?!: ', cf]);
   error(ErrID, [FuncName, ': GetFullPath with folder failed']);
end

% Check a file:
file = 'File';
cf   = GetFullPath(file);
if strcmpi(cf, fullfile(thisDir, file))
   disp(['  ok: ', thisDir, ', File: ', file]);
else
   disp(['Path: ', thisDir, ', File: ', file, ' ==> error']);
   disp(['?!: ', cf]);
   error(ErrID, [FuncName, ': GetFullPath with file failed']);
end

% Separate current directory into cell:
fl       = Str2Cell_L(thisDir, FSep);
fl(2, :) = {FSep};
depth    = size(fl, 2);

testFolder = ['Folder', FSep];
testStr    = testFolder;
for i = depth:-1:2
   testStr = ['..', FSep, testStr];  %#ok<AGROW>
   try
      cf  = GetFullPath(testStr);
      xfl = fl(:, 1:i - 1);
      
      % Construct the reply by hand:
      cf2 = cat(2, xfl{:}, testFolder);
      if strcmpi(cf, cf2)
         disp(['  ok: ', testStr]);
      else
         fprintf(['Path: [%s]  ==> error\n', ...
            '  GetFullPath replied: [%s]\n', ...
            '  Expected:            [%s]\n'], testStr, cf, cf2);
         error([FuncName, ': GetFullPath with folder failed']);
      end
   catch
      if isempty(lasterr)
         error(ErrID, [FuncName, ': GetFullPath crashed?!']);
      else
         error(ErrID, lasterr);
      end
   end
end

testFile = 'File';
testStr  = testFile;
for i = depth:-1:2
   testStr = ['..', FSep, testStr];  %#ok<AGROW>
   try
      cf  = GetFullPath(testStr);
      xfl = fl(:, 1:i - 1);
      
      % Construct the reply by hand:
      cf2 = [cat(2, xfl{:}), testFile];
      if strcmpi(cf, cf2)
         disp(['  ok: ', testStr]);
      else
         fprintf(['Path: [%s]  ==> error\n', ...
            '  GetFullPath replied: [%s]\n', ...
            '  Expected:            [%s]\n'], testStr, cf, cf2);
         error(ErrID, [FuncName, ': GetFullPath with folder failed']);
      end
   catch
      if isempty(lasterr)
         error(ErrID, [FuncName, ': GetFullPath crashed?!']);
      else
         error(ErrID, lasterr);
      end
   end
end

testFolder = ['Folder', FSep];
testCore   = testFolder;
for i = depth:-1:2
   testCore = ['..', FSep, testCore];  %#ok<AGROW>
   testStr  = [thisDir, FSep, testCore];
   try
      cf  = GetFullPath(testStr);
      xfl = fl(:, 1:i - 1);
      
      % Construct the reply by hand:
      cf2 = [cat(2, xfl{:}), testFolder];
      if strcmpi(cf, cf2)
         disp(['  ok: ', testStr]);
      else
         fprintf(['Path: [%s]  ==> error\n', ...
            '  GetFullPath replied: [%s]\n', ...
            '  Expected:            [%s]\n'], testStr, cf, cf2);
         error([FuncName, ': GetFullPath with folder failed']);
      end
   catch
      if isempty(lasterr)
         error(ErrID, [FuncName, ': GetFullPath crashed?!']);
      else
         error(ErrID, lasterr);
      end
   end
end

testFile = 'File';
testCore = testFile;
for i = depth:-1:2
   testCore = ['..', FSep, testCore];  %#ok<AGROW>
   testStr  = [thisDir, FSep, testCore];
   try
      cf  = GetFullPath(testStr);
      xfl = fl(:, 1:i - 1);
      
      % Construct the reply by hand:
      cf2 = [cat(2, xfl{:}), testFile];
      if strcmpi(cf, cf2)
         disp(['  ok: ', testStr]);
      else
         fprintf(['Path: [%s]  ==> error\n', ...
            '  GetFullPath replied: [%s]\n', ...
            '  Expected:            [%s]\n'], testStr, cf, cf2);
         error([FuncName, ': GetFullPath with folder failed']);
      end
   catch
      if isempty(lasterr)
         error(ErrID, [FuncName, ': GetFullPath crashed?!']);
      else
         error(ErrID, lasterr);
      end
   end
end

testStr = thisDir;
for i = depth:-1:1
   testStr = [testStr, FSep, '..'];  %#ok<AGROW>
   try
      cf = GetFullPath(testStr);
      
      % Construct the reply by hand:
      cf2 = CleanReply(testStr);
      if strcmpi(cf, cf2)
         disp(['  ok: ', testStr]);
      else
         fprintf(['Path: [%s]  ==> error\n', ...
            '  GetFullPath replied: [%s]\n', ...
            '  Expected:            [%s]\n'], testStr, cf, cf2);
         error([FuncName, ': GetFullPath with folder failed']);
      end
   catch
      if isempty(lasterr)
         error(ErrID, [FuncName, ': GetFullPath crashed?!']);
      else
         error(ErrID, lasterr);
      end
   end
end

if strcmpi(GetFullPath('.'), cd)
   disp('  ok: .');
else
   error(ErrID, [FuncName, ': GetFullPath failed for "."']);
end

if strcmpi(GetFullPath(['.', FSep, '.']), cd)
   disp('  ok: .\.');
else
   error(ErrID, [FuncName, ': GetFullPath failed for ".\."']);
end

if strcmpi(GetFullPath(fullfile(thisDir, '.')), cd)
   disp('  ok: <cd>\.');
else
   error(ErrID, [FuncName, ': GetFullPath failed for "<cd>\."']);
end

longName = repmat('0123456789', 1, 20);
fullname = GetFullPath(fullfile(thisDir, longName, '..', longName, '..'));
if ispc && isMex
   want = fullfile('\\?\', thisDir);
else
   want = thisDir;
end
if strcmpi(fullname, want)
   if ispc
      disp('  ok: long input  (initial: \\?\)');
   else
      disp('  ok: long input');
   end
else
   error(ErrID, [FuncName, ': GetFullPath failed for long input']);
end

fullname = GetFullPath(fullfile(thisDir, longName, longName));
if ispc && isMex
   want = fullfile('\\?\', thisDir, longName, longName);
else
   want = fullfile(thisDir, longName, longName);
end
if strcmpi(fullname, want)
   if ispc
      disp('  ok: long input and output  (initial: \\?\)');
   else
      disp('  ok: long input and output');
   end
else
   error(ErrID, [FuncName, ': GetFullPath failed for long input and output']);
end

if ispc  % No UNC paths under Linux
   UNCPath = '\\Server\Folder';
   folder  = fullfile(UNCPath, 'SubFolder');
   if isequal(GetFullPath(folder), folder)
      disp(['  ok: ', folder]);
   else
      error(ErrID, [FuncName, ': GetFullPath failed for "%s"', folder]);
   end
   
   folder2 = fullfile(UNCPath, 'SubFolder', '.');
   if isequal(GetFullPath(folder2), folder)
      disp(['  ok: ', folder2]);
   else
      error(ErrID, [FuncName, ': GetFullPath failed for "%s"'], folder2);
   end
   
   folder2 = fullfile(UNCPath, 'SubFolder', '..');
   if isequal(GetFullPath(folder2), UNCPath)
      disp(['  ok: ', folder2]);
   else
      error(ErrID, [FuncName, ': GetFullPath failed for "%s"'], folder2);
   end
   
   folder2 = fullfile(UNCPath, 'SubFolder', 'Sub2', '..');
   if isequal(GetFullPath(folder2), folder)
      disp(['  ok: ', folder2]);
   else
      error(ErrID, [FuncName, ': GetFullPath failed for "%s"'], folder2);
   end
   
   folder2 = fullfile(UNCPath, 'SubFolder', 'Sub2', '..', '..');
   if isequal(GetFullPath(folder2), UNCPath)
      disp(['  ok: ', folder2]);
   else
      error(ErrID, [FuncName, ': GetFullPath failed for "%s"'], folder2);
   end
   
   folder2 = fullfile(UNCPath, 'SubFolder', 'Sub2', '..', '..', '..');
   if isequal(GetFullPath(folder2), UNCPath)
      disp(['  ok: ', folder2]);
   else
      error(ErrID, [FuncName, ': GetFullPath failed for "%s"'], folder2);
   end
end

% Cell string input: -----------------------------------------------------------
fullpath = GetFullPath({});
if isa(fullpath, 'cell') && isempty(fullpath)
   disp('  ok: {}');
else
   error(ErrID, [FuncName, ': GetFullPath failed for {}']);
end

fullpath = GetFullPath({''});
if isa(fullpath, 'cell') && length(fullpath) == 1 && strcmpi(fullpath, cd)
   disp('  ok: {''''}');
else
   error(ErrID, [FuncName, ': GetFullPath failed for {''''}']);
end

fullpath = GetFullPath(cell(1, 1));  % NULL pointer!
if isa(fullpath, 'cell') && length(fullpath) == 1 && strcmpi(fullpath, cd)
   disp('  ok: cell(1, 1)  uninitialized');
else
   error(ErrID, [FuncName, ': GetFullPath failed for: cell(1, 1)']);
end

fullpath = GetFullPath({'.'});
if isa(fullpath, 'cell') && length(fullpath) == 1 && strcmpi(fullpath, cd)
   disp('  ok: {''.''}');
else
   error(ErrID, [FuncName, ': GetFullPath failed for {''.''}']);
end

fullpath = GetFullPath({'', '.'});
if isa(fullpath, 'cell') && isequal(size(fullpath), [1,2]) ...
      && all(strcmpi(fullpath, cd))
   disp('  ok: {'''', ''.''}');
else
   error(ErrID, [FuncName, ': GetFullPath failed for {'''', ''.''}']);
end

fullpath = GetFullPath({'.', ''});
if isa(fullpath, 'cell') && isequal(size(fullpath), [1,2]) ...
      && all(strcmpi(fullpath, cd))
   disp('  ok: {''.'', ''''}');
else
   error(ErrID, [FuncName, ': GetFullPath failed for {''.'', ''''}']);
end

Base = 'D:\Temp\Folder';
list = GetFullPath({Base; ...
   fullfile(Base, 'Sub'); ...
   fullfile(Base, 'Sub', filesep); ...
   fullfile(Base, '.'); ...
   fullfile(Base, '..'); ...
   fullfile(Base, '..', 'Sub'); ...
   fullfile(Base, '..', '..'); ...
   fullfile(Base, '..', '..', '..')});
want = {'D:\Temp\Folder'; ...
   'D:\Temp\Folder\Sub'; ...
   'D:\Temp\Folder\Sub\'; ...
   'D:\Temp\Folder'; ...
   'D:\Temp'; ...
   'D:\Temp\Sub'; ...
   'D:\'; ...
   'D:\'};
if isunix
   want = strrep(want, '\', '/');
   want = strrep(want, 'D:', '');
   list = strrep(list, 'D:', '');
end

if isequal(list, want)
   disp('  ok: List of relative paths');
else
   error(ErrID, [FuncName, ': GetFullPath failed for list of relative paths']);
end

% ------------------------------------------------------------------------------
disp([char(10), 'GetFullPath passed the tests']);
cd(backDir);

% return;

% ******************************************************************************
function F = CleanReply(F)
% Remove \.. and \. from file hierarchy - not efficient!

C                 = Str2Cell_L(F, filesep);
C(strcmp(C, '.')) = [];
DDot              = find(strcmp(C, '..'));
while ~isempty(DDot)
   if DDot(1) == 2
      C(2) = [];
   else
      C(DDot(1) - [1, 0]) = [];
   end
   DDot = find(strcmp(C, '..'));
end
if length(C) > 1
   if F(length(F)) == filesep
      F = fullfile(C{:}, filesep);
   else
      F = fullfile(C{:});
   end
else
   F = [C{1}, filesep];
end

% return;

% ******************************************************************************
function CStr = Str2Cell_L(Str, Sep)
% Split string to cell string
% Use faster C-Mex for real problems.
%
% Author: Jan Simon, Heidelberg, (C) 2006-2011 matlab.THISYEAR(a)nMINUSsimon.de
% Was JRev: R0f V:043 Sum:S1il6b0rgftL Date:07-Sep-2009 02:12:29 $
% Was File: Tools\GLString\Str2Cell_L.m $

SepInd = strfind(Str, Sep);  % Find separators
if isempty(SepInd)
   CStr = {Str};
else
   % Append trailing separator on demand:
   StrLen  = length(Str);
   iSepInd = [1, SepInd + 1];
   if iSepInd(length(iSepInd)) > StrLen
      % Last iSepInd not used later
      fSepInd = SepInd - 1;
   else
      fSepInd = [SepInd - 1, StrLen];
   end
   nParts = length(fSepInd);
   
   % Copy each part into a cell element:
   CStr = cell(1, nParts);
   for iSep = 1:nParts
      CStr{iSep} = Str(iSepInd(iSep):fSepInd(iSep));
   end
end

% return;
