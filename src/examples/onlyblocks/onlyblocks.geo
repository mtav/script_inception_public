**GEOMETRY FILE

BLOCK **name=block
{
1.000000E+00 **XL
0.000000E+00 **YL
1.000000E+00 **ZL
2.000000E+00 **XU
1.000000E+00 **YU
2.000000E+00 **ZU
1.000000E+00 **relative Permittivity
0.000000E+00 **Conductivity
}

BLOCK **name=block
{
0.000000E+00 **XL
1.000000E+00 **YL
1.000000E+00 **ZL
1.000000E+00 **XU
2.000000E+00 **YU
2.000000E+00 **ZU
1.000000E+00 **relative Permittivity
0.000000E+00 **Conductivity
}

BLOCK **name=block
{
1.000000E+00 **XL
2.000000E+00 **YL
1.000000E+00 **ZL
2.000000E+00 **XU
3.000000E+00 **YU
2.000000E+00 **ZU
1.000000E+00 **relative Permittivity
0.000000E+00 **Conductivity
}

BLOCK **name=block
{
2.000000E+00 **XL
1.000000E+00 **YL
1.000000E+00 **ZL
3.000000E+00 **XU
2.000000E+00 **YU
2.000000E+00 **ZU
1.000000E+00 **relative Permittivity
0.000000E+00 **Conductivity
}

BLOCK **name=block
{
1.000000E+00 **XL
1.000000E+00 **YL
0.000000E+00 **ZL
2.000000E+00 **XU
2.000000E+00 **YU
1.000000E+00 **ZU
1.000000E+00 **relative Permittivity
0.000000E+00 **Conductivity
}

BLOCK **name=block
{
1.000000E+00 **XL
1.000000E+00 **YL
2.000000E+00 **ZL
2.000000E+00 **XU
2.000000E+00 **YU
3.000000E+00 **ZU
1.000000E+00 **relative Permittivity
0.000000E+00 **Conductivity
}

SPHERE  **name=sphere
{
1.500000E+00 **XC
1.500000E+00 **YC
3.500000E+00 **ZC
0.500000E+00 **outer_radius
0.000000E+00 **inner_radius
1.000000E+00 **permittivity
0.000000E+00 **conductivity
}

SPHERE  **name=sphere
{
1.500000E+00 **XC
1.500000E+00 **YC
5.000000E+00 **ZC
1.000000E+00 **outer_radius
0.000000E+00 **inner_radius
2.000000E+00 **permittivity
0.000000E+00 **conductivity
}

SPHERE  **name=sphere
{
1.500000E+00 **XC
1.500000E+00 **YC
7.500000E+00 **ZC
1.500000E+00 **outer_radius
0.000000E+00 **inner_radius
3.000000E+00 **permittivity
0.000000E+00 **conductivity
}

CYLINDER **name=cylinder
{
4.5 **X CENTRE
1.5 **Y CENTRE
0.5 **Z CENTRE
0.000000E+00 **inner_radius
0.5 **outer_radius
1 **HEIGHT
0.000000E+00 **Permittivity
0.000000E+00 **Conductivity
0.000000E+00 **Angle of rotation in degrees around -Z=(0,0,-1)
}

CYLINDER **name=cylinder
{
7.5 **X CENTRE
1.5 **Y CENTRE
1 **Z CENTRE
0.000000E+00 **inner_radius
1 **outer_radius
2 **HEIGHT
0.000000E+00 **Permittivity
0.000000E+00 **Conductivity
0.000000E+00 **Angle of rotation in degrees around -Z=(0,0,-1)
}

CYLINDER **name=cylinder
{
10.5 **X CENTRE
1.5 **Y CENTRE
1.5 **Z CENTRE
0.000000E+00 **inner_radius
1.5 **outer_radius
3 **HEIGHT
0.000000E+00 **Permittivity
0.000000E+00 **Conductivity
0.000000E+00 **Angle of rotation in degrees around -Z=(0,0,-1)
}

BOX  **name=box
{
0.000000E+00 **XL
0.000000E+00 **YL
0.000000E+00 **ZL
12 **XU
3.000000E+00 **YU
9.000000E+00 **ZU
}

end
