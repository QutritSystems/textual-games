#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Battleship Core Logic
This module contains the pure game state, independent of any UI framework.
"""

from __future__ import annotations
from enum import Enum
from typing import List, Tuple, Set
from dataclasses import dataclass, field

class CellState(Enum):
    """網格單元狀態 (Grid Cell State)"""
    EMPTY = "~"      # 空白水域 (Empty Water)
    SHIP = "S"       # 船隻 (Ship)
    HIT = "X"        # 命中 (Hit)
    MISS = "o"       # 未命中 (Miss)
    SUNK = "#"       # 沉船 (Sunk Ship)

class GamePhase(Enum):
    """遊戲階段 (Game Phase)"""
    SETUP = "setup"
    BATTLE = "battle" 
    GAME_OVER = "game_over"

class GameMode(Enum):
    """遊戲模式 (Game Mode)"""
    MANUAL = "manual"
    AI_VS_AI = "ai_vs_ai"

class Orientation(Enum):
    """船隻方向 (Ship Orientation)"""
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"

@dataclass
class Ship:
    """船隻類別 (Ship Class)"""
    name: str
    size: int
    positions: List[Tuple[int, int]] = field(default_factory=list)
    hits: Set[Tuple[int, int]] = field(default_factory=set)
    
    @property
    def is_sunk(self) -> bool:
        return len(self.hits) >= self.size
    
    def hit(self, position: Tuple[int, int]) -> bool:
        if position in self.positions:
            self.hits.add(position)
            return True
        return False

class GameBoard:
    """遊戲棋盤 (Game Board)"""
    
    def __init__(self, size: int = 10):
        self.size = size
        self.grid = [[CellState.EMPTY for _ in range(size)] for _ in range(size)]
        self.ships: List[Ship] = []
        self.ship_positions: Set[Tuple[int, int]] = set()
    
    def is_valid_position(self, row: int, col: int, ship_size: int, orientation: Orientation) -> bool:
        if ship_size <= 0 or not (0 <= row < self.size and 0 <= col < self.size):
            return False

        if orientation == Orientation.HORIZONTAL:
            if col + ship_size > self.size:
                return False
            positions = [(row, col + i) for i in range(ship_size)]
        elif orientation == Orientation.VERTICAL:
            if row + ship_size > self.size:
                return False
            positions = [(row + i, col) for i in range(ship_size)]
        else:
            return False
        
        # Check collision and 1-cell distance rule
        for pos_row, pos_col in positions:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    check_row, check_col = pos_row + dr, pos_col + dc
                    if (0 <= check_row < self.size and 0 <= check_col < self.size and
                        (check_row, check_col) in self.ship_positions):
                        return False
        return True
    
    def place_ship(self, ship: Ship, row: int, col: int, orientation: Orientation) -> bool:
        if ship.size <= 0:
            return False

        if not self.is_valid_position(row, col, ship.size, orientation):
            return False
        
        if orientation == Orientation.HORIZONTAL:
            positions = [(row, col + i) for i in range(ship.size)]
        else:
            positions = [(row + i, col) for i in range(ship.size)]
        
        ship.positions = positions
        self.ships.append(ship)
        for pos in positions:
            self.ship_positions.add(pos)
            self.grid[pos[0]][pos[1]] = CellState.SHIP
        
        return True
    
    def attack(self, row: int, col: int) -> CellState:
        if not (0 <= row < self.size and 0 <= col < self.size):
            raise ValueError(f"Attack position out of bounds: ({row}, {col})")

        if self.grid[row][col] in [CellState.HIT, CellState.MISS, CellState.SUNK]:
            raise ValueError(f"Position already attacked: ({row}, {col})")
        
        for ship in self.ships:
            if ship.hit((row, col)):
                self.grid[row][col] = CellState.HIT
                if ship.is_sunk:
                    for pos in ship.positions:
                        self.grid[pos[0]][pos[1]] = CellState.SUNK
                    return CellState.SUNK
                return CellState.HIT
        
        self.grid[row][col] = CellState.MISS
        return CellState.MISS
    
    def all_ships_sunk(self) -> bool:
        return bool(self.ships) and all(ship.is_sunk for ship in self.ships)
