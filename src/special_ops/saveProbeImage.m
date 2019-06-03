function saveProbeImage(DIR)
  DIR
  cd(DIR);
  close all;
  [ folder, basename, ext ] = fileparts(DIR);
  plotProbe('p001id.prn',3,0,['~/Labortablo/Qplot/',basename, ext,'.png']);
end

