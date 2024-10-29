class Node:
    def ___init__(self,board,parent=None,move=None,depth=0,cost=0):
        self.board=board  #define the current states
        self.parent=parent #meen el parent node 
        self.move=move  # move made 3lshan awsal
        self.depth=depth #number of moves g(n)
        self.cost=cost # the estimated cost f(n)=g(n)+h(n)
    