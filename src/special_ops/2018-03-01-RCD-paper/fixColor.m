diffuse_color = [0.8984394073486328, 1.0, 0.3113873600959778];
diffuse_intensity = 0.800000011920929;

diffuse_color_picked = [152,160,94]/255;

specular_color = [1.0, 1.0, 1.0];
specular_intensity = 0.5;

%material shiny;
%material dull;
%material metal;
%material default;

p = findobj(gca, 'type', 'Patch');
p3 = p(3);

%p3.FaceColor = diffuse_color;
p3.FaceColor = diffuse_color_picked;
p3.FaceAlpha = 0.5;

%p3.FaceLighting = 'flat';
p3.FaceLighting = 'gouraud';
%p3.FaceLighting = 'none';

p3.BackFaceLighting = 'reverselit';
%p3.BackFaceLighting = 'unlit';
%p3.BackFaceLighting = 'lit';

p3.LineStyle = 'none';

p3.AmbientStrength = 0.3000;

p3.DiffuseStrength = diffuse_intensity;

p3.SpecularStrength = specular_intensity;

p3.SpecularColorReflectance = 1;

p3.SpecularExponent = 10;

%view([1,0,0]);

delete(findall(gcf,'Type','light')); camlight('headlight');
%delete(findall(gcf,'Type','light')); camlight('right');
%delete(findall(gcf,'Type','light')); camlight('left');
