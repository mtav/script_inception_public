% test automatic extraction of last snaptime number

TESTDIR = '~/TEST/snapshot_counting/';

cd(TESTDIR);

N = [10,10,0];

common = sort(randi(100,1,3)-1);

for m = 1:3
  subdir = sprintf('part_%d', m);
  delname = fullfile(TESTDIR, subdir, '*.prn');
  delete(delname);
  snap_time_number_list = randi(100, N(m), 1)-1;
  for numID = 1:N(m)
    for sub_idx = 1:randi(10)
      name = numID_to_alphaID_FrequencySnapshot(numID, 'snap_plane', 'x', 'snap_time_number', randi(10)-1);
      fullname = fullfile(TESTDIR, subdir, name);
      disp(fullname);
      fid = fopen(fullname, 'w');
      fclose(fid);
    end
    for sub_idx = 1:numel(common)
      name = numID_to_alphaID_FrequencySnapshot(numID, 'snap_plane', 'x', 'snap_time_number', common(sub_idx));
      fullname = fullfile(TESTDIR, subdir, name);
      disp(fullname);
      fid = fopen(fullname, 'w');
      fclose(fid);
    end
  end
end

cd(TESTDIR);
inpfile_list = {'./part_1/sim.inp', './part_2/sim.inp', './part_3/sim.inp'};

[snap_time_number_fsnap, snap_time_number_fsnap_info] = getLastSnapTimeNumberOverall(inpfile_list);
snap_time_number_fsnap_info.inpfile_list{1}.snap_time_number_common
snap_time_number_fsnap_info.inpfile_list{2}.snap_time_number_common
snap_time_number_fsnap_info.inpfile_list{3}.snap_time_number_common
snap_time_number_fsnap_info.snap_time_number_common
common
snap_time_number_fsnap
