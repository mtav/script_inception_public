close all;
clear all;

% load image

cd('~/Development/script_inception_public/src/FIB/imageToStreamfile');

[filename, pathname] = uigetfile({'*.png';'*.bmp';'*.jpg';'*.gif';'*.*'},'File Selector');
infile = fullfile(pathname, filename);

[filepath, name, ext] = fileparts(filename);

%name = 'CBD_1024x884_3mum';

%BW = imbinarize(imread('CBD_1024x884.png'));
%BW = flipud(imbinarize(imread(sprintf('%s.png', name))));
img = imread(infile);
if size(img, 3) > 1
  img = rgb2gray(img);
end
%BW = imbinarize(img);
BW = img;

figure;
subplot(1, 2, 1);
%imshow(flipud(double(BW))); % double conversion messes things up if contents are uint8
imshow(flipud(BW));
title('original');

[x, y, dwell] = imageToStreamfile2(BW);
%figure;
subplot(1, 2, 2);
plotFIBstream(x, y, dwell);
title('imageToStreamfile2');

rep = 1;
dwell_value = 7500;
mag = 5000;

prompt = {'repetition:', 'dwell time (if negative, use pixel values):', 'magnitude:'};
dlg_title = 'parameters';
num_lines = 1;
defaultans = {num2str(rep), num2str(dwell_value), num2str(mag)};
answer = inputdlg(prompt, dlg_title, num_lines, defaultans);

rep = str2num(answer{1});
dwell_value = str2num(answer{2});
mag = str2num(answer{3});

%if dwell_value > 0
  %dwell = dwell_value*ones(size(x));
%end

dwell = dwell_value*dwell/max(dwell(:));

outfile = sprintf('%s.rep-%d.dwell-%d.mag-%d.str', name, rep, dwell_value, mag);

writeStrFile(outfile, x, y, dwell, rep);

readStrFile(outfile, mag);
readStrFile(outfile);
