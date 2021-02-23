# NFL-Circle-of-Parity

In the NFL circle of parity, each team has beaten the team to its right (clockwise) at least once during the season. This path around the circle is an instance of a Hamiltonian cycle in a directed graph, where an edge exists from a team to all unique teams it defeated that season, with each team's node being visited exactly once. This repository contains code to find whether such a cycle exists for a given season (up to a certain week, if specified) and to generate a visualization of the cycle, as seen below and in the `sample_circles` directory (which contains all of the possible circles since 2000). A SAT solver (Glucose 3 from pysat) is used to find the Hamiltonian cycles (an NP-complete problem).

To run the code to solve the circle and create the visualization, edit the 'year' and 'last_completed_week' variables in the file `solve_circle_of_parity.py` and run with Python3.

#### Example: 2020 Circle of Parity
![Sample circle](https://github.com/gzanuttinifrank/NFL-Circle-of-Parity/blob/main/sample_circles/2020_Circle_of_Parity.png)
