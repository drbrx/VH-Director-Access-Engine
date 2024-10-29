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
# translates to
s = "R2L2+1000/R1R2+41114/L1R1+0011/L2L1-1/R1L2+0100/L1R1+0010/R1L1-3/R2L1-3/L2R2+114/R2L2+0101/L2R2+12114/L1L2+0010/R1+0111"

"""
3 L1XX:1|2|3 >< XXL1:1|2|3
    x->x"-1" | x"+1"<-x
        = 3*1 + 3*1 + 3*1 = 9
<9 tot of, with no reps:
    L2XX!1010!11xx!xx11
    XXL2!1010!11xx!xx11
        = 8! = 40320
3 R1XX >< XXR1 (y = !x)
    xxxx - xxxx - xxxx
    0xxx - xyyx - x11x
        = 1*2^4 + 1*2^4 + 1*2^4 = 48
3 R2XX>=0101-0011-0101 -> XXR2
    = (10*[4 (24)* 1 (31)* 1 (3311)* 1 (333111)* 4])
    + (12*[1 (31)* 1 (31)* (3311)* 4])
    + (10*[1 (31)* 2 (4 (31)* 2)* 1 (3 (4 (31)* 2)* 1)* 1 (33 (4 (31)* 2)* 11)* 4])
        =
"""

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
