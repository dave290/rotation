#velocity.py
#calculates rotation curve using radio telescope doppler shift data
#user enters data into file called parameters.dat
#corrects for motion of sun toward apex in LSR
#modified 3/29/2023

import read_params
import math

radiustangent=[0];velocitytangent=[0]
radiussolar=[0];velocitysolar=[0]
radius=[0];velocity=[0]
vel_err_tan=[0];vel_err_chord=[0]

degtorad=3.14159/180.0
lytokpc=1/3260.0
pi=3.14159

#Read parameter file
#Program assumes that apex velocity is between 0 and 90 degrees galactic longitude
#Last line calculates apex velocity projected onto galactic plane
params=read_params.params()
solar_radius=float(params[0])
lsr_vel=float(params[1])
apex_alpha=degtorad*float(params[3])
apex_velocity=float(params[2])*math.cos(degtorad*float(params[4]))

#Determine number of tangent points and chord points
tangent_params=read_params.tangent_params()
NI=int((len(tangent_params))/3)  #total number of tangent points
chord_params=read_params.chord_params()
NO=int((len(chord_params))/4)  #total number of chord points

#Calculate velocities using tangent point method.  Inner points only.
for i in range(NI):
    gallon_rads=degtorad*float(tangent_params[i*3])
    vel_dop_shf=float(tangent_params[i*3+1])
    radiustangent.append(solar_radius*math.sin(gallon_rads))
    aaa=lsr_vel*math.sin(gallon_rads)
    apex_radial_vel=apex_velocity*math.cos(gallon_rads-apex_alpha)
    velocitytangent.append(vel_dop_shf+aaa+apex_radial_vel)
    vel_err_tan.append(float(tangent_params[i*3+2]))  
#next i
radiustangent.pop(0)
velocitytangent.pop(0)
vel_err_tan.pop(0)

#Sun
radiussolar.append(solar_radius)    
velocitysolar.append(lsr_vel)
radiussolar.pop(0)
velocitysolar.pop(0)

#Calculate velocities using chord method
#
#Inner points: (0-90 degrees) v-shift is positive (receding)
#Magnitude of LSR vel-shift is greater than magnitude of OBS vel-shift, by apex velocity component
#Note: When the line of sight intersects 2 points on the inside circle, both points give identical v-shifts
#
#Outer points: (0-145 degrees) v-shift is negative (approaching):
#Magnitude of LSR vel-shift is less than magnitude of OBS vel-shift, by apex velocity component
#
#Outer points: (145-180 degrees) v-shift is negative (approaching):
#Magnitude of LSR vel-shift is greater than magnitude of OBS vel-shift, by apex velocity component

for i in range(NO):
    j=int(chord_params[i*4])
    if j<180:
        gallon_rads=degtorad*float(chord_params[i*4])
        object_radius=lytokpc*float(chord_params[i*4+1])
        vel_dop_shf=float(chord_params[i*4+2])
        b5=gallon_rads
        b11=lsr_vel
        a8=object_radius
        b8=solar_radius
        beta=math.asin((b8/a8)*math.sin(b5))
        lsr_radial_vel=b11*math.sin(b5)
        phi=0.5*pi-beta
        apex_radial_vel=apex_velocity*math.cos(gallon_rads-apex_alpha) 
        #apex_radial_vel is POS for gallon<145 and NEG for gallon>145)
        object_vel=(lsr_radial_vel+vel_dop_shf+apex_radial_vel)/math.cos(phi)
        radius.append(object_radius)      
        velocity.append(object_vel)
        vel_err_chord.append(float(chord_params[i*4+3]))  
    #next i

#Outer points: (180-270 degrees) v-shift is positive (receding)
#Magnitude of LSR vel-shift is less than magnitude of OBS vel-shift, by apex velocity component

for i in range(NO):
    j=int(chord_params[i*4])
    if j>180:
        gallon_rads=degtorad*float(chord_params[i*4])
        object_radius=lytokpc*float(chord_params[i*4+1])
        vel_dop_shf=float(chord_params[i*4+2])
        f5=gallon_rads
        f8=solar_radius
        e8=object_radius
        beta=math.asin((f8/e8)*math.sin(2*pi-f5))
        phi=0.5*pi-beta
        lsr_radial_vel=lsr_vel*math.cos(1.5*pi-f5)
        apex_radial_vel=apex_velocity*math.cos(gallon_rads-apex_alpha) 
        #apex_radial_vel is NEG for gallon>180
        object_vel=(lsr_radial_vel-(vel_dop_shf+apex_radial_vel))/math.cos(phi)
        radius.append(object_radius)
        velocity.append(object_vel)
        vel_err_chord.append(float(chord_params[i*4+3]))  
    #next i
#endfor
radius.pop(0)
velocity.pop(0)
vel_err_chord.pop(0)

with open("velocity.dat", 'w') as g:
    g.write("Radius (kpc), Velocity (km/s)");g.write("\n")
    print("Radius (kpc), Velocity (km/s)")
    for i in range(NI):
        print(radiustangent[i],int(velocitytangent[i]),int(vel_err_tan[i]))
        g.write(str(radiustangent[i]));g.write(" ");g.write(str(velocitytangent[i]));g.write(" ");g.write(str(vel_err_tan[i]));g.write("\n")
    #endfor
    print(radiussolar[0],int(velocitysolar[0])," 0.0")
    g.write(str(radiussolar[0]));g.write(" ");g.write(str(velocitysolar[0]));g.write(" 0.0");g.write("\n")
    for i in range(NO):
        print(radius[i],int(velocity[i]),int(vel_err_chord[i]))
        g.write(str(radius[i]));g.write(" ");g.write(str(velocity[i]));g.write(" ");g.write(str(vel_err_chord[i]));g.write("\n")
    #endfor
g.closed
True

#Plot velocity versus radius
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
fig=plt.figure(figsize=(10,6))
ax=plt.axes()
ax.scatter(radiustangent,velocitytangent,c='green',s=100)
ax.scatter(radiussolar,velocitysolar,c='orange',s=100)
ax.scatter(radius,velocity,c='black',s=100)
ax.errorbar(radiustangent,velocitytangent,vel_err_tan,linestyle='',color='green')
ax.errorbar(radius,velocity,vel_err_chord,linestyle='',color='black')
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

 
