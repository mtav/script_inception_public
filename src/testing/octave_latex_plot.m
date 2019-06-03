close all; clear all;
TESTDIR='/tmp/test/';
cd(TESTDIR);

%gset output "the_file.eps"
%gset term postscript eps

function r = Na(theta, L)
    W = 800*1000;
    w = 20;
    w_one = 200*1000;
    po180 = 3.14159 / 180;
    r = (w_one * 1.5 + (w_one*L).*(L.*cos(theta * po180)) - W*(L-3.3)) / 2.3;
end

function save1()
  gt_list = available_graphics_toolkits();

  % gnuplot backend renders latex ok, but looks ugly

  for idx = 1:numel(gt_list)
    gt = gt_list{idx};
    
    disp(gt);
    
    close all;
    graphics_toolkit(gt);

    font0 = '/usr/share/fonts/truetype/fonts-lyx/cmr10.ttf';
    
    fig = plot1();
    
    FL1 = findall(fig, '-property', 'FontName');
    set(FL1, 'FontName', font0);
    
    outfile = sprintf('%s.png', gt);
    print(fig, outfile, '-dpng');
    
    outfile = sprintf('%s.pdf', gt);
    print(fig, outfile, '-dpdf');
    
  end
end

function save2wrapper()
  gt_list = available_graphics_toolkits();
  for idx = 1:numel(gt_list)
    gt = gt_list{idx};
    disp(gt);
    %disp('press enter...'); pause;
    save2(gt);
  end
end

function save2(gt)
  close all;
  
  graphics_toolkit(gt);
  %graphics_toolkit fltk;
  
  fig = plot2();

  delete('./somb*');
  %pause

  print -depslatexstandalone somb

  ## process generated files with pdflatex
  system ("latex somb.tex");

  ## dvi to ps
  system ("dvips somb.dvi");

  ## convert to png for wiki page
  system ("gs -dNOPAUSE -dBATCH -dSAFER -sDEVICE=png16m -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -r100x100 -dEPSCrop -sOutputFile=somb.png somb.ps")
end

function save3(theta)

  close all;
  graphics_toolkit fltk;

  plot(theta, Na(theta, 2), "s", theta, Na(theta, 4), "s", theta, Na(theta, 5), "s");

  s = '$T \lambda x^{min}_{max}$';
  %s = '$hello \lambda$';

  xlabel(s);
  ylabel(s);

  title ("The sombrero function:")
  fcn = "$z = \\frac{\\sin\\left(\\sqrt{x^2 + y^2}\\right)}{\\sqrt{x^2 + y^2}}$";
  text(10, 1.6e6, fcn, "fontsize", 20);
end

function save4(TESTDIR)
  outbase = fullfile(TESTDIR, 'nice');
  cd(dirname(outbase));
  
  print(gcf, '-depslatexstandalone', outbase);
  %## process generated files with pdflatex
  pwd
  cmd = sprintf('latex %s.tex', outbase)
  disp('continue?'); pause;
  system( cmd );
  %## dvi to ps
  pwd
  cmd = sprintf('dvips %s.dvi', outbase)
  disp('continue?'); pause;
  system( cmd );
  %## convert to png for wiki page
  pwd
  cmd = sprintf('gs -dNOPAUSE -dBATCH -dSAFER -sDEVICE=png16m -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -r100x100 -dEPSCrop -sOutputFile=%s.png %s.ps', outbase, outbase)
  disp('continue?'); pause;
  system( cmd );

end

function save5()
  clear;clc;close all;
  
  font0 = '/usr/share/fonts/truetype/fonts-lyx/cmr10.ttf';
  font1 = '/usr/share/fonts/dejavu/DejaVuSerifCondensed.ttf';
  font2 = '/usr/share/fonts/dejavu/DejaVuSerif-Italic.ttf';
  font3 = '/usr/share/fonts/msttcore/cour.ttf';

  h = plot3();
  
  FN = findall(h,'-property','FontName');
  set(FN,'FontName', font0);
  FS = findall(h,'-property','FontSize');
  set(FS,'FontSize',6);
  %FL1 = findall(L,'-property','FontName');
  %set(FL1,'FontName', font0);
  %FL2 = findall(L,'-property','FontSize');
  %set(FL2,'FontSize',8);
  H = 3; W = 4;
  set(h,'PaperUnits','inches');
  set(h,'PaperOrientation','portrait');
  set(h,'PaperSize',[H,W]);
  set(h,'PaperPosition',[0,0,W,H]);
  print(h,'-dpng','-color','vib_plt4.png');
end

function fig_handle = plot1()
  fig_handle = figure();
  %s = '$T \lambda x^{min}_{max}$';
  s = 'T \lambda x^{min}_{max}';
  theta = linspace(0, 60, 200);
  plot(theta, Na(theta, 2), "s", theta, Na(theta, 4), "s", theta, Na(theta, 5), "s");
  xlabel(s);
  ylabel(s);
end

function fig_handle = plot2()
  fig_handle = figure();
  sombrero();
  title ("The sombrero function:");
  %fcn = "$z = \\frac{\\sin\\left(\\sqrt{x^2 + y^2}\\right)}{\\sqrt{x^2 + y^2}}$";
  fcn = 'z = \frac{\sin\left(\sqrt{x^2 + y^2}\right)}{\sqrt{x^2 + y^2}}';
  text (0.5, -10, 1.8, fcn, "fontsize", 20);
end

function fig_handle = plot3()
  fig_handle = figure();
  x0= 0.025; %m
  v0= 0.000; %m/s
  t = linspace(0,60,1000);
  m = 1;     % kg
  c = 0.1;   % N*sec/meter
  k = 2.5;   % N/m
  
  omega_n = sqrt(k/m);
  zeta    = 0.5*c/m/omega_n;
  
  x = exp(-zeta*omega_n*t).*(x0*cos(sqrt(1-zeta^2)*omega_n*t) +...
     (v0+zeta*omega_n*x0)/sqrt(1-zeta^2)/omega_n*...
     (sin(sqrt(1-zeta^2)*omega_n*t)));
  plot(t,x.*1000,'r-','LineWidth',4);
  
  title(["Response of an Underdamped Single Degree of\n"...
        "Freedom System Subjected to an Initial Excitation"],...
        'FontSize',8);
  xlabel('Time (seconds)','FontSize',8);
  ylabel('Displacement (mm)','FontSize',8);
  
  grid on;

  L = legend(["x_0 = ", num2str(x0*1000,'%4.1f'), " mm    ", "\nv_0 =  ", num2str(v0*1000,'%4.1f'), " mm/sec", "\n  m =  ", num2str(m,'%4.1f'),       " kg    ", "\n  c = ", num2str(c/1000,'%5.1e'),  " N-s/mm", "\n  k = ", num2str(k/1000,'%5.1e'),  " N/mm  "]);
end

function saveAll(fig_handle, file_basename_in, varargin)
  save_method_list = {'default', 'gnuplot', 'latex'};
  for idx = 1:numel(save_method_list)
    save_method = save_method_list{idx};
    file_basename = [file_basename_in, '.', save_method];
    saveas_fig_and_png(gcf, file_basename, 'saveMethod', save_method);
  end
end

cd(TESTDIR);

%graphics_toolkit('qt');
%graphics_toolkit('gnuplot');
%fig_handle = plot1();
%print(fig_handle, 'a.png', '-dpng');

%STOP

%save1();

%save2wrapper();
%STOP

close all;
fig_handle = plot1();
saveAll(fig_handle, 'plot1');

fig_handle = plot2();
saveAll(fig_handle, 'plot2');

fig_handle = plot3();
saveAll(fig_handle, 'plot3');
