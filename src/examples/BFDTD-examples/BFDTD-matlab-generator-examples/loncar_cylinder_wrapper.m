function loncar_cylinder_wrapper(BASENAME, DSTDIR)
    %  ex: loncar_cylinder_wrapper('loncar_cylinder',getenv('DATADIR'))
    % function INFILENAME = loncar_cylinder(BASENAME, DSTDIR, ITERATIONS, PrintHolesTop, PrintHolesBottom, HOLE_TYPE, pillar_radius_mum, EXCITATION_FREQUENCY, SNAPSHOTS_FREQUENCY,ExcitationType)
    %  INFILENAME = loncar_cylinder('loncar_cylinder_1048400_4', getenv('DATADIR'), ITERATIONS, 1, 1, HOLE_TYPE, pillar_radius_mum, EXCITATION_FREQUENCY, SNAPSHOTS_FREQUENCY, ExcitationType);

    ITERATIONS = [10,32000,261600,300000,1048400];
    HOLE_TYPE = 1;
    pillar_radius_mum = 0.150/2.0;
    ExcitationType_list = [1,2,3,4];
    lambda = 0.637;%mum
    EXCITATION_FREQUENCY = get_c0()/lambda;

%      lambda_res = 634.7730*10^-3;%mum
%      SNAPSHOTS_FREQUENCY = [ get_c0()/lambda_res ];
    SNAPSHOTS_FREQUENCY = [];

    disp(['creating ',DSTDIR,filesep,BASENAME]);
    mkdir([DSTDIR,filesep,BASENAME]);
    for iterations_index=1:length(ITERATIONS)
      for excitation_index=1:length(ExcitationType_list)
        disp(['--------->iterations_index=',num2str(iterations_index)]);
        N = ITERATIONS(iterations_index);
        gen_loncar(N, true, true, BASENAME, DSTDIR, HOLE_TYPE, pillar_radius_mum, EXCITATION_FREQUENCY, SNAPSHOTS_FREQUENCY, ExcitationType_list(excitation_index));
        gen_loncar(N, false, true, BASENAME, DSTDIR, HOLE_TYPE, pillar_radius_mum, EXCITATION_FREQUENCY, SNAPSHOTS_FREQUENCY, ExcitationType_list(excitation_index));
        gen_loncar(N, true, false, BASENAME, DSTDIR, HOLE_TYPE, pillar_radius_mum, EXCITATION_FREQUENCY, SNAPSHOTS_FREQUENCY, ExcitationType_list(excitation_index));
        gen_loncar(N, false, false, BASENAME, DSTDIR, HOLE_TYPE, pillar_radius_mum, EXCITATION_FREQUENCY, SNAPSHOTS_FREQUENCY, ExcitationType_list(excitation_index));
      end
    end
end

function gen_loncar(N, PrintHolesTop, PrintHolesBottom, BASENAME, DSTDIR, HOLE_TYPE, pillar_radius_mum, EXCITATION_FREQUENCY, SNAPSHOTS_FREQUENCY, ExcitationType)
    filename = [ BASENAME, '.N_', num2str(N), '.PrintHolesTop_', num2str(PrintHolesTop), '.PrintHolesBottom_', num2str(PrintHolesBottom), '.ExcitationType_', num2str(ExcitationType) ];
    INFILENAME = loncar_cylinder(filename, [DSTDIR,filesep,BASENAME], N, PrintHolesTop, PrintHolesBottom, HOLE_TYPE, pillar_radius_mum, EXCITATION_FREQUENCY, SNAPSHOTS_FREQUENCY, ExcitationType);
    disp(['-->created ',INFILENAME]);
end
