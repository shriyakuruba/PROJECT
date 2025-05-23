import pandas as pd
import numpy as np

class Die:
    """A class representing a single die with chosen N sides and W weights.

    Each face has a unique symbol, and a weight associated with it that determines the likelihood of that face being rolled. By default, all weights are 1.0, making the die fair, but can be changed after the object is created. The die can be rolled to select a face based on weights.

    Attributes:
        faces (np.ndarray): A NumPy array of unique face values (must be strings or numbers)
        weights (np.ndarray): A NumPy array of weights, defaulting to 1.0 for each face.
        _df (pd.DataFrame): A private DataFrame storing faces and weights with faces as the index.
    """
    def __init__(self, faces: np.ndarray):
        """Initializes the Die object with the provided faces.

        Args:
            faces (np.ndarray): A NumPy array of unique face values (must be strings or numbers)

        Raises:
            TypeError: If `faces` is not a NumPy array.
            ValueError: If the values in `faces` are not distinct.
        """
        # to take care of the errors for this method
        if not isinstance(faces, np.ndarray):
            raise TypeError("Faces must be a NumPy array.")
        if len(np.unique(faces)) != len(faces):
            raise ValueError("Faces must be unique.")
            
        self.faces  = faces    
        self._df = pd.DataFrame({'face': faces, 'weight': [1.0] * len(faces)})
        self._df.set_index('face', inplace=True)

    def change_weight(self, face, new_weight):
        """Changes the weight of a single face on the die.

        Args:
            face (str or int): The face value whose weight should be changed.
            new_weight (float): The new weight to assign to the face chosen.

        Raises:
            IndexError: If the face is not found in the die.
            TypeError: If the weight is not numeric or cannot be cast as numeric.
        """
        if face not in self._df.index:
            raise IndexError(f"Face '{face}' is not in the die.")
        try:
            new_weight = float(new_weight)
        except (TypeError, ValueError):
            raise TypeError("New weight must be a numeric value (int or float).")
            
        self._df.loc[face, 'weight'] = new_weight

    def roll(self, num_rolls = 1):
        """Rolls the die one or more times using the current weights.

        Args:
            num_rolls (int): Number of rolls to perform. Defaults to 1.

        Returns:
            list: A list of face values rolled.
        
        Raises:
            ValueError: If `num_rolls` is not a positive integer.
        """
        if not isinstance(num_rolls, int) or num_rolls < 1:
            raise ValueError("Number of rolls must be a positive integer.")
            
        results = list(
            np.random.choice(
                self._df.index,
                size = num_rolls,
                replace = True,
                p = self._df['weight'] / self._df['weight'].sum()
            )
        )
        return results
    
    def show_die(self):
        """Show the current faces and weights of the die.

        Returns:
            pd.DataFrame: A copy of the internal dataframe with the faces and weights.
        """
        return  self._df.copy()
    
class Game:
    """
    A Game consists of rolling one or more Die objects a specified number of times.
    
    The game is played by rolling all provided dice a specified number of times.
    Dice in a game are considered similar if they have the same faces, although their weights may differ.
    The Game class only stores the results of the most recent play.

    Attributes:
        dice (list): A list of Die objects.
        _results (pd.DataFrame): Results of the most recent play.
    """
    def __init__(self, dice_list: list):
        """
        Initialize the Game with a list of Die objects.

        Args:
            dice_list (list): List of Die objects.
        
        Raises:
            TypeError: If any item in the list is not an instance of the Die class.
            ValueError: If not all dice have the same faces.
        """
        
        if not all(isinstance(d, Die) for d in dice_list):
            raise TypeError("All elements in dice must be instances of the Die class.")
        
        first_face = dice_list[0].faces
        for d in dice_list[1:]:
            if not np.array_equal(d.faces, first_face):
                raise ValueError("All dice must have the same set of faces.")
                
        self.dice = dice_list
        self._results = None

    def play(self, num_rolls: int):
        """
        Roll all dice for a specified number of times and store the result.

        Args:
            n_rolls (int): Number of times to roll the dice.
            
        Raises:
            ValueError: If `num_rolls` is not a positive integer.
        """
        
        if not isinstance(num_rolls, int) or num_rolls < 1:
            raise ValueError("Number of rolls must be a positive integer.")

        roll_data = {}
        for i, die in enumerate(self.dice):
            roll_data[i] = die.roll(num_rolls)

        self._results = pd.DataFrame(roll_data)
        self._results.index.name = "roll number"

    def show(self, form: str = "wide"):
        """
        Show the results of the most recent game.

        Args:
            form (str): Format of the returned DataFrame. Either 'wide' or 'narrow'.
                                  'wide' returns the DataFrame as-is (default).
                                  'narrow' returns a long-format version with three columns: roll number, die number, and face.

        Returns:
            pd.DataFrame: A copy DataFrame of the game results.

        Raises:
            ValueError: If the `form` argument is not 'wide' or 'narrow'.
        """
        if self._results is None:
            return pd.DataFrame()  # No play has occurred yet

        if form == "wide":
            return self._results.copy()
        elif form == "narrow":
            return self._results.reset_index().melt(id_vars=["roll number"],
                                                         var_name="die number",
                                                         value_name="face")
        else:
            raise ValueError("form must be either 'wide' or 'narrow'")
            
            
class Analyzer:
    """
    An Analyzer takes the results of a single Game and computes different descriptive statistical analysis.

    Attributes:
        game (Game): A Game object containing the results of the dice rolls.
        results (pd.DataFrame): The results of the game's last play (each row is a roll).
        face_counts_per_roll (pd.DataFrame): Counts of each face in each roll.
        jackpots (pd.DataFrame): Rolls where all dice showed the same face.
        permutations (pd.DataFrame): Unique combos and their counts.
    """
    def __init__(self, game):
        """
        Initialize the Analyzer with a Game object.

        Parameters:
            game (Game): An instance of the Game object

        Raises:
            ValueError: If input is not an instance of Game
        """
        if not isinstance(game, Game):
            raise ValueError("The input must be a Game object.")
        
        self.game = game
        self.results = game.show('wide')
        
    def jackpot(self):
        """
        Count how many times all dice in a roll showed the same face

        Returns:
            int: # of jackpots
        """
        jackpots = self.results.nunique(axis = 1) == 1
        return jackpots.sum()

    def face_counts_per_roll(self):
        """
        Counts how many times each face appeared in each roll

        Returns:
            pd.DataFrame: A DataFrame with roll number as index, face values as columns, and the count of each face per roll as values
        """
        face_counts = self.results.apply(pd.Series.value_counts, axis = 1).fillna(0).astype(int)
        face_counts.index.name = "roll number"
        return face_counts

    def combo(self):
        """
        Counts the distinct combinations of faces rolled, along with their counts
        
        Combos are unordered ([1,2,3] is the same as [3,2,1]) and can include repeated faces

        Returns:
            pd.DataFrame: Dataframe of unique combos and their counts.
        """
        sorted_results = self.results.apply(lambda row: tuple(sorted(row)), axis=1)
        combos = sorted_results.value_counts().sort_index()
        combo_df = combos.to_frame(name='count')
        combo_df.index = pd.MultiIndex.from_tuples(combo_df.index)
        return combo_df

    def permutation(self):
        """
        Counts the distinct permutations of faces rolled (order matters), along with count

        Returns:
            pd.DataFrame: DataFrame indexed by permutation with 'count' column.
        """
        perms = self.results.apply(lambda row: tuple(row), axis=1).value_counts().sort_index()
        perm_df = perms.to_frame(name='count')
        perm_df.index = pd.MultiIndex.from_tuples(perm_df.index)
        return perm_df