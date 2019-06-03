close all;
clear all;
locs = {'eastoutside', 'east', 'westoutside', 'west', 'northoutside', 'north', 'southoutside', 'south'};
for i = 1:length(locs)
  figure;
  title(locs{i});
  colorbarLabel(colorbar('location', locs{i}), 'foo_123', 'interpreter', 'none');
end
