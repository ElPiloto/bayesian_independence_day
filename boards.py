from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple, Set, Optional
import numpy as np
import pytensor as pt

@dataclass
class Position:
  row: int
  col: int
  
  def __eq__(self, other):
    return self.row == other.row and self.col == other.col
    
  def __hash__(self):
    return hash((self.row, self.col))


class BoardGame(ABC):
  @abstractmethod
  def get_alien_start(self) -> Position:
    pass
  
  @abstractmethod
  def get_human_start(self) -> Position:
    pass
  
  @abstractmethod
  def get_possible_moves_alien(self, pos: Position) -> Set[Position]:
    pass
  
  @abstractmethod
  def get_possible_moves_human(self, pos: Position) -> Set[Position]:
    pass
  
  @abstractmethod
  def is_silent_sector(self, pos: Position) -> bool:
    pass
  
  @abstractmethod
  def is_dangerous_sector(self, pos: Position) -> bool:
    pass


class GridBoard(BoardGame):
  """Boards that can be represented as ASCII."""

  def __init__(self, board_str: str):
    self.board = np.array([list(row) for row in board_str.strip().split('\n')])
    self.rows, self.cols = self.board.shape
    
    alien_pos = np.where(self.board == 'A')
    human_pos = np.where(self.board == 'H')
    
    if len(alien_pos[0]) != 1 or len(human_pos[0]) != 1:
      raise ValueError("Board must have exactly one alien start (A) and one human start (H)")
    
    self.alien_start = Position(alien_pos[0][0], alien_pos[1][0])
    self.human_start = Position(human_pos[0][0], human_pos[1][0])
    
    # Replace A and H with their underlying sector type (assuming they're in normal sectors)
    self.board[alien_pos] = '.'
    self.board[human_pos] = '.'
  
  def get_alien_start(self) -> Position:
    return self.alien_start
  
  def get_human_start(self) -> Position:
    return self.human_start
  
  def _is_valid_position(self, pos: Position) -> bool:
    in_bounds = (0 <= pos.row < self.rows and 0 <= pos.col < self.cols)
    return in_bounds and pos != self.alien_start and pos != self.human_start
  
  def _get_adjacent_positions(self, pos: Position) -> Set[Position]:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
    
    adjacent = set()
    for dr, dc in directions:
      new_pos = Position(pos.row + dr, pos.col + dc)
      if self._is_valid_position(new_pos):
        adjacent.add(new_pos)
    return adjacent
  
  def get_possible_moves_alien(self, pos: Position) -> Set[Position]:
    moves = set()
    moves.update(self._get_adjacent_positions(pos))
    
    for adj_pos in list(moves):
      moves.update(self._get_adjacent_positions(adj_pos))
    
    moves.discard(pos)
    return moves
  
  def get_possible_moves_human(self, pos: Position) -> Set[Position]:
    return self._get_adjacent_positions(pos)
  
  def is_silent_sector(self, pos: Position) -> bool:
    return self.board[pos.row, pos.col] == 'S'
  
  def is_dangerous_sector(self, pos: Position) -> bool:
    return self.board[pos.row, pos.col] == 'D'
  
  def position_to_index(self, pos: Position) -> int:
    """Convert 2D position to 1D index for PyMC"""
    return pos.row * self.cols + pos.col
  
  def index_to_position(self, idx: int) -> Position:
    """Convert 1D index back to 2D position"""
    return Position(idx // self.cols, idx % self.cols)
  
  def get_movement_matrix_alien(self, pos_idx: int) -> np.ndarray:
    """Get probability distribution over possible next positions for alien"""
    pos = self.index_to_position(pos_idx)
    possible_moves = self.get_possible_moves_alien(pos)
    
    probs = np.ones(self.rows * self.cols) * 1e-5
    # probs = np.zeros(self.rows * self.cols)
    for move in possible_moves:
      probs[self.position_to_index(move)] = 1
    
    # Normalize
    if probs.sum() > 0:
      probs = probs / probs.sum()
    # print(f'{probs.shape=}')
    return probs
  
  def get_movement_matrix_human(self, pos_idx: int) -> np.ndarray:
    """Get probability distribution over possible next positions for human"""
    pos = self.index_to_position(pos_idx)
    possible_moves = self.get_possible_moves_human(pos)
    
    probs = np.zeros(self.rows * self.cols)
    for move in possible_moves:
      probs[self.position_to_index(move)] = 1
    
    # Normalize
    if probs.sum() > 0:
      probs = probs / probs.sum()
    return probs

