import random
from calculator import Calculator
from maze import Maze
from rockPaperScissors import RockPaperScissors
from ticTacToe import TicTacToe


pillars = [Maze(), Calculator(), TicTacToe(), RockPaperScissors()]

# activePillar = random.choice(list(filter(lambda p: p.canReceive, pillars)))
# inputPillar = random.choice(
#     list(filter(lambda p: p.canInput and p != activePillar, pillars))
# )

# input = []
# for i in range(inputPillar.inputLen):
#     input.append(random.choice(inputPillar.inputSym))

# print(
#     "Generated input for "
#     + type(inputPillar).__name__
#     + " (to "
#     + type(activePillar).__name__
#     + "): "
#     + str(input)
# )
# activePillar.receive(inputPillar.input(input))

pillars[0].receive(pillars[2].input([1, 0, 0, 0]))
pillars[1].receive(pillars[0].input([4, 1, 1, 1, 4]))
pillars[3].receive(pillars[1].input([0, 0, 1, 1]))
pillars[2].receive(pillars[3].input(1))
pillars[1].receive(pillars[2].input([0, 1, 0, 0]))
pillars[3].receive(pillars[1].input([0, 0, 1, 0]))
pillars[1].receive(pillars[3].input(3))
pillars[0].receive(pillars[3].input(3))
pillars[2].receive(pillars[0].input([1, 1, 4]))
pillars[0].receive(pillars[2].input([0, 1, 0, 1]))
pillars[2].receive(pillars[0].input([1, 2, 1, 1, 4]))
pillars[3].receive(pillars[2].input([0, 0, 1, 0]))
pillars[1].input([0, 1, 1, 1])

for i in range(4):
    if pillars[i].score != pillars[i].targetScore:
        print(str(i) + " incomplete")
