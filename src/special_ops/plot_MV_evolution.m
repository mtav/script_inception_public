function plot_MV_evolution(result_list, titulo)
  % function plot_MV_evolution(result_list)
  %
  % Plots MV results vs the number of iterations.
  % The input should be a structured array of the form {ret1, ret2, ret3, ...} where the "ret" values are output from calculateModeVolume().
  % They should usually correspond to increasing "snap_time_number" values.
  %
  % TODO: Output data table again, but needs to deal with new MaximumEnergyDensity subvalues. + maybe save it?

  % create arrays for plotting
  Niterations=[]; for idx=1:length(result_list); Niterations(end+1) = result_list{idx}.Niterations; end;
  TotalEnergy=[]; for idx=1:length(result_list); TotalEnergy(end+1) = result_list{idx}.TotalEnergy; end;
  MaximumEnergyDensity=[]; for idx=1:length(result_list); MaximumEnergyDensity(end+1) = result_list{idx}.MaximumEnergyDensity.value; end;
  mode_volume_mum3=[]; for idx=1:length(result_list); mode_volume_mum3(end+1) = result_list{idx}.mode_volume_mum3; end;
  normalized_mode_volume_1=[]; for idx=1:length(result_list); normalized_mode_volume_1(end+1) = result_list{idx}.normalized_mode_volume_1; end;
  normalized_mode_volume_2=[]; for idx=1:length(result_list); normalized_mode_volume_2(end+1) = result_list{idx}.normalized_mode_volume_2; end;

%    timestep = 2.7849285878449524e-12;
%    time = Niterations*timestep;
%    Niterations
%    TotalEnergy
%    MaximumEnergyDensity.value
%    mode_volume_mum3
%    normalized_mode_volume_1
%    normalized_mode_volume_2

  fontsize=12;
  figure;
%    subplot(2,3,1);
%    plot(Niterations, time, 'b--s'); xlabel('Niterations', 'FontSize', fontsize); ylabel('time (\mus)', 'FontSize', fontsize);
  subplot(2,3,1);
  plot(Niterations, TotalEnergy, 'b--s'); xlabel('Niterations', 'FontSize', fontsize); ylabel('Total energy in studied volume (\propto J) = \int{\epsilon \cdot E^{2} dV}', 'FontSize', fontsize);
  title(titulo);

  subplot(2,3,2);
  plot(Niterations, MaximumEnergyDensity, 'b--s'); xlabel('Niterations', 'FontSize', fontsize); ylabel('Maximum energy density in studied volume (\propto J/m^3) = max(\epsilon \cdot E^{2})', 'FontSize', fontsize);
  title(titulo);

  subplot(2,3,3);
  plot(Niterations, mode_volume_mum3, 'b--s'); xlabel('Niterations', 'FontSize', fontsize); ylabel('mode volume V (\mum^3) = (total energy)/(maximum energy density)', 'FontSize', fontsize);
  title(titulo);

  subplot(2,3,4);
  plot(Niterations, normalized_mode_volume_1, 'b--s'); xlabel('Niterations', 'FontSize', fontsize); ylabel('normalized mode volume (no unit) V_{n1} = V / (lambda/n)^{3}', 'FontSize', fontsize);
  title(titulo);

  subplot(2,3,5);
  plot(Niterations, normalized_mode_volume_2, 'b--s'); xlabel('Niterations', 'FontSize', fontsize); ylabel('normalized mode volume (no unit) V_{n2} = V / (lambda/(2n))^{3}', 'FontSize', fontsize);
  title(titulo);


%    fields = fieldnames(result_list{1});
%    header = strjoin(fields','; ');
%  
%    Nrows = length(result_list);
%    Ncols = length(fields);
%  
%    data = zeros(Nrows, Ncols);
%  
%    for row = 1:Nrows
%      for col = 1:Ncols
%        data(row, col) = getfield(result_list{row}, char(fields(col)));
%      end
%    end
%    saveas_fig_and_png(gcf, titulo);
end
