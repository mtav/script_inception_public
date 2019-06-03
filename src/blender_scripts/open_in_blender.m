function [status,result] = open_in_blender(FILE)
    if ispc
      [status,result] = system(['"C:\Program Files\Blender Foundation\Blender\blender" -P "',getenv('USERPROFILE'),'\Application Data\Blender Foundation\Blender\.blender\scripts\bfdtd_import.py" -- "',FILE,'"'])
    else
      [status,result] = system(['xterm -e blender -P $HOME/.blender/scripts/bfdtd_import.py -- ',FILE])
    end
end
