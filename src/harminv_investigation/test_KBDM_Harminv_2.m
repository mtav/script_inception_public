Nmodes = 3

d0 = rand()
d1 = rand()
d2 = rand()

w0 = rand()
w1 = rand()
w2 = rand()

input_values = [[-angle(exp(-w0*i)), d0];
[-angle(exp(-w1*i)), d1];
[-angle(exp(-w2*i)), d2]];

input_values = sortrows(input_values);

FunkyFunction = @(t) myfunc2(t, d0, d1, d2, w0, w1, w2);

K = 12
c = zeros(1,K);
for t = 0:K-1
  c(t+1) = FunkyFunction(t);
end
%c

output_values = KBDM_Harminv(c);

disp('Input (w,d) pairs:');
input_values

disp('Output (w,d) pairs:');
output_values

disp('output_values - input_values');
output_values(1:size(input_values,1), 1:size(input_values,2)) - input_values
