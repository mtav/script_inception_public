%getS21('empty/i1id00.prn','bulk/i1id00.prn','S11-empty-bulk','S11'); getS21('empty/i2id00.prn','bulk/i2id00.prn','S21-empty-bulk','S21');

list = {'empty','bulk','block','prism_block','prism'};
for i = 1:length(list)
  for j = i+1:length(list)
    disp([list{i},'-',list{j}]);
    getS21([list{i},filesep,'i1id00.prn'],[list{j},filesep,'i1id00.prn'],['snapshot-S11-',list{i},'-',list{j}],'snapshot S11');
    getS21([list{i},filesep,'i2id00.prn'],[list{j},filesep,'i2id00.prn'],['snapshot-S21-',list{i},'-',list{j}],'snapshot S21');
    tdtreat([list{i},filesep,'p001id.prn'],[list{j},filesep,'p001id.prn'],['probe-S11-',list{i},'-',list{j}],'probe S11');
    tdtreat([list{i},filesep,'p002id.prn'],[list{j},filesep,'p002id.prn'],['probe-S21-',list{i},'-',list{j}],'probe S21');
  end
end
