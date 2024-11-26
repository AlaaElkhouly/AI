import numpy as np

numofmoves=int(input("Please Enter Number of moves to be played:"))
r=6
c=7
board=np.zeros((r,c),dtype=int)
def terminal(board):
    if np.count_nonzero(board)==numofmoves : # insert end condition here
        return 1
    else:
        return 0

def minimax():
    if "depth==0 or" terminal(board)