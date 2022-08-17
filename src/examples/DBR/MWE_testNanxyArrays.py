import numpy as np
import matplotlib.pyplot as plt

# works
x = [1,2,3]
y = [4,5,6,7]
x,y=np.meshgrid(x,y)
z = x+y
plt.pcolormesh(x,y,z)

# fails
x = [1,2,3]
y = [4,5,np.nan,7]
x,y=np.meshgrid(x,y)
z = x+y
plt.pcolormesh(x,y,z)

# fails
x = [1,np.nan,3]
y = [4,5,6,7]
x,y=np.meshgrid(x,y)
z = x+y
plt.pcolormesh(x,y,z)

# https://stackoverflow.com/questions/36228363/dealing-with-masked-coordinate-arrays-in-pcolormesh
