function test_inputParserWrapper(req, varargin)

  p = inputParser();
  
  p = inputParserWrapper(p, 'addRequired', 'req');
  p = inputParserWrapper(p, 'addOptional', 'opt', 12);
  p = inputParserWrapper(p, 'addParamValue', 'par', 42);
  
  p = inputParserWrapper(p, 'parse', req, varargin{:});
  
  p.Results

%test_inputParserWrapper(45)
%ans =

  %scalar structure containing the fields:

    %req =  45
    %opt =  12
    %par =  42

%>> test_inputParserWrapper(45, 77)
%ans =

  %scalar structure containing the fields:

    %req =  45
    %opt =  77
    %par =  42

%>> test_inputParserWrapper(45, 77, 'par', 678)
%ans =

  %scalar structure containing the fields:

    %req =  45
    %opt =  77
    %par =  678

%>> test_inputParserWrapper(45, 'par', 678)
%error: argument '' is not a valid parameter
%error: called from
    %error at line 480 column 7
    %parse at line 397 column 13
    %inputParserWrapper at line 36 column 7
    %test_inputParserWrapper at line 9 column 5

% TODO: It should be possible to specify param value pairs without specifying all options...?
% TODO: print_usage is also not called if no options passed... How to call print_usage? Does it exist?

end
