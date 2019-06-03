diffuse_color = [0.8984394073486328, 1.0, 0.3113873600959778];
diffuse_intensity = 0.800000011920929;

diffuse_color_picked = [152,160,94]/255;

specular_color = [1.0, 1.0, 1.0];
specular_intensity = 0.5;

p = findobj(gca, 'type', 'Area');
p.FaceColor=diffuse_color_picked;
pbaspect([1 1 1]);
