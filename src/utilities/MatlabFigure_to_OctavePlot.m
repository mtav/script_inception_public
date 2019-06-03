function [header, data] = MatlabFigure_to_OctavePlot(filename)
  % Extracts data from Matlab .fig files and creates corresponding plots in GNU Octave + Saves them to .csv files.
  % Tested successfully on simple 2D plots with multiple lines.
  %
  % Note: scipy.io.loadmat() could be used to do the same from Python.
  %
  % TODO: If both Octave and Python can read .fig files, why is there still no open-source viewer for them?! :(
  
  all_data = load(filename);
  A = all_data.hgS_070000.children;
  B = A(1).children
  line_idx_list = [];
  line_idx_list_name = {};
  for idx=1:size(B,1)
    disp([num2str(idx),' : ', B(idx).type]);
    if strcmp(B(idx).type,'graph2d.lineseries')
      line_idx_list_name{end+1} = B(idx).properties.DisplayName;
      line_idx_list(end+1) = idx;
    end
  end
  
  N = 0;
  
  for idx = line_idx_list
    X = B(idx).properties.XData;
    Y = B(idx).properties.YData;
    X = X(:);
    Y = Y(:);
    if size(Y, 1) > N
      N = size(Y, 1);
    end
  end

  Nplots = length(line_idx_list);
  
  X_mat = NaN*ones(N, Nplots);
  Y_mat = NaN*ones(N, Nplots);
  data = NaN*ones(N, 2*Nplots);
  header = {};

  for idx = 1:Nplots
    line_idx = line_idx_list(idx);
    X = B(line_idx).properties.XData;
    Y = B(line_idx).properties.YData;
    X = X(:);
    Y = Y(:);
    
    X_mat(1:size(X,1), idx) = X;
    Y_mat(1:size(Y,1), idx) = Y;
    data(1:size(X,1), 2*idx-1) = X;
    data(1:size(Y,1), 2*idx) = Y;
    header{2*idx-1} = [line_idx_list_name{idx},' X'];
    header{2*idx} = [line_idx_list_name{idx},' Y'];
  end

  % show plot
  figure;
  semilogy(X_mat, Y_mat);
  legend(line_idx_list_name);
  title(filename);

  % save data to .csv file
  csvfile = [basename(filename, '.fig'), '.csv'];
  writePrnFile(csvfile, header, data, 'delimiter', ',', 'precision', 6);

end
