function plot_time_signal(fcen, df, sampling_time, resolution)
    % plot time signal and Fourier transform
    
    % example usage:
    % close all; clear all; fcen=0.123; df=0.1; sampling_time=1/fcen/20; resolution=10; plot_time_signal(fcen, df, sampling_time, resolution);

%     [FNAME, FPATH, FLTIDX] = uigetfile('*.h5', 'Select an HDF5 file.');
%     infile = fullfile(FPATH, FNAME); % 'time_signal-ez-source.h5';

    infile = 'time_signal-ez-source.h5';

    h5disp(infile);
    data = h5read(infile,'/ez');

%     fcen = 3.14; % frequency in MEEP units
    Tn = 1/fcen; % period in MEEP units
    % t = 10.0 (200 timesteps)
    %dt = 10/200;

    % The default timestep used in MEEP (in MEEP units) is dtn = 0.5/resolution.
    % See here for details: https://meep.readthedocs.io/en/latest/Introduction/#units-in-meep

    S = 0.5; % default Courant factor used in MEEP
%     resolution = 10; % resolution used in MEEP

    timestep = S/resolution;             % simulation timestep
    actual_sampling_time = max(timestep, sampling_time)
    
    Fs = 1/actual_sampling_time;            % Sampling frequency
    L = length(data);             % Length of signal
    t = (0:L-1)*actual_sampling_time;        % Time vector

    plotTimeAndFFT(t, data, fcen);

%%%%% enable these to check for undersampling:
%     data = sin(2*pi*fcen*t); % test run with a sinewave
%     plotTimeAndFFT(t, data, fcen);
%     
%     sigma = 20;
%     t0 = 50;
%     data = exp(-((t-t0)./sigma).^2).*sin(2*pi*fcen*t); % test run with gaussian modulated sinewave
%     plotTimeAndFFT(t, data, fcen);
end

function plotTimeAndFFT(t, data, fcen)

    actual_sampling_time = t(2) - t(1)
    Fs = 1/actual_sampling_time;            % Sampling frequency

    L = length(data);             % Length of signal

    length(data)
    length(t)

    Y = fft(data);

    P2 = abs(Y/L);
    P1 = P2(1:L/2+1);
    P1(2:end-1) = 2*P1(2:end-1);

    f = Fs*(0:(L/2))/L;

    disp('max time:');
    max(t)
    length(t)

    figure;
    subplot(1,2,1);
    plot(t, data, 'b.-');
    xlabel('Normalized time (MEEP units)');
    ylabel('Ez amplitude (a.u.)');
    
    subplot(1,2,2);
    plot(f,P1);
    xlabel('Normalized frequency a/\lambda (MEEP units)');
    ylabel('Amplitude (a.u.)');
    vline(fcen);

%     data_time_domain = data;
%     dt_mus = T;
%     [calcFFT_output, lambda_vec_mum, freq_vec_Mhz] = calcFFT(data_time_domain, dt_mus);
%     subplot(1,3,3);
%     plot(freq_vec_Mhz, calcFFT_output);
end
