import numpy as np
import cmath as cm
import matplotlib.pyplot as plt


def rotate(vect,rot):
    radAngle = rot * np.pi / 180
    
    rotvect = cm.rect(1,radAngle)
    
    x = (vect[0] * rotvect.real) - (vect[1] * rotvect.imag) #calculate X component of resultant vector
    y = (vect[1] * rotvect.real) + (vect[0] * rotvect.imag) #calculate Y component of resultant vector
    
    #mag = np.round(np.sqrt((x * x) + (y * y)), decimals = 2) # calculate magnitude of the vector
    
    plt.plot([0,vect[0]],[0,vect[1]], label= "Original Vector") #plot original vector
    plt.plot([0, x], [0, y], label="Rotated Vector") #plot rotated vector
    
    plt.legend()
    plt.show()

def rotate_2 (vect, rot):
    rad = rot * np.pi/180
    alpha = vect[1]/ vect[0]
    theta = cm.atan(alpha)
    mag = np.sqrt((vect[0] * vect[0]) + (vect[1] * vect[1]))
    x = mag * (cm.cos(rad + theta))
    y = mag * (cm.sin(rad + theta))
    plt.plot([0,vect[0]],[0,vect[1]], label= "Original Vector") #plot original vector
    plt.plot([0, x], [0, y], label="Rotated Vector") #plot rotated vector
    
    plt.legend()
    plt.show()
    
inp = input("Enter X and Y components: ").split()

vect = [float(inp[0]), float(inp[1])]

angle = float(input("Enter angle to rotate (degrees) in the anticlockwise direction: "))

print("\n")
radAngle = angle * np.pi / 180

rotvect = cm.rect(1,radAngle) #Vector with mag 1 and makes radAngle with x axis

x = (vect[0] * rotvect.real) - (vect[1] * rotvect.imag) #calculate X component of resultant vector
y = (vect[1] * rotvect.real) + (vect[0] * rotvect.imag) #calculate Y component of resultant vector

max = np.max([vect[0], x, vect[1], y])
min = np.min([vect[0], x, vect[1], y])


#plt.xlim(min, max)
#plt.ylim(min, max)

plt.axes().set_aspect("equal")
mag = np.round(np.sqrt((x * x) + (y * y)), decimals = 4) # calculate magnitude of the vector

#rotate(vect, angle)
rotate_2(vect, angle)

print ("Magnitude of Vectors: ",mag)

x = np.round(x,decimals = 3)
y = np.round(y, decimals = 3)
print ("\nRotated Vector: X: ", x,"Y: ", y)





