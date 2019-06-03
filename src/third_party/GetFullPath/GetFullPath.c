// GetFullPath.c
// Get absolute path of a file or folder [WINDOWS]
// FullName = GetFullPath(Name)
// INPUT:
//   Name: String or cell string, file or folder name with or without relative
//         or absolute path.
//         Unicode characters and UNC paths are supported.
//         Up to 8192 characters are allowed here, but some functions of the
//         operating system may support 260 characters only.
//
// OUTPUT:
//   FullName: String or cell string, file or folder name with absolute path.
//         "\." and "\.." are processed such that FullName is fully qualified.
//         For empty strings the current directory is replied.
//         The created path need not exist.
//
// NOTE: The Mex function calls the Windows-API, therefore does not run on
//   MacOS and Linux.
//   The magic initial key '\\?\' is inserted on demand to support names
//   exceeding MAX_PATH characters as defined by the operating system.
//
// EXAMPLES:
//   cd(tempdir);                    % Here assumed as C:\Temp
//   GetFullPath('File.Ext')         % ==>  'C:\Temp\File.Ext'
//   GetFullPath('..\File.Ext')      % ==>  'C:\File.Ext'
//   GetFullPath('..\..\File.Ext')   % ==>  'C:\File.Ext'
//   GetFullPath('.\File.Ext')       % ==>  'C:\Temp\File.Ext'
//   GetFullPath('*.txt')            % ==>  'C:\Temp\*.txt'
//   GetFullPath('..')               % ==>  'C:\'
//   GetFullPath('Folder\')          % ==>  'C:\Temp\Folder\'
//   GetFullPath('D:\A\..\B')        % ==>  'D:\B'
//   GetFullPath('\\Server\Folder\Sub\..\File.ext')
//                                   % ==>  '\\Server\Folder\File.ext'
//   GetFullPath({'..', 'new'})      % ==>  {'C:\', 'C:\Temp\new'}
//
// COMPILE:
//   mex -O GetFullPath.c
//   Linux: mex -O CFLAGS="\$CFLAGS -std=c99" GetFullPath.c
//   Pre-compiled: http://www.n-simon.de/mex
//   Run the unit-test uTest_GetFullPath after compiling.
//
// Tested: Matlab 6.5, 7.7, 7.8, 7.13, WinXP/32, Win7/64
//         Compiler: LCC2.4/3.8, BCC5.5, OWC1.8, MSVC2008/2010
// Assumed Compatibility: higher Matlab versions
// Author: Jan Simon, Heidelberg, (C) 2009-2011 matlab.THISYEAR(a)nMINUSsimon.de
//
// See also: Rel2AbsPath, CD, FULLFILE, FILEPARTS.

/*
% $JRev: R-o V:014 Sum:4OqQxEPM3Kmd Date:05-Oct-2011 23:51:19 $
% $License: BSD (use/copy/change/redistribute on own risk, mention the author) $
% $UnitTest: uTest_GetFullPath $
% $File: Tools\Mex\Source\GetFullPath.c $
% History:
% 001: 19-Apr-2010 01:23, Successor of Rel2AbsPath.
%      No check of validity or existence in opposite to Rel2AbsPath.
% 011: 24-Jan-2011 11:38, Cell string as input.
% 013: 27-Apr-2011 10:29, Minor bug: Bad ID for error messages.
*/

#if defined(__WINDOWS__) || defined(WIN32) || defined(_WIN32) || defined(_WIN64)
#include <windows.h>
#else
#error Sorry: Implemented for Windows only now!
#endif

#include "mex.h"
#include <wchar.h>

// Assume 32 bit addressing for Matlab 6.5:
// See MEX option "compatibleArrayDims" for MEX in Matlab >= 7.7.
#ifndef MWSIZE_MAX
#define mwSize  int32_T           // Defined in tmwtypes.h
#define mwIndex int32_T
#define MWSIZE_MAX MAX_int32_T
#endif

// Error messages do not contain the function name in Matlab 6.5! This is not
// necessary in Matlab 7, but it does not bother:
#define ERR_HEAD "*** GetFullPath: "
#define ERR_ID   "JSimon:GetFullPath:"

// Static buffer and magic key to turn off path parsing:
wchar_t Buffer[MAX_PATH + 1],
        *MagicKey = L"\\\\?\\UNC";

// Do not accept ridiculous long file names:
#define MAXFILELEN_INPUT 8191L

// Prototypes:
mxArray *Core(mxChar *Name_m, mwSize NameLen);

// Main function ===============================================================
void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[])
{
  const mxArray *In, *String;
  mxArray *Out;
  mwSize  iC;
  
  // Check number of inputs and outputs:
  if (nrhs != 1 || nlhs > 1) {
     mexErrMsgIdAndTxt(ERR_ID   "BadNInput",
                       ERR_HEAD "1 input required, 1 output allowed.");
  }
  
  // Get input string or cell string: ------------------------------------------
  In = prhs[0];
  if (mxIsChar(In)) {
     plhs[0] = Core((mxChar *) mxGetData(In), mxGetNumberOfElements(prhs[0]));
     
  } else if (mxIsCell(In)) {
     plhs[0] = mxCreateCellArray(mxGetNumberOfDimensions(In),
                                 mxGetDimensions(In));
     Out = plhs[0];
     iC  = mxGetNumberOfElements(In);
     while (iC-- > 0) {                        // Backwards (faster than FOR)
        String = mxGetCell(In, iC);
        if (String == NULL) {                  // Uninitialized cell:
           mxSetCell(Out, iC, Core(NULL, 0));  // Reply current directory
        } else if (mxIsChar(String)) {
           mxSetCell(Out, iC,
                     Core((mxChar *) mxGetData(String),
                          mxGetNumberOfElements(String)));
        } else {
           mexErrMsgIdAndTxt(ERR_ID   "BadInputType",
                        ERR_HEAD "[FileName] must be a string or cell string.");
        }
     }
     
  } else {
     mexErrMsgIdAndTxt(ERR_ID   "BadInputType",
                       ERR_HEAD "[FileName] must be a string or cell string.");
  }
  
  return;
}

// =============================================================================
mxArray *Core(mxChar *Name_m, mwSize NameLen)
{
  wchar_t *Name_w, *Full_w;
  bool    freeName, freeFull;
  mwSize  FullLen, Offset, KeyLen, dims[2] = {1L, 0L};
  mxArray *Full_m;
  
  if (NameLen == 0) {          // Empty input => CD: ---------------------------
     Name_w   = L".";
     freeName = false;
     
  } else if (NameLen <= MAXFILELEN_INPUT) {
     // Copy string to Unicode string with a terminator:
     freeName = true;
     if ((Name_w = (wchar_t *) mxMalloc((NameLen + 1) * sizeof(wchar_t)))
         == NULL) {
        mexErrMsgIdAndTxt(ERR_ID   "NoMemory",
                          ERR_HEAD "No memory for FileName.");
     }
     memcpy(Name_w, Name_m, NameLen * sizeof(wchar_t));
     Name_w[NameLen] = L'\0';
  
  } else {                     // Ridiculous input: ----------------------------
     mexErrMsgIdAndTxt(ERR_ID   "BadInputSize",
                       ERR_HEAD "FileName is too long.");
  }
  
  // Call Windows API to get the full path: ------------------------------------
  FullLen = GetFullPathNameW(
                      (LPCWSTR) Name_w,    // address of file name
                      MAX_PATH,            // buffer length
                      (LPWSTR) Buffer,     // address of path buffer
                      NULL);               // address of filename in path
  
  if (FullLen == 0) {                      // GetFullPathName failed:
     mexErrMsgIdAndTxt(ERR_ID   "GetFullName_Failed_Static",
                       ERR_HEAD "GetFullPathName failed.");
                       
  } else if (FullLen <= MAX_PATH) {        // Full name matched in static buffer:
     Full_w   = Buffer;
     freeFull = false;
    
  } else {     // Static buffer was too small - create a dynamic buffer instead:
     // Maximal 8 additional characters: "\\?\UNC" and terminator:
     freeFull = true;
     Full_w   = (wchar_t *) mxCalloc(FullLen + 8, sizeof(wchar_t));
     if (Full_w == NULL) {
        mexErrMsgIdAndTxt(ERR_ID   "NoMemory",
                          ERR_HEAD "No memory for dynamic buffer.");
     }
     
     // If Name starts with "\\" it is a UNC path:
     KeyLen = 4;
     Offset = 4;
     if (FullLen >= 2) {
        if (memcmp(Name_w, MagicKey, 2 * sizeof(wchar_t)) == 0) {
           KeyLen = 7;
           Offset = 6;
        }
     }
     
     // Call Windows API again to get the full path:
     FullLen = GetFullPathNameW(
                      (LPCWSTR) Name_w,     // address of file name
                      FullLen,              // buffer length
                      Full_w + Offset,      // address of path buffer
                      NULL);                // address of filename in path
     
     if (FullLen == 0) {                    // GetFullPathName failed:
        mexErrMsgIdAndTxt(ERR_ID   "GetFullName_Failed_Dynamic",
                          ERR_HEAD "GetFullPathName failed.");
     }
     
     // Either insert leading key "\\?\" or "\\?\UNC":
     FullLen += Offset;
     memcpy(Full_w, MagicKey, KeyLen * sizeof(wchar_t));
  }
  
  // Create output: ------------------------------------------------------------
  dims[1] = FullLen;
  Full_m  = mxCreateCharArray(2, dims);
  memcpy(mxGetData(Full_m), Full_w, FullLen * sizeof(mxChar));
  
  // Cleanup: ------------------------------------------------------------------
  if (freeName) {
     mxFree(Name_w);
  }
  if (freeFull) {
     mxFree(Full_w);
  }
  
  return Full_m;
}
