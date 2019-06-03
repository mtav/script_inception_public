function saveas_fig_and_png(fig_handle, file_basename, varargin)
  % function saveas_fig_and_png(fig_handle, file_basename, varargin)
  %
  % parameters:
  %   saveMethod: 'default', 'gnuplot', 'latex'
  %   FontSize: numeric value
  
  %%%%% create parser
  save_method_list = {'default', 'gnuplot', 'latex'};
  
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'fig_handle');
  p = inputParserWrapper(p, 'addRequired', 'file_basename', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'saveMethod', 'default', @(x) any(validatestring(x, save_method_list)));
  p = inputParserWrapper(p, 'addParamValue', 'FontSize', NaN, @isnumeric);
  p = inputParserWrapper(p, 'parse', fig_handle, file_basename, varargin{:});
  
  saveMethod = validatestring(p.Results.saveMethod, save_method_list);
  
  % function saveas_fig_and_png(fig_handle, file_basename)
  
  if ~inoctave()
    saveas(fig_handle, [file_basename,'.fig']);
    %saveas(fig_handle, [file_basename,'.eps']);
  end
  
  if ~inoctave()
    saveas(fig_handle, [file_basename,'.png']);
  else
    
    try
      if ~isnan(p.Results.FontSize)
        FS = findall(fig_handle, '-property', 'FontSize');
        original_fontsizes = get(FS, 'FontSize');
        %disp('pause'); pause;
        set(FS, 'FontSize', p.Results.FontSize);
      end
      
      switch saveMethod
        case 'gnuplot'
          % this will not work because the graphics toolkit needs to be set before creating the figure...
          %disp('saving using gnuplot...');
          original_graphics_toolkit = graphics_toolkit(fig_handle);
          graphics_toolkit(fig_handle, 'gnuplot');
          %graphics_toolkit(fig_handle)
          print(fig_handle, sprintf('%s.png', file_basename), '-dpng');
          graphics_toolkit(fig_handle, original_graphics_toolkit);
          
        case 'latex'
          %disp('saving using latex...');
          return
          % Make sure to add $$ around any latex code for this to work properly...
          % this also seems to fail with the qt graphics_toolkit... (current default, and best GUI really...)
          origdir = pwd();
          TMP = tempname();
          mkdir(TMP);
          cd(TMP);
          
          tmpbasename = 'tmpbase';
          
          fprintf('creating .tex in %s\n', pwd());
          ok = false;
          n = 0;
          while ~ok && n<=100
            try
              print(fig_handle, '-depslatexstandalone', tmpbasename);
              ok = true;
            catch
              fprintf('FAIL %d\n', n);
              n = n+1;
            end
          end
          
          %## process generated files with pdflatex
          pwd
          cmd = sprintf('latex -halt-on-error %s.tex &> mylatex.log', tmpbasename)
          disp('latex run');
          STATUS = system( cmd );
          if STATUS~=0
            error('latex run failed');
          end
          %## dvi to ps
          pwd
          cmd = sprintf('dvips %s.dvi &> mydvips.log', tmpbasename)
          disp('dvips run');
          [STATUS, OUTPUT] = system( cmd );
          if STATUS~=0
            error('dvips run failed');
          end
          %## convert to png for wiki page
          cd(origdir);
          pwd
          out_ps = fullfile(TMP, [tmpbasename, '.ps']);
          if ~exist(out_ps)
            error('File not found: %s\n', out_ps);
          end
          cmd = sprintf('gs -dNOPAUSE -dBATCH -dSAFER -sDEVICE=png16m -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -r100x100 -dEPSCrop -sOutputFile=%s.png %s', file_basename, out_ps)
          disp('gs run');
          [STATUS, OUTPUT] = system( cmd );
          if STATUS~=0
            error('gs run failed');
          end
          
          cd(origdir);
          
        otherwise
          saveas(fig_handle, [file_basename,'.png']);
      end
    catch
      warning('Failed to save figure as %s', file_basename);
    end
  end
end
