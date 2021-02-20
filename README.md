# NFL-Circle-of-Parity

In the NFL circle of parity, each team has beaten the team to its right (clockwise) at least once during the season. This path around the circle is an instance of a Hamiltonian cycle, with each team's node being visited exactly once. This repository contains code to find whether such a cycle exists for a given season (up to a certain week, if specified) and to generate a visualization of the cycle, as seen in the `sample_circles` directory. A SAT solver is used to find the Hamiltonian cycles (an NP-complete problem).

#### Example: 2020 Circle of Parity
![Sample circle](https://github.com/gzanuttinifrank/NFL-Circle-of-Parity/blob/main/sample_circles/2020_Circle_of_Parity.png)
