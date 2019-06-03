function volume = blockVolume(block_structure)
  S = abs(block_structure.upper - block_structure.lower);
  volume = prod(S);
end
