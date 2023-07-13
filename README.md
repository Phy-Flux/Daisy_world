# Daisy_world
A 3D-Daisyworld visualization model 

Daisyworld is a planetary toy model first designed by Lovelock in the early 1980s to study the impact of life on the global temperature of the earth. The model takes into account two species of daisy: black and white. Earth is approximated to a grey box where most of the major environmental phenomena are neglected. Only the interplay between surface temperature, albedo, daisy growth rate, and solar incoming radiation is considered in the mathematical modeling. 

The literature on the subject is vast. For those interested in a summary of the topic you can refer to: Wood, Andrew J., et al. "Daisyworld: A review." Reviews of Geophysics 46.1 (2008).

- Daisy_.py contains the function to evolve the population of daisies and the global temperature. It returns summary plots.
It requires as input from the user the solar average energy. For optimal usage, we suggest exploring the range between 700-1200 Wm^-2. Also, the initial cover of daisies can be changed by setting init_white, and init_black.

- Daisy_3D.py allow to produce plots of the population field projected on a 2D and 3D domain.
