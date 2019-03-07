import numpy as np
import rebound

G = 6.67408e-11


class Body:
    mass = None
    radius = 0.0
    pos = np.array([0,0,0])
    v = np.array([0,0,0])

    def __init__(self, mass, pos, v, radius=0.0):
        self.mass = mass
        self.radius = radius
        self.pos = pos
        self.v = v

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


def run_simulation(star, planets, total_transits, step_time=3600):
    system = rebound.Simulation()
    system.integrator = "whfast"
    system.units = ('s', 'm', 'kg')
    system.add(m=star.mass, vx=0.0, vy=0.0, vz=0.0)
    for i in range(len(planets)):
        system.add(m=planets[i].mass, a=planets[i].a)
    system.move_to_com()
    system.dt = 1000
    system.status()

    pos_data = np.zeros((system.N,3), dtype="float64")

    num_transits = 0
    transits = []
    step = 0

    planet = planets[0]
    in_transit = is_transiting(system.particles, star.radius, planet.radius)

    while num_transits < total_transits:
        step += 1
        system.integrate(step*step_time)
        system.serialize_particle_data(xyz=pos_data)
        rad = np.linalg.norm(pos_data[1,:]-pos_data[0,:])
        if is_transiting(system.particles, star.radius, planet.radius):
            if not in_transit:
                in_transit = True

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

    return transits


def is_transiting(particles, r_star, r_planet):
    if particles[1].x < particles[0].x:
        return False

    r2 = (r_star + r_planet)**2
    distyz2 = (particles[0].y - particles[1].y)**2 + (particles[0].z - particles[1].z)**2

    return distyz2 < r2


sun = Star(1.9885e30, 6.957e8)
earth = Planet(5.97237e24, 1.49959e11)
jup = Planet(1.89e27,1e20)
t = run_simulation(sun, [earth,jup], 10)
periods = [t[i+1]-t[i] for i in range(len(t)-1)]
print(periods)