from exceptions import FailStateException


class Pillar:
    canReceive = False
    canInput = False
    targetScore = 0
    score = 0
    inputLen = 0
    inputSym = []
    receiveLen = 0  # 0 means single int, not list of 0|1

    def receive(self, input):
        if self.receiveLen > 0:
            out = input if type(input) == list else [int(bit) for bit in bin(input)[2:]]
            if out.__len__() > self.receiveLen:
                raise FailStateException(
                    "Received bit string too long: expected "
                    + self.receiveLen
                    + " bits, mapped input to "
                    + str(out)
                )
            while out.__len__() < self.inputLen:
                out.insert(0, 0)
            return out
        else:
            return input if type(input) == int else int("".join(map(str, input)), 2)

    def input(self, input):
        print(input)
        return input
