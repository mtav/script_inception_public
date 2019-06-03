% examples for the various *fun functions

% arrayfun
% Apply function to each element of array
% [B1,...,Bm] = arrayfun(func,A1,...,An)
% [B1,...,Bm] = arrayfun(func,A1,...,An,Name,Value)
A = [1,2,3]
B = arrayfun(@(x) x^2, A)

% cellfun
% Apply function to each cell in cell array
% [A1,...,Am] = cellfun(func,C1,...,Cn)
% [A1,...,Am] = cellfun(func,C1,...,Cn,Name,Value)
days = {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'}
abbrev = cellfun(@(x) x(1:3), days, 'UniformOutput', false)

% spfun
% Apply function to nonzero sparse matrix elements
% f = spfun(fun,S)
S = spdiags([1:4]',0,4,4)
f = spfun(@(x) x.^3, S)

% structfun
% Apply function to each field of scalar structure
% [A1,...,An] = structfun(func,S)
% [A1,...,An] = structfun(func,S,Name,Value)
s = struct();
s.f1 = 'Sunday';
s.f2 = 'Monday';
s.f3 = 'Tuesday'; 
s.f4 = 'Wednesday';
s.f5 = 'Thursday';
s.f6 = 'Friday';
s.f7 = 'Saturday';
s
lengths = structfun(@numel, s)

abbrev = filefun(@(x) ['==> ',x,' <=='], 'fun_examples.in', 'UniformOutput', false)
