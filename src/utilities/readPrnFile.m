function [header, data, ux, uy] = readPrnFile(filename, varargin)
  % function [header, data, ux, uy] = readPrnFile(filename)
  %
  % header = cell array of strings created from space-separated words in the first line of the input file
  %
  % If ux and uy are not requested:
  %   data = 2D matrix of size (N_lines, N_columns) created from the lines of the input file after the first line.
  %
  % If ux and uy are requested:
  %   ux = list of unique values in column 1 and of size NX
  %   uy = list of unique values in column 2 and of size NY
  %   data = 3D matrix of size (NY, NX, N_data_columns) of col(3:) vs ( col(1), col(2) )
  %
  % TODO: Change data to be (NX, NY, N_data_columns), i.e. invert meaning of ux and uy?
  %       -> Makes data access indices much more consistent and logical...
  %       We are working with matrices in general and not (X,Y) planar coordinates.
  %       (in which case X,Y access still makes more sense than Y,X...)
  %       -> This is a major change and might break a lot of things down the line.
  %       -> A simple solution would be to add an option to load a "transposed" data matrix with a deprecation warning.
  %       -> Once all scripts using readPrnFile are updated to the new system, the option could be removed (or its default value changed)
  % TODO: Add better error handling when file is empty, has bad format, etc
  % TODO: Progress bar or some other form of feedback. (needs GUI feedback)
  % TODO: Add check for invalid .prn files where length(M)/ncols!=length(M)//ncols (//=integer division)
  % TODO: Get max_cols automatically, quickly and safely. Add step function as well? (ex: to get every 10 lines)
  % TODO: Implement settings to also be able to read .csv files where "x/y columns" are inverted. + with varying header length?
  % TODO: Auto-detect delimiter via try statements? Note that the default delimiter used in .prn files seems to be spaces, NOT tabs.
  % TODO: Use textscan instead of dlmread? -> Seems more robust at handling inconsistent line ending types. And used by matlab-generated import scripts.
  %
  % Example code for general reshaping:
  %  Find correct N using unique() and size() on x/y and then:
  %  X = reshape(x, N, []);
  %  Y = reshape(y, N, []);
  %  Z = reshape(z, N, []);
  %
  % TODO: Update so that it returns coords+data in meshgrid format (including first two columns) -> might cause problems/slowdowns in PP+calculateMV but needs to be done!
  % TODO: + this will also require update of writePrnFile?
  %
  % TODO: Inconsistent behaviour: [h,d] will return d with all columns, but [h,d,u1,u2] will return d with Ncols-2...
  % TODO: support the greeped output from MPB... (old .dat format)
  % TODO: use 'auto' for custom delimiter guessing and '' for matlab-delimiter guessing? or similar...
  % TODO: separate header and data delimiters?
  % All ASCII data should really be stored using ';'... No commas because it can be a decimal separator and no whitespace because it's in headers, etc...
  
  % create parser
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'filename', @ischar);
  p = inputParserWrapper(p, 'addOptional', 'max_lines', NaN, @isnumeric);
  p = inputParserWrapper(p, 'addOptional', 'max_cols', NaN, @isnumeric);
  p = inputParserWrapper(p, 'addOptional', 'delimiter', '', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'GuessCsvDelimiter', true, @islogical);
  
  p = inputParserWrapper(p, 'addParamValue', 'includeAllColumns', false, @islogical);
  
  % TODO: Maybe implement these:
  %p = inputParserWrapper(p, 'addParamValue', 'meshgrid', false, @islogical); % not necessary since data(:,:,1 or 2) can be used
  %p = inputParserWrapper(p, 'addParamValue', 'transpose', false, @islogical); % could be useful, cf thesis_readPrnFiles.m
  
  p = inputParserWrapper(p, 'addParamValue', 'verbosity', 1, @isnumeric);
  p = inputParserWrapper(p, 'parse', filename, varargin{:});

  % assign input arguments
  filename = p.Results.filename;
  max_lines = p.Results.max_lines;
  max_cols = p.Results.max_cols;
  delimiter = p.Results.delimiter;
  
  % offer ui if no filename specified
  if (nargin == 0)
    [FileName,PathName] = uigetfile({'*.prn *.dat'},'Select the prn-file',getenv('DATADIR'));
    filename = [PathName,filesep,FileName];
  end
  
  % Prevent Matlab from loading data from some random place in the Matlab path!!! Why does "exist" not distinguish between random file in matlab path and file in filesystem path???
  filename = GetFullPath(filename);

  % check that the files exist
  if ~exist(filename, 'file')
    error('readPrnFile:FileNotFound', ['File not found: ', filename]);
  end
  
  if(p.Results.verbosity >= 2)
    tic;
    disp(['Loading: ', basename(filename), ' , full path: ', filename]);
    disp(['from ',pwd()]);
    disp('Patience young Padawan, this may take a while...');
    disp('...');
  end
  
  %%%%%%%%%%%%%%%%
  %%% get header (and guess delimiter if necessary)
  [header, delimiter] = readHeader(filename, delimiter, p.Results.GuessCsvDelimiter);
  %%%%%%%%%%%%%%%%
  %%% get data

  % We start reading from the second line, skipping the header.
  %if exist('max_lines','var') == 0 || exist('max_cols','var') == 0
  if isnan(max_lines) || isnan(max_cols)
    data = dlmread(filename, delimiter, 1, 0);
  else
    data = dlmread(filename, delimiter, [1, 0, max_lines, max_cols-1]);
  end

  % We store the number of columns for processing the header at the end.
  ncols = size(data,2);

  %%%%%%%%%%%%%%%%
  %%% reshape data if requested
  ux = [];
  uy = [];
  if nargout > 3
    x = data(:,1);
    y = data(:,2);
    ux = unique(x);
    nx = length(ux);
    if mod(length(x), nx) ~= 0
      error('Invalid snapshot file.');
    end
    ny = length(x)/nx;
    uy = y(1:ny);
    
    if p.Results.includeAllColumns
      for m = 1:size(data,2)
        data_reshaped(:,:,m) = reshape(data(:,m),ny,nx);
      end
    else
      warning('Deprecated system: Please use the includeAllColumns = true parameter.');
      for m = 3:size(data,2)
        data_reshaped(:,:,m-2) = reshape(data(:,m),ny,nx);
      end
    end
    data = data_reshaped;
  end
  
  %%%%%%%%%%%%%%%%
  % make sure header and data have same number of columns
  
  if ncols > length(header)
    warning('Not enough column headers found for the number of columns of data.');
  end
  
  % truncate header, so it fits data
  header = header(1:min(ncols, length(header)));
  %%%%%%%%%%%%%%%%
  
  if(p.Results.verbosity >= 2)
    disp('...loading done');
    toc;
  end

end
