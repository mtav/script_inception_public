function ret = plotSnapshot3D(prnfile, titro, dosave, outfile_basename)
  % currently customized for the woodpile snapshots
  %p = inputParser();
  %p = inputParserWrapper(p, 'addRequired', 'bfdtd_file_list', @iscellstr);
  %p = inputParserWrapper(p, 'parse', bfdtd_file_list, varargin{:});

  %ret.x=2
  
  %save('/tmp/foo.struct', 'ret');

  [basename_str, path_str, basename_str_with_suffix] = basename(prnfile, '.prn');
  cropped_prnfile = fullfile(path_str, [basename_str, '.cropped.prn'])

  ret = struct();
  ret.xmin =  2.4936;
  ret.xmax =  3.1652;
  ret.ymin =  2.4936;
  ret.ymax =  3.1652;
  ret.zmin =  2.5776;
  ret.zmax =  3.2492;

  [ret.header, ret.data, ret.u1, ret.u2] = readPrnFile(prnfile);
  
  ret.data_normalized = ret.data/max(ret.data(:));
  
  figure;
  
  [ret.U1, ret.U2] = meshgrid(ret.u1, ret.u2);
  
  if strcmpi(ret.header{1},'x')  && strcmpi(ret.header{2},'y')
    ret.dir = 3;
    
    [Nx, Ny, Nv] = subsurface(ret.U1, ret.U2, ret.data_normalized, [ret.xmin, ret.xmax, ret.ymin, ret.ymax]);
    %surf(ret.U1, ret.U2, ret.data_normalized);
    surf(Nx, Ny, Nv);
    
    %xlabel(ret.header{1});
    %ylabel(ret.header{2});
    xlabel('x ($\mu m$)', 'interpreter','latex');
    ylabel('y ($\mu m$)', 'interpreter','latex');

    %writePrnFile(cropped_prnfile, {'x', 'y', 'EnergyDensity'}, ret.data);
    
  elseif strcmpi(ret.header{1},'y')  && strcmpi(ret.header{2},'z')
    ret.dir = 1;
    
    [Ny, Nz, Nv] = subsurface(ret.U1, ret.U2, ret.data_normalized, [ret.ymin, ret.ymax, ret.zmin, ret.zmax]);    
    %surf(ret.U2, ret.U1, ret.data_normalized);
    surf(Nz, Ny, Nv);
    
    %xlabel(ret.header{2});
    %ylabel(ret.header{1});
    xlabel('z ($\mu m$)', 'interpreter','latex');
    ylabel('y ($\mu m$)', 'interpreter','latex');
    
  elseif strcmpi(ret.header{1},'x')  && strcmpi(ret.header{2},'z')
    ret.dir = 2;
    
    [Nx, Nz, Nv] = subsurface(ret.U1, ret.U2, ret.data_normalized, [ret.xmin, ret.xmax, ret.zmin, ret.zmax]);
    %surf(ret.U2, ret.U1, ret.data_normalized);
    surf(Nx, Nz, Nv);
    
    %xlabel(ret.header{1});
    %ylabel(ret.header{2});
    xlabel('x ($\mu m$)', 'interpreter','latex');
    ylabel('z ($\mu m$)', 'interpreter','latex');
    
  else
    error('unknown snapshot direction!!!');
  end
  
  
  %zlabel(ret.header{3});
  %zlabel('\varepsilon|E|^2 (a.u.)');
  %zlabel('\varepsilon|E|^2/max(\epsilon|E|^2) (a.u.)');
  %zlabel('Normalized energy density (a.u.)');
  zlabel('$\varepsilon|E|^2 (a.u.)$', 'interpreter','latex');
  
  grid off;
  shading interp;
  
  %view(2);
  view(45, 45);
  
  %colorbar;
  
  %AspectRatio = get(gca,'DataAspectRatio');
  %AspectRatio(1) = AspectRatio(2);
  %set(gca,'DataAspectRatio',AspectRatio);
  
  daspect([1 1 2]);
  
  axis tight;

  %cb = colorbar;
  cb = colorbar('southoutside');
  
  ax = gca();
  %axpos = ax.Position; % Matlab-only
  axpos = get(ax, "Position");
  
  %cpos = cb.Position; % Matlab-only
  cpos = get(cb, "Position");
  
  cpos(1) = 0.3;
  cpos(3) = 0.5*cpos(3);
  cpos(4) = 0.5*cpos(4);
  %cb.Position = cpos; % Matlab-only
  set(cb, "Position", cpos);
  
  %ax.Position = axpos; % Matlab-only
  set(ax, "Position", axpos);
  
  ret.cb = cb;
  
  %set(cb,'position',[.8 .2 .02 .5]);
  
  %title(titro, 'Interpreter', 'None');
  
  set(gcf, 'PaperPositionMode', 'auto');
  
  if dosave
    outfile_basename
    %saveas_fig_and_png(gcf, outfile_basename);
    
    %saveas(gcf, snapshot_filename_base, 'fig');
    %print(outfile_basename, '-dpdf', '-r300');
    print([outfile_basename, '.r300.png'], '-dpng', '-r300');
    %!pdfcrop -margins 10 autoExample.pdf autoExample.pdf
    %!pdfcrop autoExample.pdf autoExample.pdf
    %!pdfcrop autoExample.pdf
    %system(['pdfcrop ', outfile_basename, '.pdf ', outfile_basename, '.pdf']);
    %system(['pdfcrop --margins "-5 -30 -10 -25" ', snapshot_filename_base,'.pdf ', snapshot_filename_base, '_cropped.pdf']);
    
  end
end
