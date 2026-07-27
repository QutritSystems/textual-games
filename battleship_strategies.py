import random
from typing import Tuple, Sequence, Union
from battleship_core import CellState

# Define a flexible return type supporting either (row, col) or ((row, col), "reason")
DecisionResult = Union[Tuple[int, int], Tuple[Tuple[int, int], str]]

def decide_attack_p1(grid_state: Sequence[Sequence[CellState]]) -> DecisionResult:
    """
    Decides the next coordinate for Player 1 (Left AI) to attack.
    Returns:
        ((row, col), "reasoning") or (row, col)
    """
    size = len(grid_state)
    valid_targets = []
    for r in range(size):
        for c in range(size):
            # The arena masks SHIP as EMPTY for the AI's view
            if grid_state[r][c] == CellState.EMPTY:
                valid_targets.append((r, c))
                
    if not valid_targets:
        return (0, 0), "無可用目標，預設轟炸 (0, 0)"
        
    # Baseline Strategy: Random Attack
    r, c = random.choice(valid_targets)
    return (r, c), f"發動「隨機探測」轟炸座標 ({r}, {c})。剩餘未探測區域: {len(valid_targets)} 格。"

def decide_attack_p2(grid_state: Sequence[Sequence[CellState]]) -> DecisionResult:
    """
    Decides the next coordinate for Player 2 (Right AI) to attack.
    """
    size = len(grid_state)
    valid_targets = []
    for r in range(size):
        for c in range(size):
            if grid_state[r][c] == CellState.EMPTY:
                valid_targets.append((r, c))
                
    if not valid_targets:
        return (0, 0), "無可用目標，預設轟炸 (0, 0)"
        
    # Simple Variation: Checkerboard Pattern (Parity)
    parity_targets = [(r, c) for r, c in valid_targets if (r + c) % 2 == 0]
    if parity_targets:
        r, c = random.choice(parity_targets)
        return (r, c), f"採用「奇偶效驗演算法」鎖定黑格 ({r}, {c})。偶數候選格剩餘: {len(parity_targets)} 格。"
    
    r, c = random.choice(valid_targets)
    return (r, c), f"偶數格已探測完畢，降級為「隨機掃描」轟炸 ({r}, {c})。"

# Keep the original for manual mode fallback/simplicity
def decide_attack(grid_state: Sequence[Sequence[CellState]]) -> DecisionResult:
    return decide_attack_p1(grid_state)
