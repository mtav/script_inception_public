import bpy
op = bpy.context.active_operator

op.equation = '(3*(1-x)**2)*exp(-(x**2) - (y+1)**2) - 10*(x/5 - x**3 - y**5)*exp(-x**2-y**2) - 1/3*exp(-(x+1)**2 - y**2)'
op.div_x = 49
op.div_y = 49
op.size_x = 6.0
op.size_y = 6.0
