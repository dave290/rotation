import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

fig=plt.figure(figsize=(10,6))
ax=plt.axes()

radius=[8,10,12,14,16]
velocity=[200,220,240,260,280]
yerr=[10,20,30,40,50]

ax.scatter(radius,velocity,c="red",s=100)
ax.errorbar(radius,velocity,yerr,linestyle='',color='red')
ax.set_title("Velocity vs Radius",fontsize=25)
ax.set_xlabel("Radius (kpc)",fontsize=18)
ax.set_xlim(2,18)
ax.set_xticks([2,4,6,8,10,12,14,16,18])
ax.set_ylabel("Velocity (km/s)",fontsize=18)
ax.set_ylim(0,400)
ax.set_yticks([0,50,100,150,200,250,300,350,400])
plt.grid()
plt.show()

exit()