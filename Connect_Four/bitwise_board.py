# bitwise repreentation of board
class board(self):
    self.player1=0
    self.player2=0
    self.height=[0]*7


    def drop_peice(self,player,column):
        mask=1<<(column*7 + self.height[column])
        if player==1:
            player1|=mask
        else:
            player2|=mask
