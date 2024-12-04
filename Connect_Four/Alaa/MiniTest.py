import random
def expecticol( column):
    if column == 0:
        probabilities={0: 0.6, 1: 0.4}
    elif column == 6:
        probabilities={6: 0.6, 5: 0.4}
    else:
        probabilities={column - 1: 0.2, column: 0.6, column + 1: 0.2}
    rand = random.random()
    cumulative_probability = 0
    for key, probability in probabilities.items():
        cumulative_probability += probability
        if rand < cumulative_probability:
            ecol = key
    return ecol
