# Monte Carlo Simulator

## Metadata
**Author:** Shriya Kuruba  
**Project Name:** Monte Carlo Simulator  

---

## Synopsis
This project is a Python package that allows users to simulate and analyze outcomes of rolling dice. The package has three main classes:
1. ```Die```: Represents a single die that can have N faces and W weights.
2. ```Game```: Manages one or more Die objects and playing a sequence of rolls.
3. ```Analyzer```: Analyzes the results of a game to provide statistics such as jackpots, combinations, and face counts.

## Package Structure
```python
montecarlo/
│
├── __init__.py         # Initializes the package
├── montecarlo.py       # Contains the classes: Die, Game, and Analyzer
│
tests/
├── test_montecarlo.py  # Contains unit tests for all three classes
│
README.md               # Project documentation
LICENSE                 # Licensing information
setup.py                # Setup script for installing the package
```
## Installation Instructions
You can clone the repository and install the package locally:

```python
git clone https://github.com/shriyakuruba/PROJECT.git
cd PROJECT
```
**OR**

You can install it as a package:

```python
pip install .
```

## How to Use
### Example Usage
```python
from montecarlo.montecarlo import Die, Game, Analyzer

### Create + Modify a Die
# Create a die with 6 sides
die = Die([1, 2, 3, 4, 5, 6])
# Change weight of face '1' to 3.0
die.change_weight(1, 3.0)
# View current die configuration
print(die.show())


### Play the Game
# Create a game with 3 dice
game = Game([die, die, die])
# Play 10 rolls
game.play(10)
# Show results in wide form
print(game.show('wide'))
# Show results in narrow form
print(game.show('narrow'))


### Analyze the Game
# Initialize analyzer with the played game
analyzer = Analyzer(game)
# Count how many times all dice had the same face (jackpot)
print(analyzer.jackpot())
# Get combination counts
print(analyzer.combo())
# Get face counts per roll
print(analyzer.face_counts_per_roll())
```

## API Description
### Class: ```Die```
```python
"""A class representing a single die with N sides and W weights.

    Each face has a unique symbol, and a weight associated with it that determines the likelihood of that face being rolled. By default, all weights are 1.0, making the die fair, but can be changed after the object is created. The die can be rolled to select a face based on weights.

    Attributes:
        faces (np.ndarray): A NumPy array of unique face symbols.
        weights (np.ndarray): A NumPy array of weights, defaulting to 1.0 for each face.
        _df (pd.DataFrame): A private DataFrame storing faces and weights with faces as the index.
"""
```
**Methods:**
*  ```__init__(faces: list)```
```python
    """Initializes the Die object with the provided faces.

        Args:
            faces (np.ndarray): A NumPy array of unique face symbols (must be strings or numbers).

        Raises:
            TypeError: If `faces` is not a NumPy array.
            ValueError: If the values in `faces` are not distinct.
        """
```
Initializes the die with given face values. All weights default to 1.0.

*  ```change_weight(face, new_weight: float)```
```python
    """Changes the weight of a single face on the die.

        Args:
            face (str or int): The face value whose weight should be changed.
            weight (float): The new weight to assign to the face chosen.

        Raises:
            IndexError: If the face is not found in the die.
            TypeError: If the weight is not numeric or cannot be cast as numeric.
        """
```
Changes the weight of a specific face.
    
**Parameters:**
    - face: The face value to modify.
    - new_weight (float): New weight to assign.
        Raises: ValueError if face not found or weight is invalid.
    
*  ```roll(n_rolls: int = 1) -> list```
```python
    """Rolls the die one or more times using the current weights.

        Args:
            num_rolls (int): Number of rolls to perform. Defaults to 1.

        Returns:
            list: A list of outcomes from the rolls.
        
        Raises:
            ValueError: If `num_rolls` is not a positive integer.
        """
```
Rolls the die n_rolls times and returns the outcomes.
*  ```show() -> pd.DataFrame```
```python
    """Show the current faces and weights of the die.

        Returns:
            pd.DataFrame: A copy of the internal dataframe.
        """
```
Returns a DataFrame of faces and their corresponding weights.

### Class: ```Game```
```python
"""
    A Game consists of rolling one or more Die objects a specified number of times.
    
    The game is played by rolling all provided dice a specified number of times.
    Dice in a game are considered similar if they have the same faces, although their weights may differ.
    The Game class only stores the results of the most recent play.

    Attributes:
        dice (list): A list of Die objects.
        _results (pd.DataFrame): Results of the most recent play.
    """
```
Represents a game with one or more dice.
**Methods:**
*  ```__init__(dice: list)```
```python
"""
        Initialize the Game with a list of Die objects.

        Args:
            dice_list (list): List of Die objects.
        
        Raises:
            TypeError: If any item in the list is not an instance of the Die class.
            ValueError: If not all dice have the same faces.
        """
```
Initializes the game with a list of Die objects.
*  ```play(n_rolls: int)```
```python
"""
        Roll all dice for a specified number of times and store the result.

        Args:
            n_rolls (int): Number of times to roll the dice.
            
        Raises:
            ValueError: If `num_rolls` is not a positive integer.
        """
```
Rolls all dice n_rolls times. Results are stored internally.

*  ```show(form: str = 'wide') -> pd.DataFrame```
```python
"""
        Show the results of the most recent play.

        Args:
            form (str): Format of the returned DataFrame. Either 'wide' or 'narrow'.
                                  'wide' returns the DataFrame as-is (default).
                                  'narrow' returns a long-format version with three columns:
                                  Roll Number, Die Number, and Face.

        Returns:
            pd.DataFrame: A copy of the play results in the specified format.

        Raises:
            ValueError: If the `form` argument is not 'wide' or 'narrow'.
        """
```
Displays the results of the game.

**Parameters:**
    *  ```form```: Either ```"wide"``` (default) or ```"narrow"```.
        Returns: A DataFrame of results.

### Class: ```Analyzer```
```python
"""
    An Analyzer takes the results of a Game and computes descriptive statistics.

    Attributes:
        game (Game): A Game object.
        results
```
Analyzes the results of a played game.

**Methods:**
*  ```__init__(game: Game)```
```python
"""
"""
```
Initializes the analyzer with a Game object.
*  ```jackpot() -> int```
```python
"""
"""
```
Counts how many rolls had all dice show the same face.
    *  Returns: Integer count of jackpots.
*  ```combo() -> pd.DataFrame```
```python
"""
"""
```
Returns a DataFrame of combinations of faces rolled, with counts.
*  ```face_counts_per_roll() -> pd.DataFrame```
```python
"""
"""
```
Returns a DataFrame of how many times each face appeared in each roll.

## Running Tests
To run all tests, run the following command from the root directory of the project:
```python
python -m unittest tests.test_montecarlo
```

### Author
Shriya Kuruba
GitHub: shriyakuruba
Email: ewu9af@virginia.edu