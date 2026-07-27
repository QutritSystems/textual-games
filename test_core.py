from battleship_core import GameBoard, Ship, Orientation, CellState

board = GameBoard(10)
ship = Ship("TestShip", 3)
assert board.place_ship(ship, 0, 0, Orientation.HORIZONTAL)
assert board.grid[0][0] == CellState.SHIP
assert board.grid[0][1] == CellState.SHIP
assert board.grid[0][2] == CellState.SHIP

assert board.attack(0, 0) == CellState.HIT
assert board.attack(0, 1) == CellState.HIT
assert board.attack(0, 2) == CellState.SUNK

try:
    board.attack(0, 0)
except ValueError:
    pass
else:
    raise AssertionError("Repeated attacks must be rejected")

invalid_board = GameBoard(10)
assert not invalid_board.place_ship(Ship("Invalid", 2), -1, 0, Orientation.HORIZONTAL)
assert not invalid_board.place_ship(Ship("Invalid", 0), 0, 0, Orientation.HORIZONTAL)
assert not GameBoard(10).all_ships_sunk()

print("Core logic tests passed!")
