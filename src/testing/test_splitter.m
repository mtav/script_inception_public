clear all; close all;

function ret = split_it(Nsnaps, Nsnaps_max)
  Nparts = ceil(Nsnaps/Nsnaps_max);
  n2 = floor(Nsnaps/Nparts);
  n1 = n2 + 1;
  m1 = Nsnaps - n2*Nparts;
  m2 = Nparts - m1;
  ret = [n1*ones(m1,1); n2*ones(m2,1)];
  
  msg = sprintf('sum(ret(:))=%d, Nsnaps=%d, max(ret(:))=%d, Nsnaps_max=%d\n', sum(ret(:)), Nsnaps, max(ret(:)), Nsnaps_max);
  %fprintf(msg);
  if (sum(ret(:)) ~= Nsnaps) || (max(ret(:)) > Nsnaps_max)
    error(msg);
  end
end

Nsnaps_max = 52;
for Nsnaps = 1:500
  ret = split_it(Nsnaps, Nsnaps_max);
  hold off;
  bar(ret);
  ylim([0, Nsnaps_max+1]);
  hline(Nsnaps_max);
  sleep(0.0001);
end
