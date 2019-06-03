MAINDIR='~/TEST/dipole+block/';
cd(MAINDIR);
file_list = {'sim.inp', 'sim.geo'};
[entries, FDTDobj] = GEO_INP_reader(file_list);

filename='mesh.inp';
fulltext = fileread(filename);

% remove comments
pattern_stripcomments = '\*\*(?!name=).*\n';
% does not seem to work anymore on Matlab 2013 and 2015?! (at least on BC3) :/
cleantext =  regexprep(fulltext, pattern_stripcomments, '\n', 'lineanchors', 'dotexceptnewline', 'warnings');

% extract blocks
pattern_objects = '^(?<type>\w+)\s*(?<nameblob>[^\{\}]+)?\{(?<data>[^\{\}]*?)\}';
if inoctave()
  [tokens_blocks match_blocks names_blocks] =  regexp(cleantext, pattern_objects, 'tokens', 'match', 'names', 'lineanchors');
  % this is slow!
  names_blocks = ScalarStructureToStructArray(names_blocks);
else
  [tokens_blocks match_blocks names_blocks] =  regexp(cleantext, pattern_objects, 'tokens', 'match', 'names', 'lineanchors', 'warnings');
end

i=1;

[entries, FDTDobj] = GEO_INP_reader({'block.geo'});
[entries, FDTDobj] = GEO_INP_reader({'boundary.inp'});
[entries, FDTDobj] = GEO_INP_reader({'box.geo'});
[entries, FDTDobj] = GEO_INP_reader({'cylinder.geo'});
[entries, FDTDobj] = GEO_INP_reader({'excitation.inp'});
[entries, FDTDobj] = GEO_INP_reader({'flag.inp'});
[entries, FDTDobj] = GEO_INP_reader({'fsnap.inp'});
[entries, FDTDobj] = GEO_INP_reader({'probe.inp'});
[entries, FDTDobj] = GEO_INP_reader({'rotation.geo'});
[entries, FDTDobj] = GEO_INP_reader({'sphere.geo'});
[entries, FDTDobj] = GEO_INP_reader({'tsnap.inp'});
[entries, FDTDobj] = GEO_INP_reader({'mesh.inp'});

[entries, FDTDobj] = GEO_INP_reader({'sim.inp','sim.geo', 'block.geo', 'box.geo', 'cylinder.geo', 'rotation.geo', 'sphere.geo'});

[entries, FDTDobj] = BFDTDtoMEEP({'sim.inp', 'sphere.geo', 'sim.geo', 'block.geo', 'box.geo', 'cylinder.geo', 'rotation.geo', 'sphere.geo'});
