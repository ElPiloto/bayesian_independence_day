import numpy as np
import pymc as pm
import pytensor as pt

import boards


class OracleModel():
  """Simple version of game where agents announce their true location."""

  def __init__(self, board: boards.GridBoard):
    self.board = board


  def create_model(self, observations: list[boards.Position]):
    board_size = self.board.rows * self.board.cols
    num_turns = len(observations)
    with pm.Model() as model:
      is_alien = pm.Bernoulli('is_alien', p=0.5)

      locations = []

      # First turn: deterministic starting position based on player type
      alien_start_idx = self.board.position_to_index(self.board.get_alien_start())
      human_start_idx = self.board.position_to_index(self.board.get_human_start())
      
      locations.append(
        pm.Deterministic('location_0', 
                        pm.math.switch(is_alien, alien_start_idx, human_start_idx))
      )

      for t in range(1, num_turns):
        print(t)
        prev_loc = locations[t-1]

        # Get movement matrices for current position
        move_probs_alien = pt.shared(np.stack([
          self.board.get_movement_matrix_alien(i) for i in range(board_size)
        ]))
        move_probs_human = pt.shared(np.stack([
          self.board.get_movement_matrix_human(i) for i in range(board_size)
        ]))

        
        # Select appropriate movement matrix based on player type
        possible_moves = pm.math.switch(
          is_alien,
          move_probs_alien[prev_loc],
          move_probs_human[prev_loc]
        )

        # Current location probability distribution
        loc_t = pm.Categorical(f'location_{t}', 
                             p=possible_moves,
                             shape=1)
        locations.append(loc_t)
      return model




