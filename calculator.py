from pillar import Pillar
from exceptions import FailStateException


class CalculatorLevel:
    def __init__(self):
        self.operation = lambda a, b: None
        self.initialValue = [None, None, None, None]


class Calculator(Pillar):
    def __init__(self):
        self.canReceive = True
        self.canInput = True
        self.targetScore = 3
        self.score = 0
        self.inputLen = 4
        self.inputSym = [0, 1]
        self.receiveLen = 4

        self.levels = [CalculatorLevel(), CalculatorLevel(), CalculatorLevel()]

        self.levels[0].operation = lambda a, b: int(bool(a) and bool(b))
        self.levels[0].initialValue = [0, 1, 1, 1]
        self.levels[1].operation = lambda a, b: int(
            (bool(a) or bool(b)) and not (bool(a) and bool(b))
        )
        self.levels[1].initialValue = [0, 1, 1, 0]
        self.levels[2].operation = lambda a, b: int(bool(a) or bool(b))
        self.levels[2].initialValue = [0, 1, 1, 0]

        self.values = [[], []]

    def calculate(self):
        for i in range(4):
            if (
                self.levels[self.score].operation(
                    self.levels[self.score].initialValue[i], self.values[0][i]
                )
                != self.values[1][i]
            ):
                raise FailStateException(
                    "Calculator mismatch on bit "
                    + str(i)
                    + " of level "
                    + str(self.score)
                )
        self.values = [[], []]
        self.score += 1
        if self.score == self.targetScore:
            self.canReceive = False
            self.canInput = False

    def receive(self, symbols):
        self.values[0] = super().receive(symbols)
        if self.values[0] != [] and self.values[1] != []:
            self.calculate()

    def input(self, symbols):
        self.values[1] = symbols
        if self.values[0] != [] and self.values[1] != []:
            self.calculate()
        return symbols
