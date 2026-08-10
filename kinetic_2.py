import numpy as np
import matplotlib.pyplot as plt

# parameters
N = 100000 # number of macro parts
Ng = 256 # num of grid cells

L = 2 * np.pi

dt = 0.05

n_steps = 500

# Grid
dx = L / Ng # grid spacing

x_grid = np.arange(Ng) * dx

# inital conds
rng = np.random.default_rng(seed=67)
positions = rng.uniform(0,L,N)
velocities = rng.normal(0,0.1,N)

# notes
# I gave the particles their vels based on a gaussian distribution, like the maxwell boltzmaan dist
#rho is charge density

q_per = -L / N # charge per macro particle

def deposit_charge(positions):
    """
    Spread each particle's charge onto the two nearest grid points using cluod in cell weighting. Returns charge density rho
    """
    rho = np.zeros(Ng)
    # for each parti, find which grid cell its in and where within that cell

    j_float = positions/dx # position in grid units
    j = np.floor(j_float).astype(int) % Ng 
    f = j_float - np.floor(j_float) # fractional distance to the right 
    jp1 = (j+1) % Ng

    #scatter charge to left and right grid points
    np.add.at(rho, j, q_per * (1-f))
    np.add.at(rho, jp1, q_per * (f))

    # convert to charge density (charge per unit length)
    rho /= dx

    rho += 1.0
    # going to treat the protons as a background, just like that one guy with the plum pudding model
    #text book says this is the frozen ion approx or jellium

    return rho


# Testing

rho = deposit_charge(positions)


print(f"total particles = {N}")
print(f"mean rho = {rho.mean()}")
print(f"max rho = {np.abs(rho).max()}")
print(f"q_er = {q_per}")
print(f"sum rho = {rho.sum() * dx}")
print(f"first 10 rho values {rho[:10]}")
plt.plot(x_grid,rho)
plt.xlabel('x')
plt.ylabel('rho')
plt.title("charge density (uniform)")
plt.axhline(0,color='k', lw = 0.5)

#notice how this plot is centered around zero? Thats noise bc I don't own a super computer and need to work with finate particle numbers :(. 
# #The Poisson noise should scale as sqrt(Ng/N) i think
plt.show()