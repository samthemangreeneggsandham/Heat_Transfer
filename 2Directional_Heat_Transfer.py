import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

field_shape = [50,50]
dt = 0.1
t_max = 100
Tbound = 1 # Temperature function scale factor
alpha = 2 # Heat diffusivity

t_list = []
T_list = []

def field_func(x):
    """Define function of Tfield"""

    return np.sin(x/10)

def gen_init_field(field_shape, Tbound):
    """Generates an initial field using the product of the field function evaluated at i and j positions"""

    Tfield = np.zeros(field_shape)
    for i in range(0,field_shape[0]-1):
        for j in range(0,field_shape[1]-1):
            Tfield[i][j] += (field_func(i)*field_func(j))*Tbound #Generates a field from positions
    return Tfield

Tfield = gen_init_field(field_shape, Tbound)

def update_T(Tfield):
    """Function to update the Temperature of the field over time"""

    x_range = Tfield.shape[0]
    y_range = Tfield.shape[1]
    t = 0

    while t < t_max:
        # Creates a copy of the current field to take T values from
        T_old = Tfield.copy()

        # Calculates change in T wrt t from second derivative of position
        for i in range(1,x_range-1):
            for j in range(1,y_range-1):
                Tfield[i, j] = T_old[i, j] + alpha * dt * ((T_old[i-1][j] - 2*T_old[i][j] + T_old[i+1][j]) + (T_old[i][j-1] - 2*T_old[i][j] + T_old[i][j+1]))

        # Edge boundary conditions (insulated)
        for l in range(0,x_range):
            Tfield[0][l] = Tfield[1][l]
            Tfield[x_range-1][l] = Tfield[x_range-2][l]

        for k in range(0,y_range):
            Tfield[k][0] = Tfield[k][1]
            Tfield[k][y_range-1] = Tfield[k][y_range-2]

        t += dt

        t_list.append(t)
        T_list.append(Tfield.copy())

update_T(Tfield)

fig, ax = plt.subplots()
im = ax.imshow(T_list[0], cmap='viridis', interpolation='nearest')

def update(frame):
    im.set_data(T_list[frame])
    ax.set_title(f"Time = {t_list[frame]:2f}")
    print(t_list[frame])
    return [im]

# Create animation
ani = FuncAnimation(
    fig, update, frames=len(T_list), interval=200, blit=False, repeat=False
)

# Show animation
plt.show()