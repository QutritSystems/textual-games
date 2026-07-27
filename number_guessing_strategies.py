import random
from typing import Tuple, List

def decide_guess(min_val: int, max_val: int, history: List[Tuple[int, str]]) -> Tuple[int, str]:
    """
    Decides the next guess based on the current valid range and previous guess history.
    
    This strategy can be hot-reloaded during the game!
    
    Args:
        min_val: The absolute minimum possible number (e.g. 1).
        max_val: The absolute maximum possible number (e.g. 100).
        history: A list of tuples of past guesses and their feedback, e.g. [(50, "high"), (25, "low")]
                 "high" means the guess was too high (secret is lower).
                 "low" means the guess was too low (secret is higher).
                 
    Returns:
        Tuple[int, str]: The next guess and the reasoning behind it.
    """
    # 💡 Compute current search space boundaries based on history
    current_min = min_val
    current_max = max_val
    
    for guess, result in history:
        if result == "high":
            current_max = min(current_max, guess - 1)
        elif result == "low":
            current_min = max(current_min, guess + 1)
            
    # Bounds check
    if current_min > current_max:
        current_min, current_max = min(min_val, current_max), max(max_val, current_min)
        
    # Baseline Strategy: Binary Search (The mathematically optimal search)
    next_guess = (current_min + current_max) // 2
    
    reasoning = (
        f"🤖 [二元搜尋法]: 根據歷史反饋，判定正確答案區間收縮為 [{current_min} ~ {current_max}]。"
        f"計算其中位數作為最優探測點：({current_min} + {current_max}) // 2 = {next_guess}。"
    )
    
    return next_guess, reasoning


# Alternative Strategy (for user to easily hot-swap and test):
def decide_guess_random(min_val: int, max_val: int, history: List[Tuple[int, str]]) -> Tuple[int, str]:
    """An alternative strategy that guesses randomly within the computed bounds."""
    current_min = min_val
    current_max = max_val
    
    for guess, result in history:
        if result == "high":
            current_max = min(current_max, guess - 1)
        elif result == "low":
            current_min = max(current_min, guess + 1)
            
    if current_min > current_max:
        return random.randint(min_val, max_val), "🤖 [隨機邊界]: 區間混亂，完全隨機猜測。"
        
    next_guess = random.randint(current_min, current_max)
    return next_guess, f"🤖 [隨機邊界法]: 鎖定區間 [{current_min} ~ {current_max}]，在此區間內隨機抽樣：{next_guess}。"
