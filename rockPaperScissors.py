from pillar import Pillar
from exceptions import FailStateException


class RockPaperScissors(Pillar):
    def __init__(self):
        self.canReceive = True
        self.canInput = True
        self.targetScore = 3
        self.score = 0
        self.inputLen = 1
        self.inputSym = [1, 2, 3]
        self.receiveLen = 0

        self.values = [None, None]

    def calculate(self):
        if (self.values[0] - 1) != (self.values[1] % 3):
            raise FailStateException("RockPaperScissors loss")

        self.values = [None, None]
        self.score += 1
        if self.score == self.targetScore:
            self.canReceive = False
            self.canInput = False

    def receive(self, symbols):
        input = super().receive(symbols)
        if input < 1 or input > 3:
            raise FailStateException(
                "RockPaperScissors invalid received: " + str(input)
            )
        self.values[1] = input

        if None not in self.values:
            self.calculate()

    def input(self, symbols):
        if symbols < 1 or symbols > 3:
            raise FailStateException("RockPaperScissors invalid input: " + str(symbols))
        self.values[0] = symbols

        if None not in self.values:
            self.calculate()

        return symbols
