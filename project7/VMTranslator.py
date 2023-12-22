import sys

C_ARITHMETIC = 1
C_PUSH = 2
C_POP = 3
C_LABEL = 4
C_GOTO = 5
C_IF = 6
C_FUNCTION = 7
C_RETURN = 8
C_CALL = 9
ARITHMRTIC_CMDS = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]


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
        self.curr_cmd = self.cmds[self.curr_line]

    def commandType(self):
        op = self.curr_cmd.split(" ")[0]

        if op in ARITHMRTIC_CMDS:
            return C_ARITHMETIC

        elif op == "push":
            return C_PUSH
        
        elif op == "pop":
            return C_POP

    def arg1(self):
        cmds = self.curr_cmd.split()

        if self.commandType() == C_ARITHMETIC:
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
            "add": "M=D+M",
            "sub": "M=D-M",
            "and": "M=D&M",
            "or": "M=D|M",
            "neg": "M=-M",
            "not": "M=!M",
            "eq": "D;JEQ",
            "gt": "D;JGT",
            "lt": "D;JLT",

            "local": "@LCL",
            "argument": "@ARG",
            "this": "@THIS",
            "that": "@THAT",
            "pointer": "@3",
            "temp": "@5"
        }

        self.label_cnt = 0
        self.filename = filename[:-4]

    @classmethod
    def setFileName(self, filename):
        strs = filename.split(".")
        strs[-1] = "asm"

        return ".".join(strs)

    def writeArithmetic(self, command):
        output = []

        if command in ["add", "sub", "and", "or"]:
            output.append("@SP")
            output.append("AM=M-1")
            output.append("D=M")
            output.append("@SP")
            output.append("A=M-1")
            output.append(self.symbols[command])
            output.append("@SP")
            output.append("M=M+1")

        elif command in ["neg", "not"]:
            output.append("@SP")
            output.append("A=M-1")
            output.append(self.symbols[command])
        
        elif command in ["eq", "gt", "lt"]:
            label = "jump" + str(self.label_cnt)
            self.label_cnt += 1

            output.append("@SP")
            output.append("AM=M-1")
            output.append("D=M")

            output.append("@SP")
            output.append("A=M-1")
            output.append("D=M-D")
            output.append("M=-1")
            output.append("@" + label)
            output.append(self.symbols[command])

            output.append("@SP")
            output.append("A=M-1")
            output.append("M=0")
            output.append(f"({label})")

        output.append("")
            
        for line in output:
            print(line, file=self.file)

    def writePushPop(self, command, segment, index):
        output = []
        # segment : argument, local, static, constant, this, that, pointer, temp

        if command == C_PUSH:
            if segment == "constant":
                output.append("@" + str(index))
                output.append("D=A")
                output.append("@SP")
                output.append("A=M")
                output.append("M=D")
                output.append("@SP")
                output.append("M=M+1")

            elif segment == "argument":
                output.append("@" + str(index))
                output.append("D=A")
                output.append(self.symbols["argument"])
                output.append("A=M+D")
                output.append()

            


        elif command == C_POP:
            pass


        output.append("")

        for line in output:
            print(line, file=self.file)


    def close(self):
        self.file.close()


def main():
    input_file = sys.argv[1]
    output_file = CodeWriter.setFileName(input_file)

    parser = Parser(input_file)
    code_writer = CodeWriter(output_file)

    while parser.hasMoreCommands():
        parser.advance()

        cmd = parser.get_cmd()
        arg1 = parser.arg1()
        cmd_type = parser.commandType()

        if cmd_type == C_ARITHMETIC:
            code_writer.writeArithmetic(arg1)

        elif cmd_type in [C_POP, C_PUSH]:
            arg2 = parser.arg2()
            code_writer.writePushPop(cmd_type, arg1, arg2)

    code_writer.close()

if __name__ == "__main__":
    main()