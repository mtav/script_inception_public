%
% PROBE_FFT Calculate the FFT from probe file data.
%
% PROBE_FFT(number,'sim',start,col) performs FFT on multiple 
% data sets in standard University of Bristol probe file fo-
% rmats. The number of input files is defined by number.  The 
% appended letter on probe files is given by 'sim' (e.g. 'a').
% start tells the subroutine where to begin. Col defines the
% data on which to perform the FFT.
%
% An example function call for performing the FFT on the Ey data
% from 12 files from simulation run 'c' starting at the 15th 
% probe would be: PROBE_FFT(12,'c',15,3).  This would produce
% 12 files named in the form 'fft_Ey_p15.prn' to 'fft_Ey_p27.prn'.
% 
% Version 1, 28/11/2006. Ian Buss.

% The MIT License
%
% Copyright (c) 2009 Ian Buss
%
% Permission is hereby granted, free of charge, to any person obtaining a copy
% of this software and associated documentation files (the "Software"), to deal
% in the Software without restriction, including without limitation the rights
% to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
% copies of the Software, and to permit persons to whom the Software is
% furnished to do so, subject to the following conditions:
%
% The above copyright notice and this permission notice shall be included in
% all copies or substantial portions of the Software.
%
% THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
% IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
% FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
% AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
% LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
% OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
% THE SOFTWARE.

% TODO: Get rid of this. Should be same as calcFFT. Also check other probe_fft_* functions by Ian Buss.

function probe_fft(number,sim,start,col)
    %% Define columns
    data_cols = ['Ex';'Ey';'Ez';'Hx';'Hy';'Hz'];

    %% Calculate FFT for number files
    for ii=start:1:(number+start-1)
        %load in probe file data
        if ii<10
            file = ['p0',int2str(ii),sim,'.prn'];
        elseif ii>=10
            file = ['p',int2str(ii),sim,'.prn'];
        end
        [header,datain] = readPrnFile(file);
        
        [fft_out,lambda,freq] = calcFFT(datain(:,col), (datain(2,1)-datain(1,1))*1e-12);
        %calculate magnitude of fft
        y_mag = abs(fft_out);
        %calculate power of fft
        y_pow = fft_out.* conj(fft_out)/NFFT;
        
        % write output file
        titles = [' frequency ','wavelength ','fft_',data_cols((col-1),1:2),...
            '_mag fft_',data_cols((col-1),1:2),'_pow','\n'];
        outfile = ['fft_',data_cols((col-1),1:2),'_',file];
        fid = fopen(outfile,'w');
        fprintf(fid,titles);
        fclose(fid);
        out = cat(2,freq,lambda,y_mag,y_pow);
        save(outfile,'out','-append','-ascii');
    end
end
