close all;
%  for s=1:4
%    cmd = ['./MPB-scaling-test.sh ', num2str(s)];
%    system(cmd);
%    name=['MPB-scaling-test_scale-',num2str(s)]
%    plot_MPB([name, '.out.dat']);
%    hline(((n1+n2)*s)/(4*n1*n2));
%    saveas(gcf, name, 'png');
%  end

lattice_basis_size = 1

for scaling_factor = [1,2,3,4]
  for lattice_size = [1,3,5]
    name = ['MPB-scaling-test_lattice_basis_size-', num2str(lattice_basis_size), '_lattice_size-', num2str(lattice_size), '_scale-', num2str(scaling_factor)]
    OUTFILE = [name, '.out']
    cmd = ['mpb scaling_factor=', num2str(scaling_factor), ' lattice_size=', num2str(lattice_size), ' MPB-scaling-test.ctl | tee ', OUTFILE]
    system(cmd)
    cmd = ['postprocess_mpb.sh ', OUTFILE]
    system(cmd)
    plot_MPB([name, '.out.dat']);
    v = ((n1+n2)/(4*n1*n2))*(scaling_factor/lattice_basis_size)
    dv = v*(4/pi)*(asin((n2-n1)/(n1+n2)));
    [v, dv]
    hline(v, 'r--');
    hline(v-dv/2, 'b--');
    hline(v+dv/2, 'b--');
    axis([0,25,0,2]);
    saveas(gcf, name, 'png');
  end
end
