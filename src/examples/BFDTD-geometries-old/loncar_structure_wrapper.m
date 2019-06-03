function loncar_structure_wrapper(BASENAME, DSTDIR)
  %  ex: loncar_structure_wrapper('loncar_resonance',getenv('DATADIR'))

  ITERATIONS = [10,32000,261600,300000];
  HOLE_TYPE = 3;
  pillar_radius = 1;
  
  lambda = 637*10^-3;%mum
  EXCITATION_FREQUENCY = get_c0()/lambda;

  lambda_res = 634.7730*10^-3;%mum

  SNAPSHOTS_FREQUENCY = [ get_c0()/lambda_res ];
  
  disp(['creating ',DSTDIR,filesep,BASENAME]);
  mkdir([DSTDIR,filesep,BASENAME]);
  %      disp('...done');
  %      disp('...done1');
  
  %      disp('...done2');
  for iter_index=1:length(ITERATIONS)
  disp(['--------->iter_index=',num2str(iter_index)]);
    N = ITERATIONS(iter_index);
    gen_loncar(N, true, true, BASENAME, DSTDIR, HOLE_TYPE, pillar_radius, EXCITATION_FREQUENCY, SNAPSHOTS_FREQUENCY);
    gen_loncar(N, false, true, BASENAME, DSTDIR, HOLE_TYPE, pillar_radius, EXCITATION_FREQUENCY, SNAPSHOTS_FREQUENCY);
    gen_loncar(N, true, false, BASENAME, DSTDIR, HOLE_TYPE, pillar_radius, EXCITATION_FREQUENCY, SNAPSHOTS_FREQUENCY);
    gen_loncar(N, false, false, BASENAME, DSTDIR, HOLE_TYPE, pillar_radius, EXCITATION_FREQUENCY, SNAPSHOTS_FREQUENCY);
  end
  %      disp('...done3');
end

function gen_loncar(N, print_holes_top, print_holes_bottom, BASENAME, DSTDIR, HOLE_TYPE, pillar_radius, EXCITATION_FREQUENCY, SNAPSHOTS_FREQUENCY)
  % for excitation_direction=1:12
  filename = [ BASENAME, '_', num2str(N), '_', num2str(print_holes_top), '_', num2str(print_holes_bottom) ];
  loncar_structure(filename, [DSTDIR,filesep,BASENAME], N, print_holes_top, print_holes_bottom, HOLE_TYPE, pillar_radius, EXCITATION_FREQUENCY, SNAPSHOTS_FREQUENCY);
  % BASENAME, DSTDIR, ITERATIONS, print_holes_top, print_holes_bottom, HOLE_TYPE, pillar_radius, EXCITATION_FREQUENCY, SNAPSHOTS_FREQUENCY
  % end
end
