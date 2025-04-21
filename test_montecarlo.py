import unittest
import numpy as np
import pandas as pd

from montecarlo import Die, Game, Analyzer

class TestDie(unittest.TestCase):
    """
    Unit tests for the Die class.
    
    Tests:
        - Initialization and internal structure
        - Changing weight of a face
        - Rolling the die
        - Showing the faces and weights
    """

    def setUp(self):
        """Set up a standard 3-face die for testing."""
        self.faces = np.array([1, 2, 3])
        self.die = Die(self.faces)

    def test_init_structure(self):
        """
        Test that the Die object creates an internal DataFrame with proper structure.
        """
        self.assertIsInstance(self.die._df, pd.DataFrame)
        self.assertListEqual(sorted(self.die._df.columns.tolist()), ['weight'])

    def test_change_weight(self):
        """
        Test that change_weight correctly modifies the weight of a face.
        """
        self.die.change_weight(2, 5.0)
        self.assertEqual(self.die._df.loc[2, 'weight'], 5.0)

    def test_roll_output_type(self):
        """
        Test that roll returns a NumPy array of the correct length.
        """
        result = self.die.roll(5)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result), 5)

    def test_show_returns_dataframe(self):
        """
        Test that show returns a DataFrame with 'face' and 'weight' columns.
        """
        df = self.die.show()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn('face', df.columns)
        self.assertIn('weight', df.columns)


class TestGame(unittest.TestCase):
    """
    Unit tests for the Game class.

    Tests:
        - Playing a game and saving results
        - Showing results in wide and narrow format
    """

    def setUp(self):
        """Set up a simple 2-die game using coin faces."""
        faces = np.array(['H', 'T'])
        die1 = Die(faces)
        die2 = Die(faces)
        self.game = Game([die1, die2])

    def test_play_result_shape(self):
        """
        Test that the play method creates a result DataFrame with correct shape.
        """
        self.game.play(10)
        df = self.game._results
        self.assertEqual(df.shape, (10, 2))  # 10 rolls, 2 dice

    def test_show_wide_format(self):
        """
        Test that show('wide') returns a wide-format DataFrame.
        """
        self.game.play(5)
        result = self.game.show('wide')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape[1], 2)  # 2 dice columns

    def test_show_narrow_format(self):
        """
        Test that show('narrow') returns a long-format DataFrame with correct columns.
        """
        self.game.play(3)
        result = self.game.show('narrow')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(set(result.columns), {'roll_num', 'die', 'face'})


class TestAnalyzer(unittest.TestCase):
    """
    Unit tests for the Analyzer class.

    Tests:
        - Jackpot detection
        - Face count per roll structure
        - Combo frequency generation
        - Permutation frequency generation
    """

    def setUp(self):
        """Set up a game and analyzer for testing statistical properties."""
        faces = np.array([1, 2, 3])
        dice = [Die(faces) for _ in range(3)]
        self.game = Game(dice)
        self.game.play(20)
        self.analyzer = Analyzer(self.game)

    def test_jackpot_output(self):
        """
        Test that jackpot returns an integer (count of matching rolls).
        """
        result = self.analyzer.jackpot()
        self.assertIsInstance(result, int)

    def test_face_counts_per_roll_structure(self):
        """
        Test that face_counts_per_roll returns a DataFrame with roll count rows.
        """
        df = self.analyzer.face_counts_per_roll()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape[0], 20)

    def test_combo_returns_dataframe(self):
        """
        Test that combo returns a DataFrame with combinations and counts.
        """
        combo_df = self.analyzer.combo()
        self.assertIsInstance(combo_df, pd.DataFrame)
        self.assertIn('count', combo_df.columns)

    def test_permutation_returns_dataframe(self):
        """
        Test that permutation returns a DataFrame with permutations and counts.
        """
        perm_df = self.analyzer.permutation()
        self.assertIsInstance(perm_df, pd.DataFrame)
        self.assertIn('count', perm_df.columns)


if __name__ == '__main__':
    unittest.main()
