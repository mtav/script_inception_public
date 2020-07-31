% Run "bash DBR_stack.sh" in a GNU/Linux shell first, before using this script.
close all;
clear all;

cd(dirname(which('DBR_stack')));
pwd();

for eps1 = 1:13
  BASENAME = sprintf('DBR-stack_%d-13', eps1);
%   cmd = sprintf('mpb eps1=%d eps2=13 DBR-stack.ctl | tee %s', eps1, [BASENAME, '.out']);
%   system(cmd);
%   cmd = sprintf('postprocess_mpb.sh %s', [BASENAME, '.out']);
%   system(cmd);
  plotDBR([BASENAME, '.out.dat'], eps1);
end

% system('./DBR_stack.sh');
