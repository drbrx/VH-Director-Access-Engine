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

# base formula gen
for i in range(12):
    # Define two distinct elements for each pair
    variables[f"e1_{i}"] = Int(f"e1_{i}")
    variables[f"e2_{i}"] = Int(f"e2_{i}")
    constraints.append(variables[f"e1_{i}"] != variables[f"e2_{i}"])
    constraints.append(
        Or([variables[f"e1_{i}"] == element_map[elem] for elem in elements])
    )
    constraints.append(
        Or([variables[f"e2_{i}"] == element_map[elem] for elem in elements])
    )

    # Define suffixes for each element pair
    # True for "-", False for "+"
    variables[f"suffix_value_{i}"] = Int(f"suffix_value_{i}")

    # Constraints for suffix types
    constraints.append(
        If(
            variables[f"e2_{i}"] == element_map["L1"],
            And(
                variables[f"suffix_value_{i}"] >= 1, variables[f"suffix_value_{i}"] <= 3
            ),
            If(
                variables[f"e2_{i}"] == element_map["R2"],
                True,
                And(
                    variables[f"suffix_value_{i}"] >= 0,
                    variables[f"suffix_value_{i}"] <= 15,
                ),
            ),
        )
    )
# extra, final step gen
variables[f"e1_{12}"] = Int(f"e1_{12}")
constraints.append(
    Or([variables[f"e1_{12}"] == element_map[elem] for elem in elements])
)
variables[f"suffix_value_{12}"] = Int(f"suffix_value_{12}")

# Constraints for suffix types
constraints.append(
    If(
        variables[f"e2_{12}"] == element_map["L1"],
        And(variables[f"suffix_value_{12}"] >= 1, variables[f"suffix_value_{12}"] <= 3),
        If(
            variables[f"e1_{12}"] == element_map["R2"],
            True,  # TODO how do i deal with binary with zero in front?
            And(
                variables[f"suffix_value_{12}"] >= 0,
                variables[f"suffix_value_{12}"] <= 15,
            ),
        ),
    )
)

# full rule gen
solver.add(
    Sum([If(variables[f"e1_{i}"] == element_map["L1"], 1, 0) for i in range(13)]) == 3
)
solver.add(
    Sum([If(variables[f"e2_{i}"] == element_map["L1"], 1, 0) for i in range(12)]) == 3
)
solver.add(
    Sum([If(variables[f"e1_{i}"] == element_map["R1"], 1, 0) for i in range(13)]) == 3
)
solver.add(
    Sum([If(variables[f"e2_{i}"] == element_map["R1"], 1, 0) for i in range(12)]) == 3
)
solver.add(
    Sum([If(variables[f"e1_{i}"] == element_map["R2"], 1, 0) for i in range(13)]) == 3
)
solver.add(
    Sum([If(variables[f"e2_{i}"] == element_map["R2"], 1, 0) for i in range(12)]) == 3
)

solver.add(
    And(
        Sum(
            Sum(
                [
                    If(
                        Or(
                            variables[f"e2_{i}"] == element_map["L2"],
                            variables[f"e1_{i}"] == element_map["L2"],
                        ),
                        1,
                        0,
                    )
                    for i in range(12)
                ]
            ),
            If(
                Or(
                    variables[f"e1_{12}"] == element_map["L2"],
                ),
                1,
                0,
            ),
        )
        <= 8,
        Sum(
            Sum(
                [
                    If(
                        Or(
                            variables[f"e2_{i}"] == element_map["L2"],
                            variables[f"e1_{i}"] == element_map["L2"],
                        ),
                        1,
                        0,
                    )
                    for i in range(12)
                ]
            ),
            If(
                Or(
                    variables[f"e1_{12}"] == element_map["L2"],
                ),
                1,
                0,
            ),
        )
        >= 5,
    )
)

solver.add(constraints)
# print("\n\n".join(map(str, [solver.check(), solver.model()])))

for attempts in range(1000):
    if solver.check() == sat:
        model = solver.model()
        solution_string = ""
        for i in range(13):
            solution_string += (
                reverse_map[model.eval(variables[f"e1_{i}"]).as_long()]
                + (
                    reverse_map[model.eval(variables[f"e2_{i}"]).as_long()]
                    if i < 12
                    else ""
                )
                + (
                    "-"
                    if model.eval(variables[f"e{(1 if i ==12 else 2)}_{i}"])
                    == element_map["L1"]
                    else "+"
                )
                + str(model.eval(variables[f"suffix_value_{i}"]).as_long())
                + ("/" if i < 12 else "")
            )

        print("Generated solution:", solution_string)

        if simulate(solution_string):  # Assuming simulate() is defined elsewhere
            print("Valid solution found:", solution_string)
            break
        else:
            print("Invalid solution, adding constraint to avoid it")
            solver.add(
                Or(
                    [
                        variables[f"e1_{i}"] != model.eval(variables[f"e1_{i}"])
                        for i in range(12)
                    ]
                )
            )
    else:
        print("No further solutions exist that satisfy the constraints.")
        break
