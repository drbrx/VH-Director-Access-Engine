import random
from calculator import Calculator
from maze import Maze
from rockPaperScissors import RockPaperScissors
from ticTacToe import TicTacToe
from z3 import *


""" pillars = {
    "L1": RockPaperScissors(),
    "L2": TicTacToe(),
    "R1": Calculator(),
    "R2": Maze(),
} """

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


def simulate(s):
    pillars = {
        "L1": RockPaperScissors(),
        "L2": TicTacToe(),
        "R1": Calculator(),
        "R2": Maze(),
    }

    try:
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
                    pillars[step[:2]].receive(
                        pillars[step[2:4]].input(int(step.split("-")[1]))
                    )
                else:
                    pillars[step[:2]].input(int(step.split("-")[1]))
    except:
        return False

    for pillar in pillars:
        if pillars[pillar].score != pillars[pillar].targetScore:
            print(pillar + " incomplete")
            return False

    return True


path = "R2L2+1000/R1R2+41114/L1R1+0011/L2L1-1/R1L2+0100/L1R1+0010/R1L1-3/R2L1-3/L2R2+114/R2L2+0101/L2R2+12114/L1L2+0010/R1+0111"
# print(simulate(path))

elements = ["L1", "L2", "R1", "R2"]
element_map = {elem: i for i, elem in enumerate(elements)}
reverse_map = {i: elem for elem, i in element_map.items()}

solver = Solver()
variables = {}
constraints = []

for i in range(12):
    # Define two distinct elements for each pair
    e1 = Int(f"e1_{i}")
    variables[f"e1_{i}"] = e1
    e2 = Int(f"e2_{i}")
    variables[f"e2_{i}"] = e2
    constraints.append(e1 != e2)
    constraints.append(Or([e1 == element_map[elem] for elem in elements]))
    constraints.append(Or([e2 == element_map[elem] for elem in elements]))

    # Define suffixes for each element pair
    suffix_type = Bool(f"suffix_type_{i}")  # True for "-", False for "+"
    variables[f"suffix_type_{i}"] = suffix_type
    suffix_value = Int(f"suffix_value_{i}")
    variables[f"suffix_value_{i}"] = suffix_value

    # Constraints for suffix types
    constraints.append(
        If(
            suffix_type,
            And(suffix_value >= 1, suffix_value <= 3),
            And(suffix_value >= 0, suffix_value <= 15),
        )
    )

solver.add(constraints)

print("\n\n".join(map(str, [solver.check(), solver.model()])))
part = "R2L2+1000/R1R2+41114/L1R1+0011/L2L1-1/R1L2+0100/L1R1+0010/R1L1-3/R2L1-3/L2R2+114/R2L2+0101/L2R2+12114/L1L2+0010/R1+0"

for attempts in range(1000):
    if solver.check() == sat:
        model = solver.model()
        solution_string = ""
        for i in range(12):
            solution_string += (
                model.eval(variables[f"e1_{i}"])
                + model.eval(variables[f"e2_{i}"])
                + ("-" if model.eval(variables[f"suffix_type_{i}"]) else "+")
                + model.eval(variables[f"suffix_value_{i}"])
                + ("/" if i != 11 else "")
            )
        print(solution_string)
        if simulate(solution_string):
            print("Valid solution found:", solution_string, " -> ", solver.model())
            break
        else:
            print("Failed:", solution_string, " -> ", solver.model())
            solver.add(Or([var != model.evaluate(var) for var in [x, y, z]]))
    else:
        print("No further solutions exist that satisfy the constraints.")
        break
