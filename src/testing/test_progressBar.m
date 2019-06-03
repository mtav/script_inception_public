% different ways of displaying progress in Matlab/Octave
% Matlab's fprintf does not interpret \r correctly, but sprintf() helps work around that.
% waitbar() is an easy GUI solution, but problematic if no X available.
% cf:
%   https://uk.mathworks.com/matlabcentral/newsreader/view_thread/315518
%   http://stackoverflow.com/questions/17662965/how-to-print-carriage-return-in-matlab

% prints new lines everywhere
N=10;
for idx=0:N
  fprintf('%f%%\n', 100*idx/N);
  pause(0.1);
end

% works only in Octave
for idx=0:N
  fprintf('%f%%\r', 100*idx/N);
  pause(0.1);
end
fprintf('\n');

% works everywhere, but requires GUI
h=waitbar(0,'0%');
for idx=0:N
  waitbar(idx/N, h, sprintf('%f%%', 100*idx/N));
  pause(0.1);
end
close(h);

% works everywhere, prints all on same line
for idx=0:N
  nchar = fprintf('%f%%', 100*idx/N);
  pause(0.1);
  fprintf(repmat('\b', 1, nchar));
end
fprintf('\n');

% on GNU/Linux, prints on same line everywhere, but on Windows+Matlab, it prints new lines...
for idx=0:N
  fprintf('%f%%%s', 100*idx/N, sprintf('\r'));
  pause(0.1);
end
fprintf('\n');
