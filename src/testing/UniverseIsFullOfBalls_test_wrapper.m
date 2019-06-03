close all;
clear all;

more off;

cd('~/TEST/MV-region-test/MV-region-test-energy-outside-1/UniverseIsFullOfBalls/Z/');
figure; UniverseIsFullOfBalls_test([2,2,2], 2, 1);
figure; UniverseIsFullOfBalls_test([5,2,2], 5, 1);
figure; UniverseIsFullOfBalls_test([8,2,2], 8, 1);

cd('~/TEST/MV-region-test/MV-region-test-energy-outside-0/UniverseIsFullOfBalls/Z/');
figure; UniverseIsFullOfBalls_test([2,2,2], 2, 0);
figure; UniverseIsFullOfBalls_test([5,2,2], 5, 0);
figure; UniverseIsFullOfBalls_test([8,2,2], 8, 0);
