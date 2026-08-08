# planning to do an isolated particle motion with perodic boundaries. 

import numpy as np
import matplotlib.pyplot as plt

# Sim parameters
N = 1000  # Number of particle
L = 2 * np.pi # length of the box
dt = 0.1 # time steps
n_steps = 100 # number of steps 

# store values so I can plot later
position_history = np.zeros((n_steps, N))

# inital stuff

positions = np.random.uniform(0,L,N)
velocities = np.ones(N)
#velocities = np.random.uniform(-1,1,N)

for step in range (n_steps):
    positions = positions + (velocities * dt)

    positions = positions % L # partcles wrap around, so the topology of the environment is a torous/donut

    position_history[step] = positions   

# Plot results
plt.figure(figsize=(10,6))
for i in range(0,N,50): # show every 50th particle
    plt.plot(position_history[:, i], np.arange(n_steps), '.', markersize=1)
plt.xlabel("X_position")
plt.ylabel("Time_step")

plt.xlim(0,L)
plt.show()
