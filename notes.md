## 8/11
single warm plasmas are stable because energy stays trapped between fields and particles. When a localized bunch appears, the field that it creates 
pushes against local particles. Then those particles push back against the bunch and flatten it back towards uniform. However, because electrons have mass, they overshoot just like a mass on a spring and 
slosh back and forth. 
But that process kinda happens back and forth, so it forms a closed loop with no net gain

two counter streams are unstable because theres excess kinetic energy (from the physical movement of the stream) 
the instability will die when teh two beams are thermalized, which means it is not longer ordered and directional (randomized)
Kinetic energy is converted to field energy.


linear growth phase doesn't mean that the plasma grows linearly
    but rather that the linearized physics equations predicts exponential growth
    the linear part here is referencing the regime and not the shape.

Counter streaming beams lead to vortices because the field, which gained energy from the kinetic energy of the particles,
becomes strong enough to trap electrons. When a significant number of the beam particles gets trapped, the beams look like theyve broekn up into hot particels swirling around the wave





## 8/10/2026 poisson solve on kinetic_2.py
periodic functions can be written as a Fourier Series, or a sum of complex expos

Poisson's equation in 1d is d2 phi / d x2 = -p(x)
p(x) = sigma_k p ^ k * esp(ikx)
p^k are complex numbers/fourier coefficents
k runs over integer multiples of 2pi/L

getting derivatives in fourier space is easier than solving it for real. d/dx of exp(ikx) becomes ik*exp(ikx)
which means the second derivative is just multiplying by -k^2


shot noise: arised from the fact we are counting finate discrete events but trying to represent a continuous value. 

PIC - particle in cell 
Four steps: deposit, solve, intepolate, push
    interestingly enough, this is really similar to Jos Stam's stable fluid pipeline


Instead of calculating particle to particle for N bodies, we only analyze the system at points on the spatial grid. 
We can vary our accuracy and precision by increasing the density of these grids or adding more particles




