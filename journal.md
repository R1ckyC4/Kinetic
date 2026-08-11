## 8/10/2026

**Did**
- used fourier space to solve poissons equation
- generated a sinusoidal pertubation and plotted it
- varied the number of particles to see how smooth the sinusoidal looks after the noise evens outi

noticed that the charge density roughly looks like a sin function, but with much more noise
noticed that the electric field looks like a cos function (sin with a 90 deg transformation)/ this one evened out the noise much better
Test 2- apply a small cosine displacement to the particles, this should make the density plot look like a -sin plot
    Havent quite grasped the math yet, just know it should work. 



what was hard? walkm=ing myself through the math again. 

What did I learn? embarassingly, i took some time to experiment with how to have two plots on the same screen, i usually generate them separately. Did this because I saw a matlab script have like 8 plots placed together.

**stuff to think about**
    I should find a way to make this interactive, considering steamlit, which is a python framework that I came accross when I was scrolling instagram. 

**second session**
Extended kinetic2_2.py to a PIC simulation. Built the interpolation_field function. 
Field energy oscillates kinda nicely at -2 * omega_p (ang freq)

**sadly i forgot to save the graphs of the work before the oscillation test** 
![Plasma oscillation field energy](figure\plasma_oscillation_test1.png)
I would have to note that the energy starts really high at t = 0

## 8/9/2026
playing around in kinetic_2. In phase 1 i only practiced making a box with some particles in it to warm up my numpy skills. Phase 2 i was playing around with charge densities and distributions in 1d in a CIC.
**Did**
- built charge deposition using CIC weighing
- ran noise scaling experiments with varying N and Ng.

** Learned **
- Ion background (frozen Ion/jellium approximation using 'rho += 1)
- used +=1 to balanec the -1 charge of the electrons
- we do this because protons much heavier than electrons on the timescales (they move much more slowly compared to the electrons)

** Next: ** Poisson solve using fft

Uniform particle distribution should give near zero net charge/field (which was about right for my sim)
