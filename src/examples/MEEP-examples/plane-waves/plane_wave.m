% close all;
% clear all;
function plane_wave(angle_deg, lambda_n)
    % plot plane wave field at t=0 for a given wavevector k
    if ~exist('angle_deg', 'var')
        angle_deg = 45;
    end
    if ~exist('lambda_n', 'var')
        lambda_n = 1; % normalized wavelength
    end
    
    a = 1; % always 1 (m, nm, um, lattice constant, etc) in MEEP/MPB
    kdir = [cos(deg2rad(angle_deg)), sin(deg2rad(angle_deg))]; % wavevector direction
    k = (2*pi/(a*lambda_n))*kdir/norm(kdir); % wavevector
    % kn = (1/lambda_n)*kdir/norm(kdir); % normalized wavevector
    kx = dot(k,[1,0]);
    ky = dot(k,[0,1]);
    
    % xmin = -2;
    % xmax = 2;
    % ymin = -2;
    % ymax = 2;
    [X,Y] = meshgrid(linspace(-2,2), linspace(-2,2));
    Z = cos(kx.*X+ky.*Y);
    % surf(X,Y,Z, 'EdgeColor','none');
    h = pcolor(X,Y,Z);
    set(h, 'EdgeColor', 'none');
    view(2);
    xlabel('x/a');
    ylabel('y/a');
    title(sprintf('\\lambda/a=%.2f, \\theta=%.2f^\\circ', lambda_n, angle_deg));
    axis square;
    % axis equal;
    
    hold on;
    xmin = min(X(:));
    xmax = max(X(:));
    
    v = lambda_n*kdir/norm(kdir);
    plot([xmin, xmax], (ky/kx).*[xmin, xmax], 'r--');
    plot(v(1).*[-1/2, 1/2], v(2).*[-1/2, 1/2], 'k-', 'LineWidth', 2);
    % quiver(0, 1, v(1), v(2), 'off');
    % xline(-1:0.5:1);
    % yline(-1:0.5:1);
    % annotation('arrow',[0, 0],[1, 1]);
    % Annotate(gca, 'arrow', [0, 1], [0, 1]);
end
