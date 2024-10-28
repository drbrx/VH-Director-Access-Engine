import random
from calculator import Calculator
from maze import Maze
from rockPaperScissors import RockPaperScissors
from ticTacToe import TicTacToe


pillars = [Maze(), Calculator(), TicTacToe(), RockPaperScissors()]

activePillar = random.choice(list(filter(lambda p: p.canReceive, pillars)))
inputPillar = random.choice(
    list(filter(lambda p: p.canInput and p != activePillar, pillars))
)

input = []
for i in range(inputPillar.inputLen):
    input.append(random.choice(inputPillar.inputSym))

print(
    "Generated input for "
    + type(inputPillar).__name__
    + " (to "
    + type(activePillar).__name__
    + "): "
    + str(input)
)
activePillar.receive(inputPillar.input(input))
