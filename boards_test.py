"""Tests for board.py."""
from absl.testing import absltest
import boards


class GridsTests(absltest.TestCase):

  def setUp(self):
    board_str = (
        "ADDD\n"
        "DDDD\n"
        "DDDD\n"
        "DSSH\n"
    )
    self.board = boards.GridBoard(board_str)

  def test_starts_invalid(self):
    self.assertFalse(self.board._is_valid_position(self.board.alien_start))
    self.assertFalse(self.board._is_valid_position(self.board.human_start))

  def test_human_possible_moves(self):
    self.assertLen(
        self.board.get_possible_moves_human(self.board.human_start),
        2,
        "Should only have two possible starting moves."
    )

  def test_alien_possible_moves(self):
    print(self.board.get_possible_moves_alien(self.board.alien_start))
    breakpoint()
    self.assertLen(
        self.board.get_possible_moves_alien(self.board.alien_start),
        5,
        "Should only have two possible starting moves."
    )

  def test_probabilities(self):
    human_probs = self.board.get_movement_matrix_human(
        self.board.position_to_index(self.board.human_start)
    )
    alien_probs = self.board.get_movement_matrix_alien(
        self.board.position_to_index(self.board.alien_start)
    )
    with self.subTest("Probabilities match."):
      self.assertEqual(human_probs.shape, alien_probs.shape)


if __name__ == '__main__':
  absltest.main()
