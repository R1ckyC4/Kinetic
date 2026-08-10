## 8/10/2026 poisson solve on kinetic_2.py
periodic functions can be written as a Fourier Series, or a sum of complex expos

Poisson's equation in 1d is d2 phi / d x2 = -p(x)
p(x) = sigma_k p ^ k * esp(ikx)
p^k are complex numbers/fourier coefficents
k runs over integer multiples of 2pi/L

getting derivatives in fourier space is easier than solving it for real. d/dx of exp(ikx) becomes ik*exp(ikx)
which means the second derivative is just multiplying by -k^2


shot noise: arised from the fact we are counting finate discrete events but trying to represent a continuous value. 