from pillar import Pillar
from exceptions import FailStateException


class TicTacToe(Pillar):
    def __init__(self):
        self.canReceive = False
        self.canInput = True
        self.targetScore = 1
        self.score = 0
        self.inputLen = 4
        self.inputSym = [0, 1]
        self.receiveLen = 4

        self.grid = [
            [None, None, None],
            [None, None, None],
            [None, None, 0],
        ]

    def calculate(self):
        winner = None
        for i in range(3):
            if self.grid[i][0] == self.grid[i][1] == self.grid[i][2] != None:
                return self.grid[i][0]
            if self.grid[0][i] == self.grid[1][i] == self.grid[2][i] != None:
                winner = self.grid[0][i]

        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != None:
            winner = self.grid[0][0]

        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != None:
            winner = self.grid[0][2]

        match winner:
            case 0:
                raise FailStateException("TicTacToe lost")
            case 1:
                self.score += 1
                self.canReceive = False
                self.canInput = False
            case None:
                for i in range(3):
                    for j in range(3):
                        if self.grid[i][j] == None:
                            return
                raise FailStateException("TicTacToe draw")

    def receive(self, symbols):
        input = super().receive(symbols)
        i = (input[0] * 2) + (input[1] * 1)
        j = (input[2] * 2) + (input[3] * 1)
        if i > 2 or j > 2:
            raise FailStateException("Invalid TicTacToe coords received: " + str(input))
        if self.grid[j][i] != None:
            raise FailStateException(
                "Invalid TicTacToe coords received, attempted overwrite operation: "
                + str(input)
            )
        self.grid[j][i] = 0
        self.calculate()
        self.canReceive = False
        self.canInput = True

    def input(self, symbols):
        i = (symbols[0] * 2) + (symbols[1] * 1)
        j = (symbols[2] * 2) + (symbols[3] * 1)
        if i > 2 or j > 2:
            raise FailStateException("Invalid TicTacToe coords input: " + str(symbols))
        if self.grid[j][i] != None:
            raise FailStateException(
                "Invalid TicTacToe coords inputed, attempted overwrite operation: "
                + str(input)
            )
        self.grid[j][i] = 1
        self.calculate()
        self.canReceive = False
        self.canInput = True
        return symbols
