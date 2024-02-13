import sys
import os

C_ARITHMETIC = 1
C_PUSH = 2
C_POP = 3
C_LABEL = 4
C_GOTO = 5
C_IF = 6
C_FUNCTION = 7
C_RETURN = 8
C_CALL = 9
CMDS = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]


class Parser:
    def __init__(self, filename):
        self.curr_cmd = ""
        self.curr_line = -1

        self.cmds = []

        with open(filename, 'r') as f:
            for c in f.readlines():
                if c[:2] == "//" or not c.strip():
                    continue
                self.cmds.append(c.rstrip())

    def hasMoreCommands(self):
        return self.curr_line + 1 < len(self.cmds)

    def advance(self):
        self.curr_line += 1
        self.curr_cmd = self.cmds[self.curr_line].lstrip()

    def commandType(self):
        op = self.curr_cmd.split(" ")[0]

        if op in CMDS:
            return C_ARITHMETIC

        elif op == "push":
            return C_PUSH
        
        elif op == "pop":
            return C_POP

        elif op == "label":
            return C_LABEL

        elif op == "goto":
            return C_GOTO

        elif op == "if-goto":
            return C_IF

        elif op == "function":
            return C_FUNCTION

        elif op == "return":
            return C_RETURN

        elif op == "call":
            return C_CALL

    def arg1(self):
        cmds = self.curr_cmd.split()
        if self.commandType() in [C_ARITHMETIC, C_RETURN]:
            return cmds[0]
        return cmds[1]

    def arg2(self):
        cmds = self.curr_cmd.split()
        return int(cmds[2])

    def get_cmd(self):
        return self.curr_cmd


class CodeWriter:
    def __init__(self, filename):
        self.file = open(filename, 'w')

        self.symbols = {
            "add": "M=M+D",
            "sub": "M=M-D",
            "and": "M=M&D",
            "or": "M=M|D",
            "neg": "M=-M",
            "not": "M=!M",
            "eq": "D;JEQ",
            "gt": "D;JGT",
            "lt": "D;JLT",

            "local": "@LCL",
            "argument": "@ARG",
            "this": "@THIS",
            "that": "@THAT",
            "pointer": 3,
            "temp": 5
        }

        self.label_cnt = 0
        self.call_cnt = 0

    def setFileName(self, vm_filename):
        vm_filename = vm_filename.replace(".vm", '').split('/')[-1]
        self.writeLine("/////////")
        self.writeLine("//" + vm_filename)

        self.currFile = vm_filename

    def writeInit(self):
        self.writeLine("// initialize")
        self.writeLine("@256")
        self.writeLine("D=A")
        self.writeLine("@SP")
        self.writeLine("M=D")

        self.writeCall("Sys.init", 0)

        self.writeLine("")

    def writeLabel(self, label):
        self.writeLine("(" + self.currFile + "." + label.upper() + ")")
        self.writeLine("")

    def writeGoto(self, label):
        self.writeLine("@" + self.currFile + "." + label.upper())
        self.writeLine("0;JMP")

        self.writeLine("")

    def writeIf(self, label):
        self.decSP()
        self.writeLine("A=M")
        self.writeLine("D=M")

        self.writeLine("@" + self.currFile + "." + label.upper())
        self.writeLine("D;JNE")

        self.writeLine("")

    def writeCall(self, funcName, numArgs):
        symbols = ["local", "argument", "this", "that"]
        retAddr = funcName + ".return" + str(self.call_cnt)
        self.call_cnt += 1

        self.writeLine("@" + retAddr)
        self.writeLine("D=A")

        self.writeLine("@SP")
        self.writeLine("A=M")
        self.writeLine("M=D")

        self.incSP()

        for s in symbols:
            self.writeLine(self.symbols[s])
            self.writeLine("D=M")

            self.writeLine("@SP")
            self.writeLine("A=M")
            self.writeLine("M=D")

            self.incSP()

        self.writeLine("@SP")
        self.writeLine("D=M")

        self.writeLine("@" + str(numArgs + 5))
        self.writeLine("D=D-A")

        self.writeLine(self.symbols["argument"])
        self.writeLine("M=D")

        self.writeLine("@SP")
        self.writeLine("D=M")
        self.writeLine(self.symbols["local"])
        self.writeLine("M=D")

        self.writeLine("@" + funcName)
        self.writeLine("0;JMP")

        self.writeLine("(" + retAddr + ")")
        self.writeLine("")


    def writeReturn(self):
        symbols = ["local", "argument", "this", "that"]

        self.writeLine(self.symbols["local"])
        self.writeLine("D=M")
        self.writeLine("@R13")
        self.writeLine("M=D")

        self.writeLine("@R13")
        self.writeLine("D=M")

        self.writeLine("@5")
        self.writeLine("D=D-A")
        self.writeLine("A=D")
        self.writeLine("D=M")

        self.writeLine("@R14")
        self.writeLine("M=D")

        self.decSP()
        self.writeLine("A=M")
        self.writeLine("D=M")
        self.writeLine(self.symbols["argument"])
        self.writeLine("A=M")
        self.writeLine("M=D")

        self.writeLine(self.symbols["argument"])
        self.writeLine("D=M")

        self.writeLine("@SP")
        self.writeLine("M=D+1")

        idx = 1

        for s in symbols[::-1]:
            self.writeLine("@R13")
            self.writeLine("D=M")
            self.writeLine("@" + str(idx))
            self.writeLine("D=D-A")
            self.writeLine("A=D")

            self.writeLine("D=M")

            self.writeLine(self.symbols[s])
            self.writeLine("M=D")

            idx += 1

        self.writeLine("@R14")
        self.writeLine("A=M")
        self.writeLine("0;JMP")

        self.writeLine("")

    def writeFunction(self, funcName, numLocals):
        self.writeLine("(" + funcName + ")")
        self.writeLine("D=0")

        for i in range(numLocals):
            self.writeLine("@SP")
            self.writeLine("A=M")
            self.writeLine("M=D")
            self.incSP()

        self.writeLine("")

    def writeArithmetic(self, command):
        if command in ["add", "sub", "and", "or"]:
            self.decSP()
            self.writeLine("A=M")
            self.writeLine("D=M")
            self.writeLine("@SP")
            self.writeLine("A=M-1")
            self.writeLine(self.symbols[command])

        elif command in ["neg", "not"]:
            self.writeLine("@SP")
            self.writeLine("A=M-1")
            self.writeLine(self.symbols[command])
        
        elif command in ["eq", "gt", "lt"]:
            label = "jump" + str(self.label_cnt)
            self.label_cnt += 1

            self.writeLine("@SP")
            self.writeLine("AM=M-1")
            self.writeLine("D=M")

            self.writeLine("@SP")
            self.writeLine("A=M-1")
            self.writeLine("D=M-D")
            self.writeLine("M=-1")
            self.writeLine("@" + label)
            self.writeLine(self.symbols[command])

            self.writeLine("@SP")
            self.writeLine("A=M-1")
            self.writeLine("M=0")
            self.writeLine(f"({label})")

        self.writeLine("")
            

    def writePushPop(self, command, segment, index):
        if command == C_PUSH:
            self.memoryLocation(segment, index)

            if segment == "constant":
                self.writeLine("D=A")

            elif segment in ["local", "argument", "this", "that", "pointer", "temp", "static"]:
                self.writeLine("D=M")
            
            self.writeLine("@SP")
            self.writeLine("A=M")
            self.writeLine("M=D")
            self.incSP()

        elif command == C_POP:
            self.memoryLocation(segment, index)

            self.writeLine("D=A")
            self.writeLine("@R13")
            self.writeLine("M=D")

            self.decSP()
            self.writeLine("A=M")
            self.writeLine("D=M")

            self.writeLine("@R13")
            self.writeLine("A=M")
            self.writeLine("M=D")

        self.writeLine("")

    def endLoop(self):
        self.writeLine("(END)")
        self.writeLine("@END")
        self.writeLine("0;JMP")

    def writeLine(self, line):
        self.file.write(line + "\n")

    def close(self):
        self.file.close()

    def memoryLocation(self, segment, index):
        if segment == "constant":
            self.writeLine("@" + str(index))

        elif segment in ["local", "argument", "this", "that"]:
            self.writeLine(self.symbols[segment])
            self.writeLine("D=M")
            self.writeLine("@" + str(index))
            self.writeLine("A=A+D")

        elif segment in ["pointer", "temp"]:
            self.writeLine("@R" + str(self.symbols[segment] + int(index)))
            
        elif segment == "static":
            self.writeLine("@" + self.currFile + "." + str(index))

    def incSP(self):
        self.writeLine("@SP")
        self.writeLine("M=M+1")

    def decSP(self):
        self.writeLine("@SP")
        self.writeLine("M=M-1")

class Main:
    def __init__(self, path):
        self.files = self.get_files(path)
        self.codeWriter = CodeWriter(self.asmFile)

        if len(self.files) > 1:
            self.codeWriter.writeInit()

        for vmFile in self.files:
            self.translate(vmFile)
        
        self.codeWriter.close()

    def get_files(self, path):
        is_dir = os.path.isdir(path)
        files = []

        if is_dir:
            for f in os.listdir(path):
                asmPath = path[:-1] if path[-1] == '/' else path
                pathElements = asmPath.split('/')
                pathElements.append(pathElements[-1])
                self.asmFile = '/'.join(pathElements) + ".asm"

                if f.endswith(".vm"):
                    files.append(asmPath + '/' + f)
                    
        else:
            files.append(path)
            self.asmFile = path.replace(".vm", ".asm")

        return files

    def translate(self, file):
        parser = Parser(file)

        self.codeWriter.setFileName(file)

        while parser.hasMoreCommands():
            parser.advance()
            
            cmd = parser.get_cmd()
            arg1 = parser.arg1()
            cmd_type = parser.commandType()

            self.codeWriter.writeLine("//" + parser.get_cmd())

            if cmd_type == C_ARITHMETIC:
                self.codeWriter.writeArithmetic(arg1)

            elif cmd_type in [C_POP, C_PUSH]:
                arg2 = parser.arg2()
                self.codeWriter.writePushPop(cmd_type, arg1, arg2)

            elif cmd_type == C_GOTO:
                self.codeWriter.writeGoto(arg1)

            elif cmd_type == C_LABEL:
                self.codeWriter.writeLabel(arg1)
                
            elif cmd_type == C_IF:
                self.codeWriter.writeIf(arg1)

            elif cmd_type == C_FUNCTION:
                arg2 = parser.arg2()
                self.codeWriter.writeFunction(arg1, arg2)

            elif cmd_type == C_RETURN:
                self.codeWriter.writeReturn()

            elif cmd_type == C_CALL:
                arg2 = parser.arg2()
                self.codeWriter.writeCall(arg1, arg2)


if __name__ == "__main__":
    Main(sys.argv[1])