# region imports and setup
import random
from calculator import Calculator
from maze import Maze
from rockPaperScissors import RockPaperScissors
from ticTacToe import TicTacToe
from z3 import *

z3.set_option(
    max_args=10000000, max_lines=1000000, max_depth=10000000, max_visited=1000000
)
MAX_TRIES = 2

path = "R2L2+1000/R1R2+41114/L1R1+0011/L2L1-1/R1L2+0100/L1R1+0010/R1L1-3/R2L1-3/L2R2+114/R2L2+0101/L2R2+12114/L1L2+0010/R1+0111"
# print(simulate(path))

elements = ["L1", "L2", "R1", "R2"]
element_map = {elem: i for i, elem in enumerate(elements)}
reverse_map = {i: elem for elem, i in element_map.items()}

solver = Solver()
variables = {}
constraints = []
# endregion

# region "Manual" simulation. Only for testing functionality of the simulation
""" pillars = {
    "L1": RockPaperScissors(),
    "L2": TicTacToe(),
    "R1": Calculator(),
    "R2": Maze(),
} 

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
activePillar.receive(inputPillar.input(input)) """
# endregion


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


# region Base formula gen
for i in range(13):
    # Define two distinct elements for each pair
    param = 2
    variables[f"e1_{i}"] = Int(f"e1_{i}")
    constraints.append(
        Or([variables[f"e1_{i}"] == element_map[elem] for elem in elements])
    )
    if i == 12:
        param = 1
    else:
        variables[f"e2_{i}"] = Int(f"e2_{i}")
        constraints.append(variables[f"e1_{i}"] != variables[f"e2_{i}"])
        constraints.append(
            Or([variables[f"e2_{i}"] == element_map[elem] for elem in elements])
        )

    # Define suffixes for each element pair
    variables[f"suffix_value_{i}"] = Array(f"suffix_value_{i}", IntSort(), IntSort())

    # Constraints for suffix types
    constraints.append(
        If(
            variables[f"e{param}_{i}"] == element_map["L1"],
            And(
                Select(variables[f"suffix_value_{i}"], 0) >= 1,
                Select(variables[f"suffix_value_{i}"], 0) <= 3,
                Select(variables[f"suffix_value_{i}"], 1) == -1,
            ),
            If(
                variables[f"e{param}_{i}"] == element_map["R2"],
                Or(
                    [
                        And(
                            Select(variables[f"suffix_value_{i}"], k) == -1,
                            And(
                                [
                                    And(
                                        Select(variables[f"suffix_value_{i}"], h) >= 1,
                                        Select(variables[f"suffix_value_{i}"], h) <= 4,
                                    )
                                    for h in range(k)
                                ]
                            ),
                            If(
                                i == 12,
                                Sum(
                                    [
                                        Select(variables[f"suffix_value_{i}"], h)
                                        for h in range(k)
                                    ]
                                )
                                <= 15,
                                If(
                                    variables[f"e1_{i}"] == element_map["L1"],
                                    Sum(
                                        [
                                            Select(variables[f"suffix_value_{i}"], h)
                                            for h in range(k)
                                        ]
                                    )
                                    <= 3,
                                    If(
                                        variables[f"e1_{i}"] == element_map["L2"],
                                        And(
                                            Sum(
                                                [
                                                    Select(
                                                        variables[f"suffix_value_{i}"],
                                                        h,
                                                    )
                                                    for h in range(k)
                                                ]
                                            )
                                            != 3,
                                            Sum(
                                                [
                                                    Select(
                                                        variables[f"suffix_value_{i}"],
                                                        h,
                                                    )
                                                    for h in range(k)
                                                ]
                                            )
                                            != 7,
                                            Sum(
                                                [
                                                    Select(
                                                        variables[f"suffix_value_{i}"],
                                                        h,
                                                    )
                                                    for h in range(k)
                                                ]
                                            )
                                            < 10,
                                        ),
                                        Sum(
                                            [
                                                Select(
                                                    variables[f"suffix_value_{i}"], h
                                                )
                                                for h in range(k)
                                            ]
                                        )
                                        <= 15,
                                    ),
                                ),
                            ),
                        )
                        for k in range(3, 16)
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
        ),
    )
# endregion

# region counter rule setup
L1Counter_1 = Int("L1Counter_1")
L1Counter_2 = Int("L1Counter_2")
solver.add(
    L1Counter_1
    == Sum([If(variables[f"e1_{i}"] == element_map["L1"], 1, 0) for i in range(13)]),
    L1Counter_1 >= 3,
    L1Counter_1 <= 4,
    L1Counter_2
    == Sum([If(variables[f"e2_{i}"] == element_map["L1"], 1, 0) for i in range(12)]),
    L1Counter_2 >= 2,
    L1Counter_2 <= 3,
    L1Counter_1 + L1Counter_2 == 6,
)

R1Counter_1 = Int("R1Counter_1")
R1Counter_2 = Int("R1Counter_2")
solver.add(
    R1Counter_1
    == Sum([If(variables[f"e1_{i}"] == element_map["R1"], 1, 0) for i in range(13)]),
    R1Counter_1 >= 3,
    R1Counter_1 <= 4,
    R1Counter_2
    == Sum([If(variables[f"e2_{i}"] == element_map["R1"], 1, 0) for i in range(12)]),
    R1Counter_2 >= 2,
    R1Counter_2 <= 3,
    R1Counter_1 + R1Counter_2 == 6,
)

R2Counter_1 = Int("R2Counter_1")
R2Counter_2 = Int("R2Counter_2")
solver.add(
    R2Counter_1
    == Sum([If(variables[f"e1_{i}"] == element_map["R2"], 1, 0) for i in range(13)]),
    R2Counter_1 >= 3,
    R2Counter_1 <= 4,
    R2Counter_2
    == Sum([If(variables[f"e2_{i}"] == element_map["R2"], 1, 0) for i in range(12)]),
    R2Counter_2 >= 2,
    R2Counter_2 <= 3,
    R2Counter_1 + R2Counter_2 == 6,
)

L2Counter = Int("L2Counter")
solver.add(
    L2Counter
    == Sum(
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
)
solver.add(And(L2Counter <= 8, L2Counter >= 5, L2Counter % 2 == 1))
# endregion

# region L1 ordering rule setup
solver.add(
    [
        Implies(
            variables[f"e1_{i}"] == element_map["L1"],
            Or(
                Or(
                    [
                        And(
                            variables[f"e2_{j}"] == element_map["L1"],
                            And(
                                [
                                    variables[f"e1_{k}"] != element_map["L1"]
                                    for k in range(i + 1, j)
                                ]
                            ),
                        )
                        for j in range(i + 1, 12)
                    ]
                ),
                Or(
                    [
                        And(
                            variables[f"e2_{j}"] == element_map["L1"],
                            And(
                                [
                                    variables[f"e1_{k}"] != element_map["L1"]
                                    for k in range(j, i)
                                ]
                            ),
                        )
                        for j in range(i)
                    ]
                ),
            ),
        )
        for i in range(13)
    ]
)
solver.add(
    [
        Implies(
            variables[f"e2_{i}"] == element_map["L1"],
            Or(
                Or(
                    [
                        And(
                            variables[f"e1_{j}"] == element_map["L1"],
                            And(
                                [
                                    variables[f"e2_{k}"] != element_map["L1"]
                                    for k in range(i + 1, j)
                                ]
                            ),
                        )
                        for j in range(i + 1, 13)
                    ]
                ),
                Or(
                    [
                        And(
                            variables[f"e1_{j}"] == element_map["L1"],
                            And(
                                [
                                    variables[f"e2_{k}"] != element_map["L1"]
                                    for k in range(j, i)
                                ]
                            ),
                        )
                        for j in range(i)
                    ]
                ),
            ),
        )
        for i in range(12)
    ]
)
# endregion

# region L2 ordering rule setup
solver.add(
    [
        Implies(
            variables[f"e1_{i}"] == element_map["L2"],
            Or(
                Or(
                    [
                        And(
                            variables[f"e2_{j}"] == element_map["L2"],
                            And(
                                [
                                    variables[f"e1_{k}"] != element_map["L2"]
                                    for k in range(i + 1, j)
                                ]
                            ),
                        )
                        for j in range(i + 1, 12)
                    ]
                ),
                Sum(
                    [
                        If(
                            Or(
                                variables[f"e{1 if j == 12 else 2}_{j}"]
                                == element_map["L2"],
                                variables[f"e1_{j}"] == element_map["L2"],
                            ),
                            1,
                            0,
                        )
                        for j in range(i + 1, 13)
                    ]
                )
                == 0,
            ),
        )
        for i in range(13)
    ]
)
solver.add(
    [
        Implies(
            variables[f"e2_{i}"] == element_map["L2"],
            Or(
                Or(
                    [
                        And(
                            variables[f"e1_{j}"] == element_map["L2"],
                            And(
                                [
                                    variables[f"e2_{k}"] != element_map["L2"]
                                    for k in range(i + 1, j)
                                ]
                            ),
                        )
                        for j in range(i + 1, 13)
                    ]
                ),
                Sum(
                    [
                        If(
                            Or(
                                variables[f"e{1 if j == 12 else 2}_{j}"]
                                == element_map["L2"],
                                variables[f"e1_{j}"] == element_map["L2"],
                            ),
                            1,
                            0,
                        )
                        for j in range(i + 1, 13)
                    ]
                )
                == 0,
            ),
        )
        for i in range(12)
    ]
)
solver.add(
    And(
        [
            Implies(
                variables[f"e1_{i}"] == element_map["L2"],
                Sum(
                    [
                        If(
                            variables[f"e2_{j}"] == element_map["L2"],
                            1,
                            0,
                        )
                        for j in range(i)
                    ]
                )
                > 0,
            )
            for i in range(13)
        ]
    )
)
# endregion

# region R1 ordering rule setup
solver.add(
    [
        Implies(
            variables[f"e2_{i}"] == element_map["R1"],
            Or(
                Or(
                    [
                        And(
                            variables[f"e1_{j}"] == element_map["R1"],
                            And(
                                [
                                    variables[f"e2_{k}"] != element_map["R1"]
                                    for k in range(i + 1, j)
                                ]
                            ),
                        )
                        for j in range(i + 1, 13)
                    ]
                ),
                Or(
                    [
                        And(
                            variables[f"e1_{j}"] == element_map["R1"],
                            And(
                                [
                                    variables[f"e2_{k}"] != element_map["R1"]
                                    for k in range(j, i)
                                ]
                            ),
                        )
                        for j in range(i)
                    ]
                ),
            ),
        )
        for i in range(12)
    ]
)
# endregion

# region R2 ordering rule setup
solver.add(
    [
        Implies(
            variables[f"e1_{i}"] == element_map["R2"],
            Or(
                Or(
                    [
                        And(
                            variables[f"e2_{j}"] == element_map["R2"],
                            And(
                                [
                                    variables[f"e1_{k}"] != element_map["R2"]
                                    for k in range(i + 1, j)
                                ]
                            ),
                        )
                        for j in range(i + 1, 12)
                    ]
                ),
                Sum(
                    [
                        If(
                            Or(
                                variables[f"e{1 if j == 12 else 2}_{j}"]
                                == element_map["R2"],
                                variables[f"e1_{j}"] == element_map["R2"],
                            ),
                            1,
                            0,
                        )
                        for j in range(i + 1, 13)
                    ]
                )
                == 0,
            ),
        )
        for i in range(13)
    ]
)
solver.add(
    [
        Implies(
            variables[f"e2_{i}"] == element_map["R2"],
            Or(
                Or(
                    [
                        And(
                            variables[f"e1_{j}"] == element_map["R2"],
                            And(
                                [
                                    variables[f"e2_{k}"] != element_map["R2"]
                                    for k in range(i + 1, j)
                                ]
                            ),
                        )
                        for j in range(i + 1, 13)
                    ]
                ),
                Sum(
                    [
                        If(
                            Or(
                                variables[f"e{1 if j == 12 else 2}_{j}"]
                                == element_map["R2"],
                                variables[f"e1_{j}"] == element_map["R2"],
                            ),
                            1,
                            0,
                        )
                        for j in range(i + 1, 13)
                    ]
                )
                == 0,
            ),
        )
        for i in range(12)
    ]
)
solver.add(
    And(
        [
            Implies(
                variables[f"e2_{i}"] == element_map["R2"],
                Sum(
                    [
                        If(
                            variables[f"e1_{j}"] == element_map["R2"],
                            1,
                            0,
                        )
                        for j in range(i)
                    ]
                )
                > 0,
            )
            for i in range(12)
        ]
    )
)
# endregion

solver.add(constraints)

# region encode/decode helpers
def encode(model):
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
    return solution_string


def decode(solution_string, solver):
    i = 0
    for step in solution_string.split("/"):
        solver.add(variables[f"e1_{i}"] == element_map[step[0:2]])
        if i < 12:
            solver.add(variables[f"e2_{i}"] == element_map[step[2:4]])
            val_start = 5
        else:
            val_start = 3
        j = 0
        for digit in step[val_start:]:
            solver.add(Select(variables[f"suffix_value_{i}"], j) == int(digit))
            j += 1
        solver.add(Select(variables[f"suffix_value_{i}"], j) == -1)
        i += 1

    return variables


# endregion

# region coherence check
solver.push()
decode(path, solver)
# print(solver.assertions())
if solver.check() == sat:
    model = solver.model()

    solution_string = encode(model)
    sim_result = simulate(solution_string)
    if sim_result == -1:  # Assuming simulate() is defined elsewhere
        print(
            "Coherence check passed with value:\n",
            solution_string,
            "\nTested value:\n",
            path,
        )
    else:
        print(f"Valid solution at coherence check. Simulation failed")
else:
    print(f"Invalid solution at coherence check")
solver.pop()
# endregion

# region solver
for attempts in range(MAX_TRIES):
    if solver.check() == sat:
        model = solver.model()

        solution_string = encode(model)

        print("Generated solution:", solution_string)
        sim_result = simulate(solution_string)
        if sim_result == -1:
            print("Valid solution found:", solution_string)
            break
        else:
            print(
                f"Invalid solution at attampt {attempts+1}/{MAX_TRIES}, adding constraint(s) to avoid it"
            )
            solver.add(
                Or(
                    variables[f"e1_{sim_result}"]
                    != model.eval(variables[f"e1_{sim_result}"]),
                    variables[f"e{1 if sim_result == 12 else 2}_{sim_result}"]
                    != model.eval(
                        variables[f"e{1 if sim_result == 12 else 2}_{sim_result}"]
                    ),
                    variables[f"suffix_value_{sim_result}"]
                    != model.eval(variables[f"suffix_value_{sim_result}"]),
                )
            )
    else:
        print("No further solutions exist that satisfy the constraints.")
        break
# endregion
