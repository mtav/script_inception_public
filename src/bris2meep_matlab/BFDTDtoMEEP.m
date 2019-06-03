function [entries, FDTDobj] = BFDTDtoMEEP(file_list)
  %% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % Written by Erman Engin, University of Bristol
  % 
  % NOTES:
  % The code might give errors if INP file has other sources than a Gaussian pulse
  % Only one field in the excitation component defined in INP should be one.
  % That is either Ex or Ey ... Hx...etc;  Otherwise the first nonzero
  % component will be translated to ctl.
  %
  % ex:
  % BFDTDtoMEEP({'qedc3_2_05.geo','qedc3_2_05.inp'})
  %% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
  % if exist('geofile','var') == 0
    % disp('geofile not given');
    % [GeoFileName,GeoPathName] = uigetfile('*.geo','Select GEO file',getuserdir());
    % geofile=[GeoPathName,GeoFileName];
  % end

  % if exist(geofile,'file') ~= 2
    % error(['file ', geofile, ' not found or not a file']);
    % return;
  % end

    % if exist('inpfile','var') == 0
    % disp('inpfile not given');
    % [InpFileName,InpPathName] = uigetfile('*.inp','Select INP file',GeoPathName);
    % inpfile=[InpPathName,InpFileName];
  % end

  % if exist(inpfile,'file') ~= 2
    % error(['file ', inpfile, ' not found or not a file']);
    % return;
  % end

    % file_list(1)
    % file_list{1}
    % file_list[1]
  [GeoPathName, GeoFileName_basename, ext] = fileparts(file_list{1});
  if isempty(GeoPathName)
    GeoPathName = '.';
  end
  
  GeoFileName = [GeoFileName_basename, ext];
      
  % [entries]=GEO_INP_reader({geofile});
  [entries, FDTDobj] = GEO_INP_reader(file_list);

  projectPath = [GeoPathName, filesep, 'ctlConversion'];
  if ~exist(projectPath, 'dir')
    mkdir(projectPath);
  end
  filename = [projectPath, filesep, GeoFileName_basename, '.ctl'];
  disp(['Saving as ',filename]);
  FILE = fopen(filename, 'w+');

  %% GEO FILE%
  % for m=1:length(entries)
    % if strcmp(lower(entries{m}.type),'box')
      % data=entries{m}.data;
      % xl=data(1);
      % yl=data(2);
      % zl=data(3);
      % xu=data(4);
      % yu=data(5);
      % zu=data(6);
    % end
  % end
    
  % [xl, yl, zl] = FDTDobj.box.lower(:)';
  % [xu, yu, zu] = FDTDobj.box.upper(:)';

  simSize = FDTDobj.box.upper - FDTDobj.box.lower;
  geoCenter = simSize(:)./2.0;

  xmesh = FDTDobj.xmesh; if ~length(xmesh); xmesh=-1; end
  ymesh = FDTDobj.ymesh; if ~length(ymesh); ymesh=-1; end
  zmesh = FDTDobj.zmesh; if ~length(zmesh); zmesh=-1; end

  dxyz = min([min(xmesh),min(ymesh),min(zmesh)]);
  resolution = 1/dxyz;

  numSteps = FDTDobj.flag.numSteps;
    
  MEEP_settings(FILE, resolution, simSize);

  %%%%%%%%%%%%%%%%%%%
  fprintf(FILE,';geometry specification\r\n(set! geometry\r\n\t(list\r\n');
  % fprintf(FILE, '\r\n');

  for m = 1:length(FDTDobj.geometry_object_list)
    type = FDTDobj.geometry_object_list{m}.type;
    
    switch lower(type)
      case 'block'
        meep_lower = FDTDobj.geometry_object_list{m}.lower(:) - geoCenter(:);
        meep_upper = FDTDobj.geometry_object_list{m}.upper(:) - geoCenter(:);
        block_size = meep_upper(:) - meep_lower(:);
        meep_centro = 0.5*(meep_lower(:) + meep_upper(:));

        %xl = meep_lower(1); yl = meep_lower(2); zl = meep_lower(3);
        %xu = meep_upper(1); yu = meep_upper(2); zu = meep_upper(3);
        %w = block_size(1);
        %h = block_size(2);
        %d = block_size(3);

        % if (axis==1) { *c=((b->p2.x-b->p1.x)/2)+b->p1.x; }
        % if (axis==2) { *c=((b->p2.y-b->p1.y)/2)+b->p1.y; }
        % if (axis==3) { *c=((b->p2.z-b->p1.z)/2)+b->p1.z; }

        % centre_[0]=centre_[0]-(w/2);
        % centre_[1]=-1*(centre_[1]-(h/2));
        % centre_[2]=centre_[2]-(d/2);

        eps = FDTDobj.geometry_object_list{m}.permittivity;
        text = meepBlock(meep_centro, block_size, eps);
        fprintf(FILE, text);
      case 'cylinder'
        meep_centro = FDTDobj.geometry_object_list{m}.center(:) - geoCenter(:);
        ri = FDTDobj.geometry_object_list{m}.inner_radius;
        ro = FDTDobj.geometry_object_list{m}.outer_radius;
        h = FDTDobj.geometry_object_list{m}.height;
        
        eps = FDTDobj.geometry_object_list{m}.permittivity;
        text = meepCylinder(meep_centro, ro, h, [0 1 0], eps);
        fprintf(FILE, text);
      case 'sphere'
        meep_centro = FDTDobj.geometry_object_list{m}.center(:) - geoCenter(:);
        ri = FDTDobj.geometry_object_list{m}.inner_radius;
        ro = FDTDobj.geometry_object_list{m}.outer_radius;
        
        eps = FDTDobj.geometry_object_list{m}.permittivity;
        text = meepSphere(meep_centro, ro, eps);
        fprintf(FILE, text);
    end
  end
    
  fprintf(FILE,'\t)\r\n)\r\n\r\n');
    
    %%%%%%%%%%%%%%%%%%%    
  % Excitations
  fields={'Ex','Ey','Ez','Hx','Hy','Hz'};
  for m=1:length(FDTDobj.excitations)
    entry=FDTDobj.excitations(m);
    excFrequency=entry.frequency/get_c0();
    excComponent=fields{find([entry.E,entry.H]==1)};
    excSize=abs(entry.P1-entry.P2);
    excCenter=(entry.P1+entry.P2)/2-geoCenter';
    excWidth=entry.time_constant*get_c0();
    MEEP_excitation(FILE, excFrequency, excWidth, excComponent, excCenter, excSize);
  end

  %%%%%%%%%%%%%%%%%%%%%%
  % PML Layers
  pmlThickness=0.3;
  fprintf(FILE,';boundaries specification\r\n(set! pml-layers\r\n(list\r\n');

  fprintf(FILE,['(make pml (direction X) (side Low) (thickness ',num2str(pmlThickness,'%2.6f'),'))\r\n']);
  fprintf(FILE,['(make pml (direction Y) (side Low) (thickness ',num2str(pmlThickness,'%2.6f'),'))\r\n']);
  fprintf(FILE,['(make pml (direction Z) (side Low) (thickness ',num2str(pmlThickness,'%2.6f'),'))\r\n']);
  fprintf(FILE,['(make pml (direction X) (side High) (thickness ',num2str(pmlThickness,'%2.6f'),'))\r\n']);
  fprintf(FILE,['(make pml (direction Y) (side High) (thickness ',num2str(pmlThickness,'%2.6f'),'))\r\n']);
  fprintf(FILE,['(make pml (direction Z) (side High) (thickness ',num2str(pmlThickness,'%2.6f'),'))\r\n']);
  fprintf(FILE,'))\r\n');

  %%%%%%%%%%%%%%%%%%%%%%
  
  abc=0;
  mag=0;
  elec=0;
  boundary_types=zeros(1,6);
  abc_pars=[ (1/excFrequency)/3,2,0.001];

  fprintf(FILE,'\r\n;boundaries specification\r\n');

  % Assign boundaries: 0 Mag, 1 Elec, 2 Absorbing (PML)
  for i=1:6
    if FDTDobj.boundaries(i).type==10
      boundary_types(i)=2;
      if abc == 0
        abc_pars(1)=FDTDobj.boundaries(1).p(1);
        abc_pars(2)=FDTDobj.boundaries(2).p(2);
        abc_pars(3)=FDTDobj.boundaries(3).p(3);
      end
      abc = abc + 1;
    elseif FDTDobj.boundaries(i).type>1
      boundary_types(i)=2;
      abc = abc+1;
    elseif FDTDobj.boundaries(i).type==0
      boundary_types(i)=0;
      mag = mag+1;
    elseif FDTDobj.boundaries(i).type==1
      boundary_types(i)=1;
      elec = elec+1;
    end
  end
  
  if (abc==6)
    fprintf(FILE,  ['(set! pml-layers (list (make pml (thickness ', num2str(abc_pars(1)*(1/resolution),'%2.6f'), '))))\r\n'] );
  else
    if (abc~=0)
      fprintf(FILE,'(set! pml-layers\r\n');
      fprintf(FILE,'\t(list\r\n');
      for i=1:6
        if (boundary_types(i)==2)
          fprintf(FILE,  '\t\t(make pml (direction ');
          if ((i==1) | (i==4)); fprintf(FILE,  'X'); end;
          if ((i==2) | (i==5)); fprintf(FILE,  'Y'); end;
          if ((i==3) | (i==6)); fprintf(FILE,  'Z'); end;
          fprintf(FILE,  ') (side ');
          if (i<4); fprintf(FILE,  'Low) (thickness '); end;
          if (i>3); fprintf(FILE,  'High) (thickness '); end;
          fprintf(FILE, [num2str(abc_pars(1)*(1/resolution),'%2.6f'), '))\r\n']);
        end
      end
      fprintf(FILE, '\t))\r\n');
    end

    if ((elec>0) | (mag>0))
      fprintf(FILE,  '(init-fields)\r\n');
      if (FDTDobj.boundaries(1).type==0); fprintf(FILE,  '(meep-fields-set-boundary fields Low X Magnetic)\r\n');
      elseif (FDTDobj.boundaries(1).type==1); fprintf(FILE,  '(meep-fields-set-boundary fields Low X Metallic)\r\n'); end;
      if (FDTDobj.boundaries(2).type==0); fprintf(FILE,  '(meep-fields-set-boundary fields Low Y Magnetic)\r\n');
      elseif (FDTDobj.boundaries(2).type==1); fprintf(FILE,  '(meep-fields-set-boundary fields Low Y Metallic)\r\n'); end;
      if (FDTDobj.boundaries(3).type==0); fprintf(FILE,  '(meep-fields-set-boundary fields Low Z Magnetic)\r\n');
      elseif (FDTDobj.boundaries(3).type==1); fprintf(FILE,  '(meep-fields-set-boundary fields Low Z Metallic)\r\n'); end;
      if (FDTDobj.boundaries(4).type==0); fprintf(FILE,  '(meep-fields-set-boundary fields High X Magnetic)\r\n)');
      elseif (FDTDobj.boundaries(4).type==1); fprintf(FILE,  '(meep-fields-set-boundary fields High X Metallic)\r\n'); end;
      if (FDTDobj.boundaries(5).type==0); fprintf(FILE,  '(meep-fields-set-boundary fields High Y Magnetic)\r\n');
      elseif (FDTDobj.boundaries(5).type==1); fprintf(FILE,  '(meep-fields-set-boundary fields High Y Metallic)\r\n'); end;
      if (FDTDobj.boundaries(6).type==0); fprintf(FILE,  '(meep-fields-set-boundary fields High Z Magnetic)\r\n');
      elseif (FDTDobj.boundaries(6).type==1); fprintf(FILE,  '(meep-fields-set-boundary fields High Z Metallic)\r\n'); end;
    end
  end

  %%%%%%%%%%%%%%%%%%%%%%
  % frequency snapshots
  str = '\n';
  if (length(FDTDobj.frequency_snapshots)>0)
    str = [str, '(set! snapshots\n'];
    str = [str, '  (list\n'];
    for idx = 1:length(FDTDobj.frequency_snapshots)
      snapshot = FDTDobj.frequency_snapshots(idx);
      name = ['snapshot-',num2str(idx)]; % should be replaced by snapshot.name once the matlab parser is also able to get the name from the comment field
      center_vec3 = 0.5*(snapshot.P1 + snapshot.P2);
      size_vec3 = abs(snapshot.P2 - snapshot.P1);
      wavelength_mum = get_c0()/snapshot.frequency;
      E_vec3 = snapshot.E;
      H_vec3 = snapshot.H;
      J_vec3 = snapshot.J;
      str = [str, meepFrequencySnapshot(name,center_vec3,size_vec3,wavelength_mum,E_vec3,H_vec3,J_vec3,resolution)];
    end
    str = [str, '  )\n'];
    str = [str, ')\n'];
  end
  fprintf(FILE,str);
  
  %%%%%%%%%%%%%%%%%%%%%%
  % Run Command
  fprintf(FILE,'\r\n');
  % fprintf(FILE,'(init-fields)\r\n');
  runUntil=2*dxyz*numSteps;
  fprintf(FILE,['(run-until ',num2str(runUntil),'\r\n']);
  fprintf(FILE,'(at-beginning output-epsilon)\r\n');
  for m=1:length(FDTDobj.all_snapshots)
    entry = FDTDobj.all_snapshots(m);
    sliceCenter = (entry.P1+entry.P2)/2-geoCenter';
    sliceSize = abs(entry.P1-entry.P2);
    atEverySlice = 2*dxyz*entry.repetition;
    fprintf(FILE, sprintf('(to-appended "Slice%i"\r\n(at-every %2.4g\r\n(in-volume (volume (center %f %f %f) (size %f %f %f))\r\noutput-efield-x)))\r\n', m, atEverySlice, sliceCenter, sliceSize));
    fprintf(FILE, '\r\n');
  end
  fprintf(FILE, ')\r\n');


  fclose(FILE);
  
  disp(['Created ', filename]);
end
