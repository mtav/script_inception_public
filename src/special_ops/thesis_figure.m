function [fig, w_fig_cm, h_fig_cm] = thesis_figure(figtype)
  %%%%% create figure of specific size
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%% figure size vars
  
  %%% unit conversion
  % 1 inch = 25.4 mm = 2.54 cm
  % 1 pt = 1⁄72 inch = 2.54/72 cm
  pt_in_cm = 2.54/72;
  
  %%% dimensions of text area in thesis:
  textwidth_pt = 390.0; %pt
  textheight_pt = 592.0; %pt
  textwidth_cm = textwidth_pt * pt_in_cm;
  textheight_cm = textheight_pt * pt_in_cm;
  
  %%% A4 paper dimensions
  % according to LaTeX
  paperwidth_pt = 597.50787; %pt
  paperheight_pt = 845.04684; %pt
  % according to internet
  paperwidth_cm = 21.0;
  paperheight_cm = 29.7;
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  switch(figtype)
    case 1
      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      
      %% A4 210 x 297 mm
      %w_fig_cm = 21.0;
      %h_fig_cm = 29.7;
      
      %% A5 148 x 210 mm
      %w_fig_cm = 21.0;
      %h_fig_cm = 14.8;
      
      w_fig_cm = paperwidth_cm;
      h_fig_cm = textheight_cm*1/2;
      
      fig = figure('Units', 'centimeters', 'position', [0, 0, w_fig_cm, h_fig_cm]);
      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case 2
      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      %%%%% create figure of specific size
      
      %% A4 210 x 297 mm
      %w_fig_cm = 21.0;
      %h_fig_cm = 29.7;
      
      %% A5 148 x 210 mm
      w_fig_cm = 21.0;
      h_fig_cm = 14.8;
      
      %w_fig_cm = paperwidth_cm*95/100;
      %h_fig_cm = textheight_cm*1/3;
      
      fig = figure('Units', 'centimeters', 'position', [0, 0, w_fig_cm, h_fig_cm]);
      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case 3
      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      
      %% A4 210 x 297 mm
      %w_fig_cm = 21.0;
      %h_fig_cm = 29.7;
      
      %% A5 148 x 210 mm
      %w_fig_cm = 21.0;
      %h_fig_cm = 14.8;
      
      w_fig_cm = textwidth_cm + 2;
      h_fig_cm = textheight_cm*1/2;
      
      fig = figure('Units', 'centimeters', 'position', [0, 0, w_fig_cm, h_fig_cm]);
      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    otherwise
      error('Invalid figtype = %d', figtype);
  end

end
