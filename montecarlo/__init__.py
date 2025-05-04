"""
montecarlo: A Monte Carlo simulation module with three classes:

=== Die ===
A die that can be rolled with weighted probabilities on each face.

Methods:
- __init__(faces): Initialize with unique faces (NumPy array).
- change_weight(face, new_weight): Change the weight for a given face.
- roll(n_rolls = 1): Roll the die n times.
- show_die(): Show current faces and weights.

=== Game ===
A Game object for rolling multiple dice and saving the results.

Methods:
- __init__(dice): Initialize with a list of Die objects.
- play(n_rolls): Roll all dice n times.
- show(form): Show results in 'wide' or 'narrow' format.

=== Analyzer ===
Analyzes a Game's results to compute statistics.

Methods:
- __init__(game): Takes a Game object to analyze.
- jackpot(): Count rolls where all dice match.
- face_counts_per_roll(): Count each face per roll.
- combo(): Count combinations of rolled faces.
- permutation(): Count ordered permutations of rolls.
"""

from .montecarlo import Die, Game, Analyzer

help(Die)        # Shows Die class docstring
help(Game)       # Shows Game class docstring
help(Analyzer)   # Shows Analyzer class docstring