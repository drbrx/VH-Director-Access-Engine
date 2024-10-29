from pillar import Pillar
from exceptions import FailStateException


class MazeLevel:
    def __init__(self):
        self.grid = [[], [], []]
        self.pos = []


class Maze(Pillar):

    def __init__(self):
        self.canReceive = True
        self.canInput = False
        self.targetScore = 3
        self.score = 0
        self.imputLen = None
        self.inputSym = [1, 2, 3, 4]
        self.receiveLen = 0

        self.levels = [MazeLevel(), MazeLevel(), MazeLevel()]

        self.levels[0].grid = [
            [False, False, False, None],
            [None, None, None, None],
            [True, False, False, False],
        ]
        self.levels[0].pos = [0, 3]
        self.levels[1].grid = [
            [False, False, False, False],
            [False, None, None, None],
            [False, True, False, False],
        ]
        self.levels[1].pos = [1, 3]
        self.levels[2].grid = [
            [False, False, False, False],
            [None, None, None, False],
            [True, False, None, None],
        ]
        self.levels[2].pos = [2, 3]

    def calculate(self):
        pass

    def receive(self, symbols):
        self.inputLen = super().receive(symbols)
        self.canInput = True

    def input(self, symbols):
        nRead = 0
        for val in symbols:
            match val:
                case 1:
                    self.levels[self.score].pos[1] -= 1
                case 2:
                    self.levels[self.score].pos[0] -= 1
                case 3:
                    self.levels[self.score].pos[1] += 1
                case 4:
                    self.levels[self.score].pos[0] += 1
            if (
                self.levels[self.score].pos[1] < 0
                or self.levels[self.score].pos[1] > 3
                or self.levels[self.score].pos[0] < 0
                or self.levels[self.score].pos[0] > 2
            ):
                raise FailStateException("Invalid maze direction")
            nRead += 1
            self.receiveLen -= 1

            match self.levels[self.score].grid[self.levels[self.score].pos[0]][
                self.levels[self.score].pos[1]
            ]:
                case False:
                    raise FailStateException("Maze loss: killed")
                case None:
                    if self.receiveLen == 0:
                        raise FailStateException("Maze loss: out of moves")
                case True:
                    self.score += 1
                    if self.score == self.targetScore:
                        self.canReceive = False
                        self.canInput = False
                    else:
                        self.canReceive = True
                        self.inputLen = None
                        self.canInput = False
                    return sum(symbols[:nRead])
