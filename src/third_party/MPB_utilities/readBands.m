%[list,bloc]=readBands(file)
%---------------------------
%
%Scans a "MIT Photonic-Bands" simulation output file for data
%sections and reads them in.
%
% list{}          band structures
%     .file          full file name
%     .grid          grid size in [x;y;z] column
%     .size          lattice size as [x;y;z] column
%     .lattice       lattice vectors in [x y z] rows
%     .reciprocal    reciprocal lattice vectors in [x y z] rows
%     .geometry      unit cell geometry as cell strings
%     .polarity      band polarisation 'none | yeven | yodd | zeven(te) | zodd(tm)'
%     .vectors       wave vectors in [x y z k] rows
%     .bands         wave frequencies in [1 2 3 ...] rows
%     .ranges        band ranges in [from;to] columns
%     .xvelocity
%     .yvelocity
%     .zvelocity     x/y/z group velocity in [1 2 3 ...] rows
%     .yparity
%     .zparity       y/z-parity [-1...+1] in [1 2 3 ...] rows
%     .time          total elapsed time for computation in seconds
%
% bloc   last cell of data in case of error
% file   simulation file name
%
function [list,bloc] = readBands(file)
  if ~nargin | isempty(file) | ~ischar(file)
     error('Unknown or undefined argument.');
  end;
  if ~nargout
     error('Unknown return value.');
  end;
  [fid,msg]=fopen(file,'rt');
  if fid < 0
     error(msg);
  end;
  list={};
  line=fgetl(fid);
  while ischar(line)
     bloc={};
     bloc.file=fopen(fid);         % file name
     bloc.grid=zeros(3,1);
     bloc.size=zeros(3,1);
     bloc.lattice=zeros(3);
     bloc.reciprocal=zeros(3);
     bloc.geometry={};
     bloc.polarity='';
     while ~length(strmatch('Grid size',line))
        line=fgetl(fid);
        if ~ischar(line)        % grid size
           return;
        end;
     end;
     bloc.grid=sscanf(line,'Grid size is %d x %d x %d');
     line=fgetl(fid);           % lattice
     while ischar(line) & ~length(strmatch('Lattice vectors',line))
        line=fgetl(fid);
     end;
     for i=1:3
        line=fgetl(fid);
        if ~ischar(line)
           'Corrupt lattice definition.'
           return;
        end;
        bloc.lattice(i,:)=sscanf(line(findstr(line,'('):length(line)),'(%f, %f, %f)')';
        bloc.size(i)=norm(bloc.lattice(i,:));
     end;
     line=fgetl(fid);           % reciprocal lattice
     while ischar(line) & ~length(strmatch('Reciprocal lattice vectors',line))
        line=fgetl(fid);
     end;
     for i=1:3
        line=fgetl(fid);
        if ~ischar(line)
           'Corrupt reciprocal lattice definition.'
           return;
        end;
        bloc.reciprocal(i,:)=sscanf(line(findstr(line,'('):length(line)),'(%f, %f, %f)')';
     end;
     line=fgetl(fid);           % unit cell geometry
     while ischar(line) & ~length(strmatch('Geometric objects',line))
        line=fgetl(fid);
     end;
     line=fgetl(fid);
     while ischar(line) & ~length(strmatch('Geometric object t',line))
        bloc.geometry{length(bloc.geometry)+1}=line;
        line=fgetl(fid);
     end;
     i=0;                       % number of wave vectors
     n=[];
     line=fgetl(fid);
     while ischar(line) & isempty(n)
        n=sscanf(line,'%d k-points:');
        line=fgetl(fid);
     end;
     while ischar(line) & ~length(strmatch('Solving for band p',line))
        line=fgetl(fid);
     end;
     if ~ischar(line)           % band polarity
        'Corrupt polarity definition.'
        return;
     end;
     bloc.polarity=line(findstr(line,': ')+2:length(line)-1);
     line=fgetl(fid);
     while ischar(line) & ~length(strmatch('Band ',line))
        s=findstr(line,':, ');
        if length(s) == 1 & s > 5
           switch line(s-5:s-1)
           case 'freqs'         % band frequency
              if i
                 v=sscanf(line(s+1:length(line)),', %f',inf)';
                 if v(1) ~= i
                    'Synchronization lost.'
                 end;
                 bloc.bands(i,:)=v(6:length(v));
                 bloc.vectors(i,:)=v(2:5);
              else
                 bloc.bands=zeros(n,length(findstr(line,','))-5);
              end;
              i=i+1;
           case 'ocity'         % x/y/z group velocity
              l=[' ' line];
              l=l(s-8);
              s=findstr(line,',');
              if sscanf(line(s(1):s(2)),', %d') ~= i-1
                 'Synchronization lost.'
              end;
              switch l
              case {'x','y','z'}
                 v=sscanf(line(s(2):length(line)),', %f',inf)';
              end;
              switch l
              case 'x'
                 if i == 2
                    bloc.xvelocity=zeros(n,length(v));
                 end;
                 bloc.xvelocity(i-1,:)=v;
              case 'y'
                 if i == 2
                    bloc.yvelocity=zeros(n,length(v));
                 end;
                 bloc.yvelocity(i-1,:)=v;
              case 'z'
                 if i == 2
                    bloc.zvelocity=zeros(n,length(v));
                 end;
                 bloc.zvelocity(i-1,:)=v;
              otherwise
                 v=sscanf(line(s(2):length(line)),', #(%f %f %f)',[3 inf]);
                 if i == 2
                    bloc.xvelocity=zeros(n,size(v,2));
                    bloc.yvelocity=bloc.xvelocity;
                    bloc.zvelocity=bloc.xvelocity;
                 end;
                 bloc.xvelocity(i-1,:)=v(1,:);
                 bloc.yvelocity(i-1,:)=v(2,:);
                 bloc.zvelocity(i-1,:)=v(3,:);
              end;
           case 'arity'         % y/z parity
              s=findstr(line,',');
              if sscanf(line(s(1):s(2)),', %d') ~= i-1
                 'Synchronization lost.'
              end;
              v=sscanf(line(s(2):length(line)),', %f',inf)';
              switch line(s-7)
              case 'y'
                 if i == 2
                    bloc.yparity=zeros(n,length(v));
                 end;
                 bloc.yparity(i-1,:)=v;
              case 'z'
                 if i == 2
                    bloc.zparity=zeros(n,length(v));
                 end;
                 bloc.zparity(i-1,:)=v;
              otherwise
                 'Unknown parity tag.'
              end;
           otherwise
              'Unknown data tag.'
           end;
        end;
        line=fgetl(fid);
     end;
     n=size(bloc.bands,2);      % band limits
     bloc.ranges=zeros(2,n);
     for i=1:n
        if ~ischar(line)
           return;
        end;
        if sscanf(line(6:10),'%d') ~= i
           'Synchronization lost.'
        end;
        bloc.ranges(:,i)=sscanf(line(findstr(line,': ')+1:length(line)),'%f at #(%*f %*f %*f) to %f')';
        line=fgetl(fid);
     end;
     while ischar(line)            % total elapsed time
        if  strcmp(line(1:5),'total')
           line=line(findstr(line,':')+2:length(line));
           n=findstr(line,',');
           bloc.time=0;
           while length(n)
              bloc.time=bloc.time*60+sscanf(line,'%d');
              line=line(n(1)+2:length(line));
              n=findstr(line,',');
           end;
           bloc.time=bloc.time*60+sscanf(line,'%d');
           break;
        end;
        line=fgetl(fid);
     end;
     list{length(list)+1}=bloc;
     line=fgetl(fid);
  end;
  fclose(fid);
  bloc={};
end
