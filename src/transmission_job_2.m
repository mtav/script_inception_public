%%empty-block
in='empty'
out='block'
getS21([in,filesep,'i1id00.prn'],[out,filesep,'i1id00.prn'],['snapshot-S11-',in,'-',out],'snapshot S11');
getS21([in,filesep,'i1id00.prn'],[out,filesep,'i2id00.prn'],['snapshot-S21-',in,'-',out],'snapshot S21');
%tdtreat([in,filesep,'p001id.prn'],[out,filesep,'p001id.prn'],['probe-S11-',in,'-',out],'probe S11');
%tdtreat([in,filesep,'p001id.prn'],[out,filesep,'p002id.prn'],['probe-S21-',in,'-',out],'probe S21');

%%bulk-block
in='bulk'
out='block'
getS21([in,filesep,'i1id00.prn'],[out,filesep,'i1id00.prn'],['snapshot-S11-',in,'-',out],'snapshot S11');
getS21([in,filesep,'i1id00.prn'],[out,filesep,'i2id00.prn'],['snapshot-S21-',in,'-',out],'snapshot S21');
%tdtreat([in,filesep,'p001id.prn'],[out,filesep,'p001id.prn'],['probe-S11-',in,'-',out],'probe S11');
%tdtreat([in,filesep,'p001id.prn'],[out,filesep,'p002id.prn'],['probe-S21-',in,'-',out],'probe S21');

%%block-cylinder
in='block'
out='cylinder'
getS21([in,filesep,'i1id00.prn'],[out,filesep,'i1id00.prn'],['snapshot-S11-',in,'-',out],'snapshot S11');
getS21([in,filesep,'i1id00.prn'],[out,filesep,'i2id00.prn'],['snapshot-S21-',in,'-',out],'snapshot S21');
%tdtreat([in,filesep,'p001id.prn'],[out,filesep,'p001id.prn'],['probe-S11-',in,'-',out],'probe S11');
%tdtreat([in,filesep,'p001id.prn'],[out,filesep,'p002id.prn'],['probe-S21-',in,'-',out],'probe S21');
