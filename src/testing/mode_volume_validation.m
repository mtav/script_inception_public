%  destdir = '/tmp/MV-ref-full'
% destdir = '/tmp/MV-ref-full-2'
destdir = '/tmp/MV-validation'

ret_list = {};

for func = 3:3
    for dir_idx = 1:3
        direction = ['x','y','z'](dir_idx);
        function_name = ['example_function_', num2str(func)];
        fulldir = fullfile(destdir, function_name, upper(direction))
        cd(fulldir);
        ret = calculateModeVolume({'sim.geo', 'sim.inp'}, 'snap_plane', direction, 'refractive_index_defect', 1/2);
        ret.simdir = fulldir;
        ret_list{end+1} = ret;
        createEnergySnapshot([direction, 'ax_id_00.prn'], '', true, 'nowarning', true);
    end
end

for idx = 1:length(ret_list)
    ret = ret_list{idx};
    disp([ret.simdir, ' -> V = ', num2str(ret.mode_volume_mum3), ' , Vn1 = ', num2str(ret.normalized_mode_volume_1), ' , Vn2 = ', num2str(ret.normalized_mode_volume_2)]);
end

cd(destdir);
