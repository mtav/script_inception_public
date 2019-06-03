function thesis_createEnergySnapshots_function(fx, ex, fy, ey, fz, ez)
  sprintf('%s %s %s %s %s %s', fx, ex, fy, ey, fz, ez)
  
  %sprintf('createEnergySnapshot(''%s'', ''%s'', true)', [fx,'.prn'], [ex,'.prn'])
  
  createEnergySnapshot([fx,'.prn'], [ex,'.prn'], true);
  createEnergySnapshot([fy,'.prn'], [ey,'.prn'], true);
  createEnergySnapshot([fz,'.prn'], [ez,'.prn'], true);
end
