function plotDBR(datfile)
%    close all;
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
    plot(x, data(:,m));
  end

  xlim([-0.5,0.5]);
  ylim([0,0.30]);
  title(datfile, 'interpreter', 'none');
end
