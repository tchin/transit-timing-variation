This project exhibits transit timing variation by simulating the variations in Earth's orbital period caused by the rest of the solar system.

The user can choose how many transits to simulate, as well as whether to simulate the entire solar system or Jupiter only. To experiment with other combinations, you can manually edit the planet_list variable in code, but Earth should always come first (so the program knows which planet to track transits for).

The program then simulates the desired number of transits, and plots the change in orbital period. If the user specifies a plot interval, then each period is compared to the period plot_interval transits (i.e. years) before. This allows you to see a more macroscopic evolution of the transit time, rather than just the year-to-year noise.

The user can also opt to plot the flux curves for each transit. If so, the program will produce a second graph with the transit curves plotted above one another so the user can see the actual curve shifting over time. However, due to plotting limitations, it becomes difficult to see the transits if too many curves are plotted on the same graph, so this option is best used when simulating a relatively small number of transits
