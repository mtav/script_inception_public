function [wn_bot, wn_top, debug_info] = DBR_bands_getBandgap(n1, n2, t1, t2)
    % Calculates the photonic bandgap edges of a 1D DBR photonic crystal.

    a = t1+t2;
    midgap = a ./ ( 2*(n1 .* t1 + n2 .* t2) );
    N = 1;
    Ngaps = 3;
    Ninter = 100;
    linspace(0, Ngaps, (Ninter+1)*Ngaps+1)*midgap;
    wn = linspace(0, N*3*midgap, 100*N);
    k = DBR_bands(wn, n1, n2, t1, t2);
    K = real(k);
  
    botgap_found = false;
    topgap_found = false;
    botgap_idx = 1;
    for idx = 2:length(wn)
        if ~botgap_found
            if K(idx) > K(botgap_idx)
                botgap_idx = idx;
            else
                botgap_found = true;
                if K(idx) < K(botgap_idx)
                    topgap_idx = idx-1;
                    topgap_found = true;
                    break;
                end
            end
        else
            if K(idx) < K(botgap_idx)
                topgap_idx = idx-1;
                topgap_found = true;
                break;
            end
        end
    end
    
    if ~botgap_found || ~topgap_found
        error('Failed to find both gap edges: botgap_found=%d topgap_found=%d', botgap_found, topgap_found);
    end       

    wn_bot = wn(botgap_idx);
    wn_top = wn(topgap_idx);

    debug_info.k = k;
    debug_info.K = K;
    debug_info.wn = wn;
    debug_info.midgap = midgap;
    debug_info.edges.botgap_idx = botgap_idx;
    debug_info.edges.topgap_idx = topgap_idx;
    debug_info.edges.botgap_K = K(botgap_idx);
    debug_info.edges.topgap_K = K(topgap_idx);
    debug_info.edges.botgap_wn = wn(botgap_idx);
    debug_info.edges.topgap_wn = wn(topgap_idx);

end
