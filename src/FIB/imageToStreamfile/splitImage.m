rep = 1;
S = 7500/max(double(BW(:)))

[x, y, dwell] = imageToStreamfile2(BW);
outfile = 'JGR_1024x884.str';
disp(outfile);
writeStrFile(outfile, x, y, dwell.*S, rep);

readStrFile(outfile, 5000);

H = size(BW,1);

N=2*2*17;

BW_list = {};
a_list = {};
b_list = {};

idx_x = 1;

while idx_x < H
  a = idx_x;
  b = idx_x + N - 1;
  I = uint8(zeros(size(BW)));
  I(a:b, 1:end) = BW(a:b, 1:end);
  BW_list{end+1} = I;
  a_list{end+1} = a;
  b_list{end+1} = b;
  idx_x = idx_x + N;
end

outfile_list = {};
for idx = 1:length(BW_list)
  [x, y, dwell] = imageToStreamfile2(BW_list{idx});
  outfile = sprintf('JGR_1024x884_%03d-%03d.str', a_list{idx}, b_list{idx});
  disp(outfile);
  writeStrFile(outfile, x, y, dwell.*S, rep);
  outfile_list{end+1} = outfile;
end
