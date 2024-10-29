import math

#function for calculating the rculeadian distance

def manhattan(self):
    distance = 0
    for i in range(2):
        for j in range(2):
            if self.board[i][j] != 0: ##skip the zero
                x, y = divmod(self.board[i][j]-1, 3) ## dah el mkan el mafrood ykoon the curent box feeh
                distance += abs(x - i) + abs(y - j) ##sum all the distances needed ... 
    return distance

