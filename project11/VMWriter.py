from Constants import Segment, Command

class VMWriter:
    def __init__(self, output:str) -> None:
        self.output = open(output, 'w')

    def writePush(self, segment:str, index:int):
        self._writeLine("push " + segment + " " + str(index))

    def writePop(self, segment:str, index:int):
        self._writeLine("pop " + segment + " " + str(index))

    def writeArithmetic(self, command:Command):
        if command == Command.ADD:
            self._writeLine("add")

        elif command == Command.SUB:
            self._writeLine("sub")

        elif command == Command.NEG:
            self._writeLine("neg")

        elif command == Command.EQ:
            self._writeLine("eq")

        elif command == Command.GT:
            self._writeLine("gt")

        elif command == Command.LT:
            self._writeLine("lt")

        elif command == Command.AND:
            self._writeLine("and")

        elif command == Command.OR:
            self._writeLine("or")

        elif command == Command.NOT:
            self._writeLine("not")

    def writeLabel(self, label:str):
        self._writeLine("label " + label)

    def writeGoto(self, label:str):
        self._writeLine("goto " + label)

    def writeIf(self, label:str):
        self._writeLine("if-goto" + " " + label)

    def writeCall(self, name:str, nArgs:int):
        self._writeLine("call" + " " + name + " " + str(nArgs))

    def writeFunction(self, name:str, nLocals:int):
        self._writeLine("function" + " " + name + " " + str(nLocals))

    def writeReturn(self):
        self._writeLine("return")

    def close(self):
        self.output.close()

    def _writeLine(self, line:str, isNewLine=True):
        newLine = "\n" if isNewLine else ""
        self.output.write(line + newLine)