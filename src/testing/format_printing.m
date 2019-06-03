function format_printing(format, iterations, frequency)
  format = strrep(format, '%D', datestr(now,'yyyymmdd_HHMMSS'));
  format = strrep(format, '%I', num2str(iterations));
  format = strrep(format, '%F', num2str(frequency));
  format
  
  %regexp(string,expressn)
end
