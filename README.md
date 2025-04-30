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
Represents a single die with customizable weights.

**Methods:**
*  ```__init__(faces: list)```
    Initializes the die with given face values. All weights default to 1.0.
*  ```change_weight(face, new_weight: float)```
    Changes the weight of a specific face.
    **Parameters:**
    *  face: The face value to modify.
    *  new_weight (float): New weight to assign.
        Raises: ValueError if face not found or weight is invalid.
*  ```roll(n_rolls: int = 1) -> list```
    Rolls the die n_rolls times and returns the outcomes.
*  ```show() -> pd.DataFrame```
    Returns a DataFrame of faces and their corresponding weights.

### Class: ```Game```
Represents a game with one or more dice.
**Methods:**
*  ```__init__(dice: list)```
    Initializes the game with a list of Die objects.
*  ```play(n_rolls: int)```
    Rolls all dice n_rolls times. Results are stored internally.
*  ```show(form: str = 'wide') -> pd.DataFrame```
    Displays the results of the game.
    **Parameters:**
    *  ```form```: Either ```"wide"``` (default) or ```"narrow"```.
        Returns: A DataFrame of results.

### Class: ```Analyzer```
Analyzes the results of a played game.

**Methods:**
*  ```__init__(game: Game)```
    Initializes the analyzer with a Game object.
*  ```jackpot() -> int```
    Counts how many rolls had all dice show the same face.
    Returns: Integer count of jackpots.
*  ```combo() -> pd.DataFrame```
    Returns a DataFrame of combinations of faces rolled, with counts.
*  ```face_counts_per_roll() -> pd.DataFrame```
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