from absl.testing import absltest
import models
import boards
import pymc as pm
import numpy as np


class OracleModelTests(absltest.TestCase):

  def setUp(self):
    board_str = """ADDD
DDDD
DDDD
DSSH"""
    self.unambiguous_board = boards.GridBoard(board_str)


  def test_can_find_human(self):
    human_obs = [
        boards.Position(2, 3),  # First move is near human corner
        boards.Position(1, 3),
    ]
    observations = [
        self.unambiguous_board.position_to_index(o) for o in human_obs
    ]
    om = models.OracleModel(self.unambiguous_board)
    model = om.create_model(observations)

    with model:
      trace = pm.sample(1000, tune=1000)
      self.assertEqual(trace.posterior['is_alien'].mean().item(), 0)

  def test_can_find_alien(self):
    alien_obs = [
        boards.Position(0, 1),  # First move is near alien corner
        boards.Position(0, 2),
    ]
    observations = [
        self.unambiguous_board.position_to_index(o) for o in alien_obs
    ]
    om = models.OracleModel(self.unambiguous_board)
    model = om.create_model(observations)

    with model:
      trace = pm.sample(1000, tune=1000)
      self.assertEqual(trace.posterior['is_alien'].mean().item(), 1)



if __name__ == '__main__':
  absltest.main()
