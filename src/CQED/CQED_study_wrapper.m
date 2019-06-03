function CQED_study_wrapper(gamma, g, omega0, delta_omega, Q_peaks, Q_spectra, filebasename)
  ret_peaks = CQED_study(gamma, g, omega0, delta_omega, Q_peaks);
  ret_spectra = CQED_study(gamma, g, omega0, delta_omega, Q_spectra);

  Hz_to_meV = get_hb()/(1e-3*get_eV()); % to convert angular frequencies (omega) from Hz to meV

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%% plotting

  figure;
  
  subplot(2,2,1); hold on;
  plot(Q_peaks, ret_peaks.delta_omega_p_real_meV, 'b-');
  plot(Q_peaks, ret_peaks.delta_omega_n_real_meV, 'r-');
  plot(Q_spectra, ret_spectra.delta_omega_p_real_meV, 'bo');
  plot(Q_spectra, ret_spectra.delta_omega_n_real_meV, 'rx');
  xlabel('Quality factor Q');
  ylabel('Re(\omega)-\omega_0 (meV)');
  vline(ret_peaks.Q_lim1, 'r--');
  vline(ret_peaks.Q_lim2, 'g--');
  vline(ret_peaks.Q_lim3, 'b--');

  subplot(2,2,3); hold on;
  plot(Q_peaks, ret_peaks.delta_omega_p_imag_meV, 'b-');
  plot(Q_peaks, ret_peaks.delta_omega_n_imag_meV, 'r-');
  plot(Q_spectra, ret_spectra.delta_omega_p_imag_meV, 'bo');
  plot(Q_spectra, ret_spectra.delta_omega_n_imag_meV, 'rx');
  plot(Q_peaks, ret_peaks.gamma_meV, 'k--');
  plot(Q_peaks, ret_peaks.kappa_meV, 'k--');
  
  Purcell_slope = (4*g^2/omega0)*Hz_to_meV;
  Purcell_x0 = Q_spectra(1);
  Purcell_y0 = ret_spectra.delta_omega_p_imag_meV(1);

  plot(Q_peaks, Purcell_slope*(Q_peaks-Purcell_x0) + Purcell_y0);
  
  mini = min(ret_peaks.delta_omega_p_imag_meV(:));
  maxi = max(ret_peaks.delta_omega_p_imag_meV(:));
  d = maxi - mini;
  ylim_omega_imag_plot = [mini-d, maxi+2*d];
  ylim(ylim_omega_imag_plot);
  xlabel('Quality factor Q');
  ylabel('-2 Im(\omega) (meV)');
  vline(ret_peaks.Q_lim1, 'r--');
  vline(ret_peaks.Q_lim2, 'g--');
  vline(ret_peaks.Q_lim3, 'b--');

  subplot(2,2,2); hold on;
  surf(ret_peaks.grid_delta_omega_meV, ret_peaks.grid_Q, ret_peaks.grid_S_Andreani_normalized_by_area);
  xlabel('\Delta \omega (meV)');
  ylabel('Quality factor Q');
  zlabel('S (a.u.)');
  
  subplot(2,2,4); hold all;
  x = ret_spectra.grid_delta_omega_meV(1, :);
  x = x(:);
  y = ret_spectra.grid_S_Andreani_normalized_by_area';
  plot(x, y);
  xlabel('\Delta \omega (meV)');
  ylabel('S (a.u.)');
  
  CQED_spectra_header = {'delta_omega_meV'};
  CQED_spectra_header_tex = {'deltaomegameV'};
  for idx = 1:ret_spectra.N_Q
    CQED_spectra_header{end+1} = sprintf('Q=%E', ret_spectra.grid_Q(idx, 1));
    CQED_spectra_header_tex{end+1} = sprintf('S%d', idx);
  end
  legend(CQED_spectra_header{2:end}, 'location', 'eastoutside');
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%% info
  fprintf('Q_lim1 = %E\n', ret_peaks.Q_lim1);
  fprintf('Q_lim2 = %E\n', ret_peaks.Q_lim2);
  fprintf('Q_lim3 = %E\n', ret_peaks.Q_lim3);
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%% store data
  
  CQED_peaks_header = {'Q', 'delta_omega_p_real_meV', 'delta_omega_p_imag_meV', 'delta_omega_n_real_meV', 'delta_omega_n_imag_meV', 'gamma_meV', 'kappa_meV'};
  CQED_peaks_header_tex = {'Q', 'deltaomegaprealmeV', 'deltaomegapimagmeV', 'deltaomeganrealmeV', 'deltaomeganimagmeV', 'gammameV', 'kappameV'};
  
  CQED_peaks_data = [Q_peaks(:), ret_peaks.delta_omega_p_real_meV(:), ret_peaks.delta_omega_p_imag_meV(:), ret_peaks.delta_omega_n_real_meV(:), ret_peaks.delta_omega_n_imag_meV(:), ret_peaks.gamma_meV(:), ret_peaks.kappa_meV(:)];
  writePrnFile([filebasename, '.CQED_peaks.csv'], CQED_peaks_header_tex, CQED_peaks_data, 'delimiter', ';');
  
  CQED_peaks_markers_data = [Q_spectra(:), ret_spectra.delta_omega_p_real_meV(:), ret_spectra.delta_omega_p_imag_meV(:), ret_spectra.delta_omega_n_real_meV(:), ret_spectra.delta_omega_n_imag_meV(:), ret_spectra.gamma_meV(:), ret_spectra.kappa_meV(:)];
  writePrnFile([filebasename, '.CQED_peaks_markers.csv'], CQED_peaks_header_tex, CQED_peaks_markers_data, 'delimiter', ';');
  
  CQED_spectra_data = [x, y];
%    size(CQED_spectra_header)
%    size(CQED_spectra_data)
  writePrnFile([filebasename, '.CQED_spectra.csv'], CQED_spectra_header_tex, CQED_spectra_data, 'delimiter', ';');
  
  % TODO: make work for any number of Q_spectra values (not just 6, even skip if 0)
  
  CQED_info_header = {'gamma', 'g', 'omega0', 'Qlim1', 'Qlim2', 'Qlim3', 'yminOmegaImagPlot', 'ymaxOmegaImagPlot', 'gammameV', 'Qa', 'Qb', 'Qc', 'Qd', 'Qe', 'Qf', 'PurcellSlope', 'PurcellX0', 'PurcellY0'};
  CQED_info_data = [gamma, g, omega0, ret_peaks.Q_lim1, ret_peaks.Q_lim2, ret_peaks.Q_lim3, ylim_omega_imag_plot(1), ylim_omega_imag_plot(2), gamma*Hz_to_meV, Q_spectra(:)', Purcell_slope, Purcell_x0, Purcell_y0];
  writePrnFile([filebasename, '.CQED_info.csv'], CQED_info_header, CQED_info_data, 'delimiter', ';');
  
  f = fopen([filebasename, '.CQED_info.formatted.csv'], 'w');
  fprintf(f, 'Qa;Qb;Qc;Qd;Qe;Qf\n');
  fprintf(f, '%d;%d;%d;%d;%d;%d\n', round(Q_spectra(:))');
  fclose(f);
%    size(x)
%    size(y)
%    huhuh
%    x = ret_spectra.grid_delta_omega_meV(idx, :);
%    y = ret_spectra.grid_S_Andreani_normalized_by_area';
%    size(y)
%    gygyg
%    for idx = 1:ret_spectra.N_Q
%      y = ret_spectra.grid_S_Andreani_normalized_by_area';
%      [x(:),]
%    end
  
%    dlmwrite([filebasename, '.CQED_peaks.csv'], CQED_peaks,'delimiter',';');
%    dlmwrite([filebasename, '.CQED_spectrum.csv'], CQED_spectrum,'delimiter',';');
  
end
