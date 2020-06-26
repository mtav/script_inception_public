**GEOMETRY FILE

BLOCK **Block Definition (XL,YL,ZL,XU,YU,ZU)
{
** "id" **ID CHARACTER (ALWAYS USE QUOTES)
** "id"
0.000000E+000 **XL
18.000000E+000 **ghgh}
** dgashgdja
0
1
2
1
2
2
}

**GEOMETRY FILE

BLOCK **Block Definition (XL,YL,ZL,XU,YU,ZU)
{
** "id" **ID CHARACTER (ALWAYS USE QUOTES) 
** "id"
0.000000E+000 **XL
18.000000E+000 **ghgh}
** dgashgdja
0
1
2
1
2
2
}


CYLINDER 
{
2.002244E+000 **X CENTRE
8.120000E-001 **Y CENTRE
2.002244E+000 **Z CENTRE
0.000000E+000 **RADIUS 1
1.000000E+000 **RADIUS 2
6.400000E-002 **HEIGHT
1.239744E+001 **Permittivity
0.000000E+000}

CYLINDER **Cylinder Definition (XL,YL,ZL,XU,YU,ZU,R1,R2)
{
2.002244E+000 **X CENTRE
8.976000E+000 **Y CENTRE
2.002244E+000 **Z CENTRE
0.000000E+000 **RADIUS 1
1.000000E+000 **RADIUS 2
6.400000E-002 **HEIGHT
1.239744E+001 **Permittivity
0.000000E+000 **Conductivity
}

SPHERE  **name=Sphere defect
{
-0.1 **XC
-0.2 **YC
-0.3 **ZC
2 **outer_radius
0.000000E+00 **inner_radius
1.000000E+00 **relative permittivity -> n=sqrt(mu_r*epsilon_r)=1.00
0.000000E+00 **relative conductivity
}

SPHERE  **name=s_1_2_3_1.5
{
1 **XC
2 **YC
3 **ZC
1.5 **outer_radius
0.000000E+00 **inner_radius
1.000000E+00 **relative permittivity -> n=sqrt(mu_r*epsilon_r)=1.00
0.000000E+00 **relative conductivity
}

SPHERE  **name=s_0_0_0_1
{
0 **XC
0 **YC
0 **ZC
1 **outer_radius
0.000000E+00 **inner_radius
1.000000E+00 **relative permittivity -> n=sqrt(mu_r*epsilon_r)=1.00
0.000000E+00 **relative conductivity
}

CYLINDER **name=Cylinder defect
{
0.000000E+00 **X centro
0.000000E+00 **Y centro
0.000000E+00 **Z centro
0.000000E+00 **inner_radius
5.000000E-01 **outer_radius
1.000000E+00 **height
1.000000E+00 **relative permittivity -> n=sqrt(mu_r*epsilon_r)=1.00
0.000000E+00 **relative conductivity
0.000000E+00 **angle of rotation in degrees around -Z=(0,0,-1)
}

BLOCK **name=Block defect
{
-5.000000E-01 **XL
-5.000000E-01 **YL
-5.000000E-01 **ZL
5.000000E-01 **XU
5.000000E-01 **YU
5.000000E-01 **ZU
1.000000E+00 **relative permittivity -> n=sqrt(mu_r*epsilon_r)=1.00
0.000000E+00 **relative conductivity
}

BOX  **BOX DEFINITION
{
0.000000E+000 **XL
0.000000E+000 **YL
0.000000E+000 **ZL
2.002244E+000 **XU
1.082595E+001 **YU
4.004487E+000 **ZU
}

end
