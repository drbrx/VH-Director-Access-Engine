import random
from calculator import Calculator
from maze import Maze
from rockPaperScissors import RockPaperScissors
from ticTacToe import TicTacToe


pillars = {
    "L1": RockPaperScissors(),
    "L2": TicTacToe(),
    "R1": Calculator(),
    "R2": Maze(),
}

""" activePillar = random.choice(list(filter(lambda p: p.canReceive, pillars)))
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
activePillar.receive(inputPillar.input(input)) """

""" pillars["R2"].receive(pillars["L2"].input([1, 0, 0, 0]))
pillars["R1"].receive(pillars["R2"].input([4, 1, 1, 1, 4]))
pillars["L1"].receive(pillars["R1"].input([0, 0, 1, 1]))
pillars["L2"].receive(pillars["L1"].input(1))
pillars["R1"].receive(pillars["L2"].input([0, 1, 0, 0]))
pillars["L1"].receive(pillars["R1"].input([0, 0, 1, 0]))
pillars["R1"].receive(pillars["L1"].input(3))
pillars["R2"].receive(pillars["L1"].input(3))
pillars["L2"].receive(pillars["R2"].input([1, 1, 4]))
pillars["R2"].receive(pillars["L2"].input([0, 1, 0, 1]))
pillars["L2"].receive(pillars["R2"].input([1, 2, 1, 1, 4]))
pillars["L1"].receive(pillars["L2"].input([0, 0, 1, 0]))
pillars["R1"].input([0, 1, 1, 1]) """

s = "R2L2+1000/R1R2+41114/L1R1+0011/L2L1-1/R1L2+0100/L1R1+0010/R1L1-3/R2L1-3/L2R2+114/R2L2+0101/L2R2+12114/L1L2+0010/R1+0111"

for step in s.split("/"):
    if "+" in step:
        if step.split("+")[0].__len__() == 4:
            pillars[step[:2]].receive(
                pillars[step[2:4]].input(list(map(int, step.split("+")[1])))
            )
        else:
            pillars[step[:2]].input(list(map(int, step.split("+")[1])))
    else:
        if step.split("-")[0].__len__() == 4:
            pillars[step[:2]].receive(pillars[step[2:4]].input(int(step.split("-")[1])))
        else:
            pillars[step[:2]].input(int(step.split("-")[1]))

for pillar in pillars:
    if pillars[pillar].score == pillars[pillar].targetScore:
        print(pillar + " complete")
