function disp_and_log(logfile_fid_list, STR, varargin)
  % function disp_and_log(logfile_fid_list, STR, varargin)
  %
  % Simple function to display and log information at the same time.
  % It can however also output to any number of files, with or without stdout output.
  %
  % logfile_fid_list can be a single FID of an open file or an FID list.
  %
  % -If only one FID is given, it outputs to stdout and the given FID.
  % -Else, it outputs to every FID>0.
  %
  % STR and varargin are passed to fprintf calls, with a linebreak added automatically at the end.
  %
  % Basic usage:
  %   disp_and_log(fid, 'hello world');
  %   disp_and_log(fid, 'N = %.2f', N);
  %
  % Advanced usage:
  %   disp_and_log(fid, 'hello world'); % output to stdout and file
  %   disp_and_log([-1, fid], 'hello world'); % output to file only
  %   disp_and_log([-1, 1], 'hello world'); % output to stdout only
  %   disp_and_log([fid1, fid2], 'hello world'); % output to two files
  %
  % TODO: Add warning + error options?

  if length(logfile_fid_list) == 1
    fprintf(1, [STR, '\n'], varargin{:});
  end
  
  for logfile_fid = logfile_fid_list
    if logfile_fid >= 0
      fprintf(logfile_fid, [STR, '\n'], varargin{:});
    end
  end
end
