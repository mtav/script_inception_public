close all;
clear all;

% load image
cd('~/Development/script_inception_public/src/FIB/imageToStreamfile');
%BW = not(imbinarize(imread('BW.bmp')));
%BW = not(imbinarize(imread('BW_CBD.bmp')));
%BW = imbinarize(imread('BW_CBD_inverted.bmp'));
%BW = not(imbinarize(imread('BW2.bmp')));
%BW = not(imbinarize(rgb2gray(imread('RGB.bmp'))));

%BW = imbinarize(imread('CBD.png'));
BW = imbinarize(imread('CBD_1024x884.png'));

figure;
imshow(double(BW));
title('original');

%%%%%%%%%%%%%%%%%%%%%%
beamStep = 1;
scanType = 'oneway';
scanDir = 'h';

[x, y] = imageToStreamfile1(BW, scanType, scanDir, beamStep);
figure;
plotFIBstream(x, y);
title('imageToStreamfile1');

%%%%%%%%%%%%%%%%%%%%%%
[x, y, dwell] = imageToStreamfile2(BW);
figure;
plotFIBstream(x, y, dwell);
title('imageToStreamfile2');

%%%%%%%%%%%%%%%%%%%%%%
beamStep = 1;
direction = 0;
etchType = 'fine';
param0 = 0;

[x, y] = imageToEtchPath(BW, beamStep, direction, etchType, param0);
figure;
plotFIBstream(x, y);
title('imageToEtchPath');
