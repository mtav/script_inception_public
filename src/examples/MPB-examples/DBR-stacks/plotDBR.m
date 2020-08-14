function plotDBR(datfile, eps1)
  % close all;
  [header, data] = readPrnFile(datfile);

  k_index = data(:,1);
  k1 = data(:,2);
  k2 = data(:,3);
  k3 = data(:,4);
  kmag_over_2pi = data(:,5);

  x = k1;

  figure;
  hold on;

  for m = 6:size(data,2)
    plot(x, data(:,m), 'bo');
  end

  wn_range = [0,0.30];
  xlim([-0.5,0.5]);
  ylim(wn_range);

  hold on;
  wn = linspace(wn_range(1), wn_range(2));
  k = DBR_bands(wn, sqrt(eps1), sqrt(13), 0.5, 0.5);
  plot(real(k)./(2*pi), wn, 'k-');
  plot(-real(k)./(2*pi), wn, 'k-');
  title(datfile, 'interpreter', 'none');
  
  info = DBRinfo(sqrt(eps1), sqrt(13), 't1', 0.5, 't2', 0.5);
  hline(info.solved.topgap, 'r--', 'topgap');
  hline(info.solved.midgap, 'b--', 'midgap');
  hline(info.solved.botgap, 'r--', 'botgap');
end
