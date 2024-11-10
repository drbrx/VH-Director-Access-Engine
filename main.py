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

    step_idx = -1
    try:
        step_idx += 1
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
        return step_idx

    for pillar in pillars:
        if pillars[pillar].score != pillars[pillar].targetScore:
            print(pillar + " incomplete")
            return False

    return -1


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
    variables[f"suffix_value_{i}"] = Array(f"suffix_value_{i}", IntSort(), IntSort())

    # Constraints for suffix types
    constraints.append(
        If(
            variables[f"e2_{i}"] == element_map["L1"],
            And(
                [
                    And(
                        Select(variables[f"suffix_value_{i}"], j) >= 1,
                        Select(variables[f"suffix_value_{i}"], j) <= 3,
                        Select(variables[f"suffix_value_{i}"], 1) == -1,
                    )
                    for j in range(1)
                ]
            ),
            If(
                variables[f"e2_{i}"] == element_map["R2"],
                And(
                    [
                        And(
                            Select(variables[f"suffix_value_{i}"], j) >= 1,
                            Select(variables[f"suffix_value_{i}"], j) <= 4,
                            Or(
                                [
                                    Select(variables[f"suffix_value_{i}"], k) == -1
                                    for k in range(4, 15)
                                ]
                            ),
                        )
                        for j in range(4)
                    ]
                ),
                And(
                    [
                        And(
                            Select(variables[f"suffix_value_{i}"], j) >= 0,
                            Select(variables[f"suffix_value_{i}"], j) <= 1,
                            Select(variables[f"suffix_value_{i}"], 4) == -1,
                        )
                        for j in range(4)
                    ]
                ),
            ),
        )
    )
# extra, final step gen
variables[f"e1_{12}"] = Int(f"e1_{12}")
constraints.append(
    Or([variables[f"e1_{12}"] == element_map[elem] for elem in elements])
)
variables[f"suffix_value_{12}"] = Array(f"suffix_value_{12}", IntSort(), IntSort())

# Constraints for suffix types
constraints.append(
    If(
        variables[f"e1_{12}"] == element_map["L1"],
        And(
            [
                And(
                    Select(variables[f"suffix_value_{12}"], j) >= 1,
                    Select(variables[f"suffix_value_{12}"], j) <= 3,
                    Select(variables[f"suffix_value_{12}"], 1) == -1,
                )
                for j in range(1)
            ]
        ),
        If(
            variables[f"e1_{12}"] == element_map["R2"],
            And(
                [
                    And(
                        Select(variables[f"suffix_value_{12}"], j) >= 1,
                        Select(variables[f"suffix_value_{12}"], j) <= 4,
                        Or(
                            [
                                Select(variables[f"suffix_value_{12}"], k) == -1
                                for k in range(4, 15)
                            ]
                        ),
                    )
                    for j in range(4)
                ]
            ),
            And(
                [
                    And(
                        Select(variables[f"suffix_value_{12}"], j) >= 0,
                        Select(variables[f"suffix_value_{12}"], j) <= 1,
                        Select(variables[f"suffix_value_{12}"], 4) == -1,
                    )
                    for j in range(4)
                ]
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

MAX_TRIES = 1000
for attempts in range(MAX_TRIES):
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
            )

            j = 0
            while True:
                value = model.eval(Select(variables[f"suffix_value_{i}"], j)).as_long()
                if value == -1:
                    break
                solution_string += str(value)
                j += 1

            solution_string += "/" if i < 12 else ""

        print("Generated solution:", solution_string)
        sim_result = simulate(solution_string)
        if sim_result == -1:  # Assuming simulate() is defined elsewhere
            print("Valid solution found:", solution_string)
            break
        else:
            print(
                f"Invalid solution at attampt {attempts}/{MAX_TRIES}, adding constraint(s) to avoid it"
            )
            for step in range(sim_result):
                solver.add(
                    Or(
                        variables[f"e1_{step}"] != model.eval(variables[f"e1_{step}"]),
                        variables[f"e{1 if step == 12 else 2}_{step}"]
                        != model.eval(variables[f"e{1 if step == 12 else 2}_{step}"]),
                        variables[f"suffix_value_{step}"]
                        != model.eval(variables[f"suffix_value_{step}"]),
                    )
                )
    else:
        print("No further solutions exist that satisfy the constraints.")
        break
