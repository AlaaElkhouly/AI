#_________________________________________EXPECTED MINIMAX CODE_______________________________________________________
import random
def randomization(col):
    #col=int(input("col?"))
    random_float = round(random.uniform(0, 1), 1) # lower & upper Limit, and  decimal place
    if col==0:
        if random_float>=0.4:
            col=0
        else: col=1
    elif col==6:
        if random_float>=0.4:
            col=6
        else: col=5
    else:
        if random_float>=0.8:
            col+=1
        elif random_float>=0.2:
            col=col
        else:
            col-=1
    return col