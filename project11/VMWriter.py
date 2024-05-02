from Constants import Segment, Command

class VMWriter:
    def __init__(self, output) -> None:
        self.output = open(self.output, 'w')

    def writePush(self, segment, index):
        self._writeLine("push " + segment + " " + str(index))

    def writePop(self, segment, index):
        self._writeLine("pop " + segment + " " + str(index))


    def writeArithmetic(self, command):
        pass

    def writeLabel(self, label):
        pass

    def writeGoto(self, label):
        pass

    def writeIf(self, label):
        pass

    def writeCall(self, name, nArgs):
        pass

    def writeFunction(self, name, nLocals):
        pass

    def writeReturn(self):
        pass

    def close(self):
        self.output.close()

    def _writeLine(self, line):
        self.output.write(line)