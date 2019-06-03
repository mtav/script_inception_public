import bpy
op = bpy.context.active_operator

op.equation = '0.2*exp(-0.02*((x-5)**2+(y+20)**2))*cos(2*pi*sqrt((x-5)**2+(y+20)**2)*2)+0.2*exp(-0.02*((x+5)**2+(y+20)**2))*cos(2*pi*sqrt((x+5)**2+(y+20)**2)*2)'
op.div_x = 256
op.div_y = 256
op.size_x = 20.0
op.size_y = 10.0
