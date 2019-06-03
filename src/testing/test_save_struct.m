function ret = test_save_struct()
  ret = struct();
  ret.a = 1;
  ret.b = 'b';
  ret.custom_function = @(x) max([1,2,3,x]);
  %save('ret.struct', 'ret');
  
  %saveable_ret = ret;
  %saveable_ret.custom_function = 'cannot be saved';
  
  saveable_ret = rmfield(ret, 'custom_function');
  
  %save('saveable_ret.struct', 'saveable_ret');
  save('-mat7-binary', 'saveable_ret.struct', 'saveable_ret');
  
end
