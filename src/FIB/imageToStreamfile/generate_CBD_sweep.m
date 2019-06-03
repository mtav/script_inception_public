for rep = [1, 25, 50, 100]
  for d = [1, 100, 1000, 10000, 25500, 100000]
    dwell = d*ones(size(x));
    outfile = sprintf('CBD_1024x884.rep-%d.dwell-%d.gwl', rep, d);
    disp(outfile);
    writeStrFile(outfile, x, y, dwell, rep);
  end
end
