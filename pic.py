import numpy as np

#this is so in the future I don't have to copy and paste critcal functions anymore
# the phase 1 2 3 files are temporary and will be cleaned up later

def make_grid(L, Ng):
    """Return dx, x_grid, k, k_safe for a periodic 1D grid (a 1d grid is lowk a number link)"""
    dx = L / Ng
    x_grid = np.arange(Ng) * dx
    k = 2 * np.pi * np.fft.fftfreq(Ng, d=dx)
    k_safe = np.where( k == 0, 1.0, k)
    return dx, x_grid, k, k_safe

def deposit_charge(position, Ng, dx, q_per):
    """
    Spread each particle's charge onto the two nearest grid point usign Cloud in Cell (CIC).
    Returns rho (charge density) with uniform ion background (frozen ion appoximation)

    """
    rho = np.zeros(Ng)
    j_float = position / dx
    j = np.floor(j_float).astype(int) % Ng
    f = j_float - np.floor(j_float)

    jp1 = (j + 1) % Ng
    np.add.at(rho, j, q_per * (1 - f))
    np.add.at(rho, jp1, q_per * f)

    rho /= dx
    rho += 1.0 # frozen ion approx

    return rho

def field_solver(rho, k_safe):
    """Solve Poisson's equation via fast fourier transform FFT. Returns E Field on the Grid"""
    rho_hat = np.fft.fft(rho)
    E_hat =-1j * rho_hat / k_safe
    E_hat[0] = 0.0;
    return np.real(np.fft.ifft(E_hat))

def interpolate_field(E, positions, Ng, dx):
    """
    Sample the grid E field at each particles postition using CIC. Testing out symmetric weights to prevent self force and preserve momentum
    """
    j_float = positions / dx 
    j = np.floor(j_float).astype(int) % Ng
    f = j_float - np.floor(j_float)
    jp1 = (j + 1) % Ng
    return (1 - f) * E[j] + f * E[jp1]




