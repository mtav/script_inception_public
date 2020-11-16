function theta_deg = grating_calibration_line(m, NA, n, lambda_um, a_um)
    theta_rad = asin((NA/n)-(m*lambda_um/a_um));
    theta_deg = rad2deg(theta_rad);
    theta_deg = real(theta_deg); % to avoid imaginary part warnings when plotting
end
