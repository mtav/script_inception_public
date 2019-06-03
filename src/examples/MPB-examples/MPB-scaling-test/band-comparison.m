% create a figure to compare bands
file1 = 'MPB-scaling-test_lattice_basis_size-1_lattice_size-1_scale-3.out.dat'
file2 = 'MPB-scaling-test_lattice_basis_size-1_lattice_size-3_scale-1.out.dat'
[ h1, d1 ] = readPrnFile(file1);
[ h2, d2 ] = readPrnFile(file2);
x = d1(:,2);
y1 = d1(:,6:end)/3;
y2 = d2(:,6:end);
A = 'lattice size = 1, scale = 3 (bands/3)';
B = 'lattice size = 3, scale = 1';
figure; hold on; p1=plot(x,y1,'b.'); p2=plot(x,y2,'r-'); legend([p1(1),p2(1)], A, B);

% TODO: How to get this to work? i.e. disabling the latex interpreter for the legend entries. Or an easy way to add escape sequences to text?
% figure; hold on; p1=plot(x,y1,'b.'); p2=plot(x,y2,'r-'); legend([p1(1),p2(1)], {file1, file2}, 'Interpreter', 'none');

title('band comparison for two simulations with same total number of layers, but different lattice values');
saveas(gcf, 'comparison','png');
