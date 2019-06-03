close all;

delta_0 = 1;
delta_max = 1.2;
ratio_max = 1.01;
Delta_X = 2.45;
err = 1e-9;

[ratio_max, Delta_X] = meshgrid(linspace(1.01, 1.25), linspace(2, 5));
Z = -1*ones(size(ratio_max));
Zpass = -1*ones(size(ratio_max));

for i = 1:size(ratio_max,1)
  for j = 1:size(ratio_max,2)
    %Z(i,j) = ratio_max(i,j) + Delta_X(i,j);
    [mymesh, solution_id] = solveUpUpCase(delta_0, delta_max, ratio_max(i,j), Delta_X(i,j), err);
    Z(i,j) = solution_id;
    
    check_results = checkMeshUpUp(mymesh, delta_0, delta_max, ratio_max(i,j), Delta_X(i,j), err);
    Zpass(i,j) = check_results.required.pass;
    
    %if solution_id == 7
      %delta_0
      %delta_max
      %ratio_max(i,j)
      %Delta_X(i,j)
      %err
      %error('FOUND ONE')
    %end
    
    check_results.required.pass
  end
end

%check_results = checkMeshUpUp(mymesh, delta_0, delta_max, ratio_max, Delta_X, err)

figure;
surf(ratio_max, Delta_X, Z);
xlabel('ratio_max');
ylabel('Delta_X');
zlabel('solution_id');
view(0,90);
colorbar();

figure;
hist(Z(:), 0:9);
xlabel('solution_id');
ylabel('counts');

figure;
surf(ratio_max, Delta_X, Zpass);
xlabel('ratio_max');
ylabel('Delta_X');
zlabel('pass');
view(0,90);
colorbar();

figure;
hist(Zpass(:), 0:1);
xlabel('pass');
ylabel('counts');

disp('Z values:');
unique(Z(:))
disp('Zpass values:');
unique(Zpass(:))
