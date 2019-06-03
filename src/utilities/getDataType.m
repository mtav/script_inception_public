function [TYPE_ID, TYPE_NAME] = getDataType(FILE)
  [ folder, basename_noext, ext ] = fileparts(FILE);
  basename = [basename_noext, ext];
  unknown = 1;
  
  if ~isempty(regexp(basename,'^p.*\.(prn|dat)$','ignorecase'))
    unknown = 0;
    TYPE_ID = 1;
    TYPE_NAME = 'Probe';
    %disp(TYPE_NAME)
  end
  
  if ~isempty(regexp(basename,'^[xyz]\d+.*\d\d\.(prn|dat)$','ignorecase'))
    unknown = 0;
    TYPE_ID = 2;
    TYPE_NAME = 'TimeSnapshot';
    %disp(TYPE_NAME)
  end
  
  if ~isempty(regexp(basename,'^[xyz][a-z{|}~][a-z{]?.*\d\d\.(prn|dat)$','ignorecase'))
    unknown = 0;
    TYPE_ID = 3;
    TYPE_NAME = 'FrequencySnapshot';
    %disp(TYPE_NAME)
  end

  if ~isempty(regexp(basename,'^ref\.(prn|dat)$','ignorecase'))
    unknown = 0;
    TYPE_ID = 4;
    TYPE_NAME = 'Reference';
    %disp(TYPE_NAME)
  end
    
  if unknown
    disp(['WARNING: unknown data : ',basename])
    TYPE_ID = -1;
    TYPE_NAME = 'unknown';
    %disp(TYPE_NAME)
    return
  end
end
