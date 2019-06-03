function [freq, decay] = harminv_generateModes(K, freq_min, freq_max, decay_min, decay_max)
  freq = (freq_max - freq_min)*rand(K,1) + freq_min;
  decay = (decay_max - decay_min)*rand(K,1) + decay_min;
end
