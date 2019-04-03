import matplotlib.pyplot as plt
import numpy as np


def plot_flux(flux, transits, step_size):
    avg_transit = int((transits[-1]/len(transits))/step_size)
    plot_data = np.empty_like(flux)
    plot_data[:,0] = (flux[:,0] - .5*avg_transit) % avg_transit
    plot_data[:,1] = flux[:,1] - .0005*np.floor((flux[:,0]-0.5*avg_transit)/avg_transit)
    near_transit = abs(plot_data[:,0] - .5*avg_transit) < 150

    left_breaks = []
    right_breaks = []
    for i in range(1, len(plot_data[:,0])):
        if near_transit[i-1] == 0 and near_transit[i] == 1:
            left_breaks.append(i)
        elif near_transit[i-1] == 1 and near_transit[i] == 0:
            right_breaks.append(i)
    if left_breaks[-1] > right_breaks[-1]:
        left_breaks = left_breaks[:-1]
    if right_breaks[0] < left_breaks[0]:
        right_breaks = right_breaks[1:]

    near_transit_data = []
    for l,r in zip(left_breaks,right_breaks):
        t_data = plot_data[l:r,:]
        near_transit_data.append(t_data)

    plt.figure()
    plt.title("flux")
    for transit_data in near_transit_data:
        plt.plot(transit_data[:,0], transit_data[:,1],"b-")
    # plt.scatter(plot_data[near_transit,0], plot_data[near_transit,1],2)
    plt.show(block=False)


def plot_transit_variations(variations, interval):
    plt.figure()
    plt.title("transit period changes")
    plt.plot(variations, "b.-")
    plt.xlabel("Transit")
    plt.xticks(range(0, len(variations)), range(0, interval*len(variations), interval))
    plt.ylabel("change from previous (seconds)")
    plt.show(block=False)