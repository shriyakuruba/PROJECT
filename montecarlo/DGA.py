import pandas as pd
import numpy as np

class Die:
    """
    A Die with N sides, each with a user-defined weight.

    Attributes:
        _df (pd.DataFrame): A private dataframe containing faces and weights.
    """
    
    def __init__(self, faces):
        """
        Initialize the Die object with a NumPy array of unique face values.
        
        Parameters:
            faces (np.ndarray): A NumPy array of unique symbols (strings or numbers).

        Raises:
            TypeError: If input is not a NumPy array.
            ValueError: If elements are not unique.
        """
    
        if not isinstance(faces, np.ndarray):
            raise TypeError("Faces must be a NumPy array.")
        if len(np.unique(faces)) != len(faces):
            raise ValueError("Faces must be unique.")
        
        self._df = pd.DataFrame({
            'face': faces,
            'weight': [1.0] * len(faces)
        }).set_index('face')

    def change_weight(self, face, new_weight):
        """
        Change the weight of a single face.
        
        Parameters:
            face: The face whose weight is to be changed.
            new_weight (float or int): The new weight, must be non-negative.

        Raises:
            ValueError: If face not found or weight is invalid.
        """
        if face not in self._df.index:
            raise ValueError("Face not found in die.")
        if not isinstance(new_weight, (float, int)) or new_weight < 0:
            raise ValueError("Weight must be a non-negative number.")
        self._df.at[face, 'weight'] = float(new_weight)

    def roll(self, n_rolls=1):
        """
        Roll the die one or more times.
        
        Parameters:
            n_rolls (int): Number of times to roll.

        Returns:
            np.ndarray: Array of rolled face values.
        """
        return self._df.sample(
            n=n_rolls, 
            weights=self._df['weight'], 
            replace=True
        ).index.to_numpy()

    def show(self):
        """
        Return the current faces and weights.

        Returns:
            pd.DataFrame: DataFrame with face and weight columns.
        """
        return self._df.reset_index()

    
class Game:
    """
    A Game consists of rolling multiple Die objects a specified number of times.
    
    Attributes:
        dice (list): A list of Die objects.
        _results (pd.DataFrame): Results of the most recent play.
    """
    def __init__(self, dice):
        """
        Initialize the Game with a list of Die objects.

        Parameters:
            dice (list): List of Die objects.
        """
        self.dice = dice
        self._results = None

    def play(self, n_rolls):
        """
        Roll all dice for a specified number of times and store the result.

        Parameters:
            n_rolls (int): Number of times to roll the dice.
        """
        all_results = {}
        for i, die in enumerate(self.dice):
            all_results[f'die_{i+1}'] = die.roll(n_rolls)
        
        self._results = pd.DataFrame(all_results)
        self._results.index.name = 'roll_num'

    def show(self, form='wide'):
        """
        Show the results of the most recent play.

        Parameters:
            form (str): 'wide' or 'narrow' format.

        Returns:
            pd.DataFrame: DataFrame of results in the selected format.
        """
        if form == 'wide':
            return self._results
        elif form == 'narrow':
            return self._results.reset_index().melt(id_vars='roll_num', var_name='die', value_name='face')
        else:
            raise ValueError("Form must be 'wide' or 'narrow'.")

            
class Analyzer:
    """
    An Analyzer takes the results of a Game and computes descriptive statistics.

    Attributes:
        game (Game): A Game object.
        results (pd.DataFrame): Results from the game's last play.
    """
    def __init__(self, game):
        """
        Initialize the Analyzer with a Game object.

        Parameters:
            game (Game): The Game object to analyze.

        Raises:
            ValueError: If input is not a Game object.
        """
        if not isinstance(game, Game):
            raise ValueError("Input must be a Game object.")
        
        self.game = game
        self.results = game.show('wide')
        self.jackpot_results = None
        self.face_counts = None

    def jackpot(self):
        """
        Count how many times all dice in a roll showed the same face.

        Returns:
            int: Number of jackpot rolls.
        """
        jackpots = self.results.nunique(axis=1) == 1
        self.jackpot_results = jackpots
        return jackpots.sum()

    def face_counts_per_roll(self):
        """
        Count how many times each face appeared in each roll.

        Returns:
            pd.DataFrame: DataFrame with roll number as index and face counts as columns.
        """
        counts = self.results.apply(pd.Series.value_counts, axis=1).fillna(0).astype(int)
        self.face_counts = counts
        return self.face_counts

    def combo(self):
        """
        Compute distinct combinations of faces rolled, regardless of order.

        Returns:
            pd.DataFrame: DataFrame indexed by combo with count column.
        """
        combos = self.results.apply(lambda row: tuple(sorted(row)), axis=1)
        combo_counts = combos.value_counts().to_frame('count')
        combo_counts.index.name = 'combo'
        self.combo_df = combo_counts
        return self.combo_df

    def permutation(self):
        """
        Compute distinct permutations of faces rolled (order matters).

        Returns:
            pd.DataFrame: DataFrame indexed by permutation with count column.
        """
        perms = self.results.apply(lambda row: tuple(row), axis=1)
        perm_counts = perms.value_counts().to_frame('count')
        perm_counts.index.name = 'permutation'
        self.permutation_df = perm_counts
        return self.permutation_df