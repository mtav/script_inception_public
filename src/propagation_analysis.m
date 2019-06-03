function propagation_analysis(INFILENAME,AMPLITUDE,TIME_OFFSET,TIME_CONSTANT,FREQUENCY)

    %figure()

    % x=0.25;
    % delta=20*1/FREQUENCY;t=[TIME_OFFSET-delta/2:delta/100:TIME_OFFSET+delta/2];
    % t=t-x/get_c0();
    % plot(t+x/get_c0(),AMPLITUDE*exp(-log(2)*((t-TIME_OFFSET)/TIME_CONSTANT).^2).*sin(2*pi*FREQUENCY*t));
    % hold on;

    % x=10;
    % delta=20*1/FREQUENCY;t=[TIME_OFFSET-delta/2:delta/100:TIME_OFFSET+delta/2];
    % t=t-x/get_c0();
    % plot(t,AMPLITUDE*exp(-log(2)*((t-TIME_OFFSET)/TIME_CONSTANT).^2).*sin(2*pi*FREQUENCY*t));

    % x=20;
    % delta=20*1/FREQUENCY;t=[TIME_OFFSET-delta/2:delta/100:TIME_OFFSET+delta/2];
    % t=t-x/get_c0();
    % plot(t,AMPLITUDE*exp(-log(2)*((t-TIME_OFFSET)/TIME_CONSTANT).^2).*sin(2*pi*FREQUENCY*t));

    % x=30;
    % delta=20*1/FREQUENCY;t=[TIME_OFFSET-delta/2:delta/100:TIME_OFFSET+delta/2];
    % t=t-x/get_c0();
    % plot(t,AMPLITUDE*exp(-log(2)*((t-TIME_OFFSET)/TIME_CONSTANT).^2).*sin(2*pi*FREQUENCY*t));

    delta=20*1/FREQUENCY;
    t_init=[TIME_OFFSET-delta/2:delta/(100*20):TIME_OFFSET+delta/2];
    %hold on;
    % x=0;
    % t=t_init+x/get_c0();
    % plot(t,AMPLITUDE*exp(-log(2)*(((t-x/get_c0())-TIME_OFFSET)/TIME_CONSTANT).^2).*sin(2*pi*FREQUENCY*(t-x/get_c0())));
    % x=10;
    % toto(0);
    % toto(10);

    function plot_theory(x,style)
        fftfig = figure();
    
        %t = t_init+x/get_c0();
        %y = AMPLITUDE*exp(-log(2)*(((t-x/get_c0())-TIME_OFFSET)/TIME_CONSTANT).^2).*sin(2*pi*FREQUENCY*(t-x/get_c0()));
        
        delta = 20*1/FREQUENCY;
        t = [-delta/2:delta/(100*20):delta/2];
        alpha = log(2)/TIME_CONSTANT^2;        
        y = exp(-alpha*t.^2).*sin(2*pi*FREQUENCY*t);
        %y = exp(-alpha*t.^2);
        
        subplot(1,3,1)
        plot(t,y,style);
        
        %% FFT for frequency estimation
        Vfit = y;
        time_length = t(end)-t(1);
        sample_int = time_length/(length(t)-1);
        
        LV = length(Vfit);
        P = abs(fft(Vfit)); Ppos=P(1:(round(LV/2)+1));
        faxis = 1/sample_int*(0:round(LV/2))/LV;
        peakf = faxis(find(Ppos==max(P(1:(round(LV/2)+1)))));
        
        subplot(1,3,2);
        semilogy(faxis,Ppos,'-'); hold on;

        plot(peakf,max(Ppos),'dr');
        title('FFT'); xlabel('Frequency [Hz]'); ylabel('Power')
        fa=axis; text((fa(2)-fa(1))/2,(fa(4)-fa(3))/2,['f_0: ' num2str(peakf,'%.1f') ' MHz',' lambda: ' num2str(get_c0()/peakf,'%.1f') ' mum']);

        subplot(1,3,3);
        lambda = get_c0()./faxis;
        plot(lambda,Ppos,'bs'); hold on;
        
        %yfit = AMPLITUDE*0.5*sqrt(pi*TIME_CONSTANT^2/log(2))*exp(-(pi*(faxis-FREQUENCY)*TIME_CONSTANT).^2/log(2));
        %yfit = 0.5*sqrt(pi/alpha)*exp(-(pi*(faxis-FREQUENCY)).^2/alpha);
        yfit = max(Ppos)*exp(-(pi*(faxis-FREQUENCY)).^2/alpha);
        plot(lambda,yfit,'r-'); hold on;
        
        LV
        fit_max = 0.5*sqrt(pi/alpha)
        fft_max1 = max(P(1:(round(LV/2)+1)))
        fft_max2 = max(Ppos)
        alpha
        maxtheo = sqrt(pi/alpha)

    end
    
    function plot_simulation(file)
        [header, data] = readPrnFile(file);
        plot(data(:,1)*10^-12,data(:,2),'ko--');
    end

    plot_theory(0,'b-');
    
    %plot_simulation('p01id.prn');
    %plot_theory(0.25,'m-');
    
    %plot_simulation('p02id.prn');
    %plot_theory(10,'c-');
    
    %plot_simulation('p03id.prn');
    %plot_theory(20,'r-');
    
    %plot_simulation('p04id.prn');
    %plot_theory(30,'g-');
    
    %plot_simulation('p01id.prn');
    %plot_theory(40,'b-');

end

% function plot_probe_signal(INFILENAME,AMPLITUDE,TIME_OFFSET,TIME_CONSTANT,FREQUENCY,x)
    % delta=20*1/FREQUENCY;t=[TIME_OFFSET-delta/2:delta/100:TIME_OFFSET+delta/2];
    % t=t-x/get_c0();
    % plot(t,AMPLITUDE*exp(-log(2)*((t-TIME_OFFSET)/TIME_CONSTANT).^2).*sin(2*pi*FREQUENCY*t));
% end
