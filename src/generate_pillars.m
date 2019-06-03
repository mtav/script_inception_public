function generate_pillars(TOPDIR)

  mkdir(TOPDIR);
  copyfile(fullfile(getuserdir(),'MATLAB','Entity.lst'),TOPDIR);
  copyfile(fullfile(getuserdir(),'MATLAB','qedc3_2_05.sh'),TOPDIR);
  cd(TOPDIR);

  c0=299792458;%mum/mus
  lambda=900*10^-3;%mum

  SNAPSHOTS_ON = 0;
  FREQUENCY = c0/lambda;

  function gen_pillars(a_pillar_type, a_N_bottom, a_N_top)
    for r=1:0.5:5
      for n_type=0:1
      dirname = strcat('pillar_',a_pillar_type,'_',num2str(n_type),'_',num2str(10*r));
      dirname
      micropillar(r, dirname, 'qedc3_2_05', n_type, a_N_bottom, a_N_top, FREQUENCY, SNAPSHOTS_ON);
      end
    end
  end
  
  % ID bottom/top pairs
  % M3687 40/36 pairs
  % M2754 33/26 pairs

  pillar_type='M3687'
  N_bottom=40;
  N_top=36;
  gen_pillars(pillar_type, N_bottom, N_top);

  pillar_type='M2754';
  N_bottom=33;
  N_top=26;
  gen_pillars(pillar_type, N_bottom, N_top);

end
