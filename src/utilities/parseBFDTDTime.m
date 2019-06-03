% Parses time.txt file created by Bristol FDTD and returns the corresponding number of iterations.
% Other return elements not implemented yet. (TODO)
function [number_of_iterations, starttime, endtime, totaltime, time_list, iteration_list] = parseBFDTDTime(time_file)
  number_of_iterations = 0;
  starttime = 0;
  endtime = 0;
  totaltime = 0;
  time_list = 0;
  iteration_list = 0;
  
  % does not work as is for octave < v3.4.0
  fid = fopen(time_file, 'r');
  % read first line
  A = textscan(fid,'%s %s %d:%d:%d',1);
  % read remaining lines
  B = textscan(fid,'%d %s %d:%d:%d');
  fclose(fid);
  
  %if ~inoctave()
    %fid = fopen(time_file, 'r');
    %% read first line
    %A = textscan(fid,'%s %s %d:%d:%d',1);
    %% read remaining lines
    %B = textscan(fid,'%d %s %d:%d:%d');
    %fclose(fid);
  %else
    %A = textread(time_file,'%s %s %d:%d:%d',1);
    %% read remaining lines
    %B = textread(time_file,'%d %s %d:%d:%d');
  %end
  number_of_iterations = B{1}(end);
end
