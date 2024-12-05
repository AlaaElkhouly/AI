import random
def get_probabilities(column):
        if column == 0:
            return {0: 0.6, 1: 0.4}
        elif column == 6:
            return {6: 0.6, 5: 0.4}
        else:
            return {column - 1: 0.2, column: 0.6, column + 1: 0.2}
        
def expecticol(column):
        rand = random.random()
        if column==0:
            if rand<= 0.4:
                ecol=1
            else:
                ecol=0 
        elif column==6:
            if rand<= 0.4:
                ecol=5
            else:
                ecol=6
        else:
            if rand<=0.2:
                ecol=column-1
            elif rand<=0.8:
                 ecol=column
            else:
                 ecol=column+1     
        return ecol

    

while 1:
     print(expecticol(int(input("col?"))))