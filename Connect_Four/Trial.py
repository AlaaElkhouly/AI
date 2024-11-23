import numpy as np
def Heuristics2(r, c):
    # Create a blank matrix
    M = np.zeros((r, c), dtype=int)
    # Calculate center row and column
    cr = r // 2
    cc = c // 2
    # Fill the matrix with values based on proximity to the center
    for i in range(r):
        for j in range(c):
            # Manhattan distance from the center
            distance = abs(i - cr) + abs(j - cc)
            # Assign a higher value to squares closer to the center
            M[i][j] = (r + c) - distance
    return M
# r:row  cr:center row  c:coloumn   cc:center column
print(Heuristics2(7,7))