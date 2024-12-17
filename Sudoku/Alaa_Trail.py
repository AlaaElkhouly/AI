#set of variables places 1-81
#domain list of possible values to fill variables with [1-9]
#constraints rules that do not allow you to assign some of the values to the variables
from collections import defaultdict

def cross(A, B):
    return [a + b for a in A for b in B]

# Define the board
rows = 'ABCDEFGHI'
cols = '123456789'
squares = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])
units = {s: [u for u in unitlist if s in u] for s in squares}
peers = {s: set(sum(units[s], [])) - {s} for s in squares}

def parse_grid(grid):
    """Convert grid to a dict of possible values, {square: digits}, or return False if a contradiction is detected."""
    values = {s: cols for s in squares}
    for s, d in grid_values(grid).items():
        if d in cols and not assign(values, s, d):
            return False
    return values

def grid_values(grid):
    """Convert grid into a dict of {square: char} with '0' or '.' for empties."""
    chars = [c if c in cols else '0' for c in grid]
    assert len(chars) == 81
    return dict(zip(squares, chars))

def assign(values, s, d):
    """Eliminate all other values (except d) from values[s] and propagate.
    Return values, or False if a contradiction is detected."""
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False

def eliminate(values, s, d):
    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values, or False if a contradiction is detected."""
    if d not in values[s]:
        return values  # Already eliminated
    values[s] = values[s].replace(d, '')
    if len(values[s]) == 0:
        return False  # Contradiction: removed last value
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False
        elif len(dplaces) == 1:
            if not assign(values, dplaces[0], d):
                return False
    return values

def search(values):
    """Using depth-first search and propagation, try all possible values."""
    if values is False:
        return False  # Failed earlier
    if all(len(values[s]) == 1 for s in squares):
        return values  # Solved!
    # Choose the unfilled square s with the fewest possibilities
    n, s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d)) for d in values[s])

def some(seq):
    """Return some element of seq that is true."""
    for e in seq:
        if e:
            return e
    return False

def display(values):
    """Display these values as a 2-D grid."""
    width = 1 + max(len(values[s]) for s in squares)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    print()

def solve(grid):
    return search(parse_grid(grid))

# Example usage
if __name__ == "__main__":
    puzzle = '790013600400070300100240975500600207070001800806920500601002053300000409024035000'
    print("Original Sudoku Puzzle:")
    display(grid_values(puzzle))

    print("\nSolved Sudoku Puzzle:")
    solution = solve(puzzle)
    if solution:
        display(solution)
    else:
        print("No solution exists.")
