A = rand(3,4,5,6,7);

Ntot = length(A(:));

for lin_idx = 1:Ntot
  [c1,c2,c3,c4,c5] = ind2sub(size(A), lin_idx);
  c = [c1,c2,c3,c4,c5];
  g = ind2sub_array(size(A), lin_idx);
  c = c(:);
  g = g(:);
  if c ~= g
    c - g
    error('FAIL');
  end
end

M = 1:Ntot;
[c1,c2,c3,c4,c5] = ind2sub(size(A), M);
c = cat(ndims(c1)+1, c1, c2, c3, c4, c5);
g = ind2sub_array(size(A), M);
if c ~= g
  c - g
  error('FAIL');
end

M=M';
[c1,c2,c3,c4,c5] = ind2sub(size(A), M);
c = cat(ndims(c1)+1, c1, c2, c3, c4, c5);
g = ind2sub_array(size(A), M);
if c ~= g
  c - g
  error('FAIL');
end

M=reshape(1:Ntot, 3, []);
[c1,c2,c3,c4,c5] = ind2sub(size(A), M);
c = cat(ndims(c1)+1, c1, c2, c3, c4, c5);
g = ind2sub_array(size(A), M);
if c ~= g
  c - g
  error('FAIL');
end

M=reshape(1:Ntot, 3, 4, []);
[c1,c2,c3,c4,c5] = ind2sub(size(A), M);
c = cat(ndims(c1)+1, c1, c2, c3, c4, c5);
g = ind2sub_array(size(A), M);
if c ~= g
  c - g
  error('FAIL');
end

M=reshape(1:Ntot, 3, 4, 5, []);
[c1,c2,c3,c4,c5] = ind2sub(size(A), M);
c = cat(ndims(c1)+1, c1, c2, c3, c4, c5);
g = ind2sub_array(size(A), M);
if c ~= g
  c - g
  error('FAIL');
end

M=reshape(1:Ntot, 3, 4, 5, 6, []);
[c1,c2,c3,c4,c5] = ind2sub(size(A), M);
c = cat(ndims(c1)+1, c1, c2, c3, c4, c5);
g = ind2sub_array(size(A), M);
if c ~= g
  c - g
  error('FAIL');
end

M=reshape(1:Ntot, 3, 4, 5, 6, 7);
[c1,c2,c3,c4,c5] = ind2sub(size(A), M);
c = cat(ndims(c1)+1, c1, c2, c3, c4, c5);
g = ind2sub_array(size(A), M);
if c ~= g
  c - g
  error('FAIL');
end

%for idx = 1:5
  %c1
  %g()
%end

%size(c)
%size(g)

%M = reshape(1:Ntot, 3, []);
