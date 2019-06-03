close all;
clear all;

for eps1 = [13, 12, 1]
  BASENAME = sprintf('DBR-stack_%d-13', eps1);
  cmd = sprintf('mpb eps1=%d eps2=13 DBR-stack.ctl | tee %s', eps1, [BASENAME, '.out']);
  system(cmd);
  cmd = sprintf('postprocess_mpb.sh %s', [BASENAME, '.out']);
  system(cmd);
  plotDBR([BASENAME, '.out.dat']);
end

system('./DBR_stack.sh');
