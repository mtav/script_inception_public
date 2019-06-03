function prepare(defect_size_vector)

  refractive_index_log = [];
  refractive_index_outer = [];
  vertical_period = [];
  w_factor = [];

  % TODO: Read those values from an input file
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%% prepare2.m

  refractive_index_log = [refractive_index_log, 3.3];
  refractive_index_outer = [refractive_index_outer, 1];
  vertical_period = [vertical_period, 0.34192];
  w_factor = [w_factor, 0.214568344294694];

  refractive_index_log = [refractive_index_log, 1.52];
  refractive_index_outer = [refractive_index_outer, 3.3];
  vertical_period = [vertical_period, 0.2759];
  w_factor = [w_factor, 0.436120944956286];

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%% prepare.m
  refractive_index_log = [refractive_index_log, 1.52];
  refractive_index_outer = [refractive_index_outer, 1];
  vertical_period = [vertical_period, 0.54474];
  w_factor = [w_factor, 0.310436763212442];

  refractive_index_log = [refractive_index_log, 2.1];
  refractive_index_outer = [refractive_index_outer, 1];
  vertical_period = [vertical_period, 0.46098];
  w_factor = [w_factor, 0.26785111938991];

  refractive_index_log = [refractive_index_log, 2.4];
  refractive_index_outer = [refractive_index_outer, 1];
  vertical_period = [vertical_period, 0.42551];
  w_factor = [w_factor, 0.263449966224216];

  refractive_index_log = [refractive_index_log, 3.3];
  refractive_index_outer = [refractive_index_outer, 1];
  vertical_period = [vertical_period, 0.34192];
  w_factor = [w_factor, 0.214568344294694];

  refractive_index_log = [refractive_index_log, 3.5];
  refractive_index_outer = [refractive_index_outer, 1];
  vertical_period = [vertical_period, 0.32695];
  w_factor = [w_factor, 0.214589803375032];

  refractive_index_log = [refractive_index_log, 3.3];
  refractive_index_outer = [refractive_index_outer, 1.52];
  vertical_period = [vertical_period, 0.2756];
  w_factor = [w_factor, 0.267240757145721];

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  refractive_index_log = [refractive_index_log, 1.52];
  refractive_index_outer = [refractive_index_outer, 1];
  vertical_period = [vertical_period, 0.54474];
  w_factor = [w_factor, 0.2];

  refractive_index_log = [refractive_index_log, 2.1];
  refractive_index_outer = [refractive_index_outer, 1];
  vertical_period = [vertical_period, 0.46098];
  w_factor = [w_factor, 0.2];

  refractive_index_log = [refractive_index_log, 2.4];
  refractive_index_outer = [refractive_index_outer, 1];
  vertical_period = [vertical_period, 0.42551];
  w_factor = [w_factor, 0.2];

  refractive_index_log = [refractive_index_log, 3.3];
  refractive_index_outer = [refractive_index_outer, 1];
  vertical_period = [vertical_period, 0.34192];
  w_factor = [w_factor, 0.2];

  refractive_index_log = [refractive_index_log, 3.5];
  refractive_index_outer = [refractive_index_outer, 1];
  vertical_period = [vertical_period, 0.32695];
  w_factor = [w_factor, 0.2];

  refractive_index_log = [refractive_index_log, 3.3];
  refractive_index_outer = [refractive_index_outer, 1.52];
  vertical_period = [vertical_period, 0.2756];
  w_factor = [w_factor, 0.2];
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  excitation_direction_string = {'Ex','Ey','Ez'};
  %defect_size_vector = {[3,1,1],[1,3,1],[1,1,3]};

  for i = 1:length(refractive_index_log)
    %for defect_size_vector = [[3,1,1],[1,3,1],[1,1,3]]
      for excitation_direction = [0,1,2]
      %for excitation_direction = [0,1]
        %BASE =['nlog_', num2str(), '.nout_', num2str((i)), '.a_', num2str((i)), '.w_', num2str((i))];
        BASE = sprintf('nlog_%.2f.nout_%.2f.a_%.2f.w_%.2f', [refractive_index_log(i),refractive_index_outer(i),vertical_period(i),w_factor(i)]);
        directory = [ BASE, filesep, excitation_direction_string{excitation_direction+1}, filesep ];
        if ~isdir(BASE); mkdir(BASE); end;
        if ~isdir(directory); mkdir(directory); end;
        %disp([' refractive_index_log = ', num2str(refractive_index_log(i)), ' vertical_period = ', num2str(vertical_period(i)), ' w_factor = ', num2str(w_factor(i)),' excitation_direction = ', num2str(excitation_direction), ' directory = ', directory ]);
        disp([' directory = ', directory ]);
        inp10a(vertical_period(i), excitation_direction, directory, w_factor(i))
        Woodpile_geo(vertical_period(i), refractive_index_log(i), refractive_index_outer(i), directory, w_factor(i), vertical_period(i)/sqrt(2)*defect_size_vector)
        
        copyfile([dirname(mfilename('fullpath')), filesep, 'sim.in'], directory)
        copyfile([dirname(mfilename('fullpath')), filesep, 'sim.sh'], directory)
      end
    %end
  end

end
