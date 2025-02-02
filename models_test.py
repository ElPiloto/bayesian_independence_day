from absl.testing import absltest
import models
import boards


class OracleModelTests(absltest.TestCase):

  def setUp(self):
    board_str = """ADDD
DDDD
DDDD
DSSH"""
    self.unambiguous_board = boards.GridBoard(board_str)


  def test_can_find_human(self):
    observations = [
        boards.Position(3, 3),
        boards.Position(2, 3),
        boards.Position(1, 3),
    ]
    om = models.OracleModel(self.unambiguous_board)
    model = om.create_model(observations)



if __name__ == '__main__':
  absltest.main()
