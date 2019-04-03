import numpy as np
import math
import rebound

from plotting import plot_flux, plot_transit_variations


class Star:
    mass = 0.0
    radius = 0.0

    def __init__(self, mass, radius):
        self.mass = mass
        self.radius = radius


class Planet:
    mass = 0.0
    a = 1.0
    radius = 0.0

    def __init__(self, mass, a, radius=0.0):
        self.mass = mass
        self.a = a
        self.radius = radius


def run_simulation(star, planets, total_transits, step_time=3600, plot_interval=25, show_plot=False):
    system = rebound.Simulation()
    system.integrator = "whfast"
    system.units = ('s', 'm', 'kg')
    system.add(m=star.mass, vx=0.0, vy=0.0, vz=0.0)
    for i in range(len(planets)):
        system.add(m=planets[i].mass, a=planets[i].a)
    system.move_to_com()
    system.dt = 100
    system.status()

    num_transits = 0
    transits = []
    flux = []

    planet = planets[0]
    in_transit = is_transiting(system.particles, star.radius, planet.radius)

    step = 0
    while num_transits < total_transits:
        step += 1
        system.integrate(step*step_time)

        if is_transiting(system.particles, star.radius, planet.radius):
            if step >= plot_interval: # make sure plot starts out not transiting
                f = calculate_flux(system.particles, star.radius, planet.radius)
                flux.append([step, f])
            if not in_transit:
                in_transit = True

                # planet was not transiting last time but is now
                # so we do binary search to find the exact start of the transit
                t_0 = (step-1)*step_time
                t_1 = step*step_time
                while t_1-t_0 > 1:
                    system.integrate((t_0+t_1)/2.)
                    if is_transiting(system.particles, star.radius, planet.radius):
                        t_1 = (t_0+t_1)/2.
                    else:
                        t_0 = (t_0+t_1)/2.
                transits.append(t_0)
                num_transits += 1
        else:
            in_transit = False

        if step % plot_interval == 0 and not in_transit:
            flux.append([step, 1.0])

    if show_plot:
        flux_arr = np.array(flux)
        plot_flux(flux_arr, transits, step_time)
    return transits


def is_transiting(particles, r_star, r_planet):
    if particles[1].x < particles[0].x:
        return False

    r2 = (r_star + r_planet)**2
    distyz2 = (particles[0].y - particles[1].y)**2 + (particles[0].z - particles[1].z)**2

    return distyz2 < r2


def calculate_flux(particles, r_star, r_planet):
    dist = ((particles[0].y - particles[1].y) ** 2 + (particles[0].z - particles[1].z) ** 2) ** 0.5
    if dist < r_star - r_planet:
        area = math.pi * r_planet**2
    else:
        area = calculate_overlap(dist, r_star, r_planet)
    frac = area/(math.pi * r_star**2)
    return 1.0 - frac


def calculate_overlap(d, r1, r2):
    cos_alpha = (r1**2 + d**2 - r2**2)/(2.0*r1*d)
    cos_beta = (r2**2 + d**2 - r1**2)/(2.0*r2*d)

    alpha = math.acos(cos_alpha)
    beta = math.acos(cos_beta)

    area = alpha * r1**2 + beta * r2**2 - 0.5*(r1**2)*math.sin(2*alpha) - 0.5*(r2**2)*math.sin(2*beta)

    return area


sun = Star(1.9885e30, 6.957e8)
earth = Planet(5.97237e24, 149.598e9, 6.3781e6)

mercury = Planet(3.3e23, 57.9e9)
venus = Planet(4.87e24, 108.2e9)
mars = Planet(6.42e23, 227.9e9)
jup = Planet(1.89e27,740.52e9)
saturn = Planet(1.9e27, 1427e9)
uranus = Planet(8.68e25, 2871e9)
neptune = Planet(1.29e22, 5913e9)

# number of transits to simulate
num_transit_str = input("number of transits: ")
while not num_transit_str.isnumeric():
    num_transit_str = input("number of transits: ")
num_transits = int(num_transit_str)

# how many transits we wait before calculating the variation
plot_interval_str = input("comparison interval (default 1): ")
if plot_interval_str.isnumeric() and int(plot_interval_str) > 0:
    plot_interval = int(plot_interval_str)
else:
    plot_interval = 1

# decide whether to show variation from jupiter only, or from entire solar system
jupiter_str = input("Jupiter only? (y/n, default n): ")
jupiter_only = (jupiter_str == "y")

show_flux_str = input("Plot flux? (y/n, default n): ")
show_flux = (show_flux_str == "y")

if jupiter_only:
    planet_list = [earth, jup]
else:
    planet_list = [earth, mercury, venus, mars, jup, saturn, neptune]

t = run_simulation(sun, planet_list, num_transits, show_plot=show_flux)
all_periods = [t[i+1]-t[i] for i in range(len(t)-1)]
periods = all_periods[0::plot_interval]
diffs = [periods[i + 1] - periods[i] for i in range(len(periods) - 1)]
plot_transit_variations(diffs, plot_interval)
