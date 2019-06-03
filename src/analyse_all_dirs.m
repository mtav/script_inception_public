function analyse_all_dirs(SRCDIR, DSTDIR)

  % runs create_harminv_input_files on all subdirs of SRCDIR and puts the output into DSTDIR
  
  if exist('SRCDIR','var')==0
    disp('SRCDIR not given');
      SRCDIR = uigetdir(getuserdir(),'SRCDIR');
  end
  if ~(exist(SRCDIR,'dir'))
    disp('dir not found');
    return;
  end

  if exist('DSTDIR','var')==0
    disp('DSTDIR not given');
      DSTDIR = uigetdir(getuserdir(),'DSTDIR');
  end
  if ~(exist(DSTDIR,'dir'))
    disp('dir not found');
    return;
  end
  
  cd(SRCDIR)
  DIRS = dir('pillar_*');
  for i=1:length(DIRS)
    if DIRS(i).isdir
      disp([DIRS(i).name,' is a directory'])
      close all;
      fprintf('===>Processing %s\n',DIRS(i).name);
      mkdir([DSTDIR,filesep,DIRS(i).name]);
      create_harminv_input_files([SRCDIR,filesep,DIRS(i).name], [DSTDIR,filesep,DIRS(i).name]);
      copyfile([SRCDIR,filesep,DIRS(i).name,filesep,'p89id_Ex_FFT_zoom1.png'],[getuserdir(),filesep,'comparepeaks',filesep,DIRS(i).name,'_p89id_Ex_FFT_zoom1.png']);
    else
      disp([DIRS(i).name,' is NOT a directory'])
    end
  end

  close all;
end
