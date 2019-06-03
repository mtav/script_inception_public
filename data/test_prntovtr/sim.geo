**GEOMETRY FILE

CYLINDER **name=Cylinder
{
5.000000E-01 **X centro
5.000000E-01 **Y centro
5.000000E-01 **Z centro
0.000000E+00 **inner_radius
1.000000E-01 **outer_radius
5.000000E-01 **height
4.000000E+00 **relative permittivity -> n=sqrt(mu_r*epsilon_r)=2.00
0.000000E+00 **relative conductivity
0.000000E+00 **angle of rotation in degrees around -Z=(0,0,-1)
}

ROTATION **name=Cylinder_rotation
{
5.000000E-01 **X axis_point
5.000000E-01 **Y axis_point
5.000000E-01 **Z axis_point
1.000000E+00 **X axis_direction
0.000000E+00 **Y axis_direction
-1.000000E+00 **Z axis_direction
5.473561E+01 **angle_degrees
}

BOX  **name=box
{
0.000000E+00 **XL
0.000000E+00 **YL
0.000000E+00 **ZL
1.000000E+00 **XU
1.000000E+00 **YU
1.000000E+00 **ZU
}

end
