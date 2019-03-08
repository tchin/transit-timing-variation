import matplotlib.pyplot as plt
import numpy as np


def plot_flux(flux, transits, step_size):
    avg_transit = int((transits[-1]/len(transits))/step_size)
    plot_data = np.empty_like(flux)
    plot_data[:,0] = (flux[:,0] - .5*avg_transit) % avg_transit
    plot_data[:,1] = flux[:,1] - .0003*np.floor((flux[:,0]-0.5*avg_transit)/avg_transit)
    near_transit = abs(plot_data[:,0] - .5*avg_transit) < 500
    plt.figure()
    plt.suptitle("flux")
    plt.axes(ylim=(.998, 1.0))
    plt.scatter(plot_data[near_transit,0], plot_data[near_transit,1],2)
    plt.show(block=False)


def plot_transit_variations(variations):
    plt.figure()
    plt.suptitle("transit period changes")
    plt.plot(variations, "b.")
    plt.show(block=False)