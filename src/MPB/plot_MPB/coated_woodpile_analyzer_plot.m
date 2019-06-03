function coated_woodpile_analyzer_plot(ret, n_index, k_index, band_index)
  
  y1 = ret.coated.data(n_index, :, k_index, band_index);
  y2 = ret.coated.data(n_index, :, k_index, band_index+1);

  y1_non_coated = ret.non_coated.data(k_index, band_index);
  y2_non_coated = ret.non_coated.data(k_index, band_index+1);
  
  size(y1)
  size(y1_non_coated)
  
  midgap = (y1+y2)./2;
  gapsize = (y2 - y1)./midgap;

  midgap_non_coated = (y1_non_coated+y2_non_coated)./2
  gapsize_non_coated = (y2_non_coated - y1_non_coated)./midgap_non_coated
  
  midgap_shift = midgap - midgap_non_coated;
  
  a=1;
  
  figure;

  x_range = [0,0.01];

  h1 = subplot(3,1,1);
  hold on;
  plot(ret.coated.t_list, a ./ midgap, 'b-o');
  hline(a ./ midgap_non_coated, 'k--');
  xlabel(ret.coated.header{2});
  ylabel('\lambda (\mum)');
  %ylabel('a/\lambda');
  set(gca,'Ydir','reverse');
  xlim(x_range);
  
  h2 = subplot(3,1,2);
  Y = a ./ midgap - a ./ midgap_non_coated;
  plot(ret.coated.t_list(2:end), diff(Y), 'b-o');
  xlabel(ret.coated.header{2});
  ylabel('\lambda (\mum)');
  %ylabel('a/\lambda');
  set(gca,'Ydir','reverse');
  xlim(x_range);
  
  h3 = subplot(3,1,3);
  plot(ret.coated.t_list, gapsize, 'b-o');
  xlabel(ret.coated.header{2});
  ylabel('relative gap size \Delta \omega / \omega')
  xlim(x_range);

  title(h1, sprintf('n = %.2f, k-index = %d, band-index =  %d', ret.coated.n_list(n_index), k_index, band_index));
  
  x = [0; ret.coated.t_list(:)];
  y = a ./ midgap;
  y = [ a ./ midgap_non_coated; y(:)];
  
  y_gapsize = [gapsize_non_coated(:); gapsize(:)];
  
  size(x)
  size(y)
  size(y_gapsize)
  
  figure;
  plot(x, y, 'b-o');
  
  figure;
  plot(x, y_gapsize, 'b-o');
  
  data = [x(:), y(:), y_gapsize(:)];
  size(data)
  
  writePrnFile(sprintf('lambda_vs_thickness_bands-%d-%d_k-%d.csv', band_index, band_index+1, k_index), {'thickness', 'lambda', 'relative_gap_size'}, data);
  
end
