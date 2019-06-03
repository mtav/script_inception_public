function ret = transmission(WORKDIR)
  cd(WORKDIR);
%    cmd = sprintf('../transmission.sh %s', WORKDIR)
  cmd = '../transmission.sh .';
  system(cmd);
  plotNormalizedTRLvalues('reference_file.dat', 'geometry_file.dat', false);
end
