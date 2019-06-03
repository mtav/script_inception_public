function saveas_fig_and_png_tight(fig, outfile)
	figure(fig);
	
	ax = gca;
	outerpos = ax.OuterPosition;
	ti = ax.TightInset; 
	left = outerpos(1) + ti(1);
	bottom = outerpos(2) + ti(2);
	ax_width = outerpos(3) - ti(1) - ti(3);
	ax_height = outerpos(4) - ti(2) - ti(4);
	ax.Position = [left bottom ax_width ax_height];

	fig = gcf;
	fig.PaperPositionMode = 'auto';
	fig_pos = fig.PaperPosition;
	fig.PaperSize = [fig_pos(3) fig_pos(4)];

	savefig(fig, [outfile, '.fig']);
	print(fig, outfile, '-dpng');
end
