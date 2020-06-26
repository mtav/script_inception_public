**GEOMETRY FILE

BLOCK **name=substrate
{
0 **XL
0 **YL
0 **ZL
1 **XU
1 **YU
0.25 **ZU
100
0
}

ROTATION
{
0.5 **X CENTRE
0.5 **Y CENTRE
0.5 **Z CENTRE
1
0
0
30
}

CYLINDER **name=pillar
{
0.5 **X CENTRE
0.5 **Y CENTRE
0.625 **Z CENTRE
0 **INNER RADIUS
0.25 **OUTER RADIUS
0.75 **HEIGHT
3 **Permittivity
0 **Conductivity
}

ROTATION
{
0.5 **X CENTRE
0.5 **Y CENTRE
0.625 **Z CENTRE
1
0
0
90
}

ROTATION
{
0.5 **X CENTRE
0.5 **Y CENTRE
0.5 **Z CENTRE
1
0
0
30
}

BLOCK **name=step1
{
0.9
1.8
2.7
1.1
2.2
3.3
1
0
}

BLOCK **name=step2
{
0.9
1.8
2.7
1.1
2.2
3.3
4
0
}

ROTATION
{
3
2
1
1
0
0
30
}

BLOCK **name=step3
{
0.9
1.8
2.7
1.1
2.2
3.3
9
0
}

ROTATION
{
3
2
1
1
0
0
30
}

ROTATION
{
4
5
6
0
1
0
60
}

BOX  **BOX DEFINITION
{
0 **XL
0 **YL
0 **ZL
1 **XU
1 **YU
1 **ZU
}

end
