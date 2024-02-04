import sys

A_COMMAND = 0
C_COMMAND = 1
L_COMMAND = 2

class Parser:
    def __init__(self, asm):
        self.symbol = asm
        self.code = Code()

        self.curr_line = None
        self.len = len(asm)

        self.binary = []

    def hasMoreCommands(self):
        return self.curr_line < self.len

    def advance(self):
        if self.curr_line == None:
            self.curr_line = 0
        self.curr_line += 1

    def commandType(self, symbol):
        if symbol[0] == "@":
            return A_COMMAND
        elif symbol[0] == '(' and symbol[-1] == ')':
            return L_COMMAND
        return C_COMMAND

    def symbol(self):
        curr_symbol = self.get_symbol()
        if curr_symbol[0] == '@':
            return curr_symbol[1:]        
        return curr_symbol[1:len(curr_symbol) - 1]

    def dest(self, curr_symbol):
        idx = curr_symbol.find('=')
        if idx == -1:
            return None
        return curr_symbol[:idx]

    def comp(self, curr_symbol):
        start = curr_symbol.find('=') + 1
        end = curr_symbol.find(';')

        if start == -1:
            start = 0

        if end == -1:
            end = len(curr_symbol)
        return curr_symbol[start:end]

    def jump(self, curr_symbol):
        idx = curr_symbol.find(';') + 1
        if idx == -1:
            return None
        return curr_symbol[idx:]

    def cinst_to_binary(self, cisnt):
        pass

    def get_symbol(self):
        return self.symbol[self.curr_line]

    def parse(self):
        self.advance()

        while self.hasMoreCommands():
            curr_symbol = self.get_symbol().rstrip()

            for i, c in enumerate(curr_symbol):
                if c == curr_symbol[i-1] == '/':
                    curr_symbol = curr_symbol[:i-1]
                    break

            if curr_symbol != '':
                comm_type = self.commandType(curr_symbol)
                if comm_type == A_COMMAND:
                    binary = curr_symbol

                elif comm_type == C_COMMAND:
                    binary = curr_symbol

                elif comm_type == L_COMMAND:
                    binary = curr_symbol

                binary = self.code.comp(self.comp())
                print(curr_symbol)

            self.advance()
        


class Code:
    def __init__(self):
        self.mnemonic = {
            "JGT": "001",
            "JEQ": "010",
            "JGE": "011",
            "JLT": "100",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111",

            "M": "001",
            "D": "010",
            "MD": "011",
            "A": "100",
            "AM": "101",
            "AD": "110",
            "AMD": "111",

            "0": "0101010",
            "1": "0111111",
            "-1": "0111010",
            "D": "0001100",
            "A": "0110000",
            "!D": "0001101",
            "!A": "0110001",
            "-D": "0001111",
            "-A": "0110011",
            "D+1": "0011111",
            "A+1": "0110111",
            "D-1": "0001110",
            "A-1": "0110010",
            "D+A": "0000010",
            "D-A": "0010011",
            "A-D": "0000111",
            "D&A": "0000000",
            "D|A": "0010101",

            "M": "1110000",
            "!M": "1110001",
            "-M": "1110011",
            "M+1": "1110111",
            "M-1": "1110010",
            "D+M": "1000010",
            "D-M": "1010011",
            "M-D": "1000111",
            "D&M": "1000000",
            "D|M": "1010101"
        }

    def comp(self, mnemonic=None):
        return self.mnemonic[mnemonic]

    def jump(self, mnemonic=None):
        if mnemonic is None:
            return "000"
        return self.mnemonic[mnemonic]

    def dest(self, mnemonic=None):
        if mnemonic is None:
            return "000"
        return self.mnemonic[mnemonic]


class SymbolTable:
    def __init__(self):
        self.table = {
            'SP': 0,
            'LCL': 1,
            'ARG': 2,
            'THIS': 3,
            'THAT': 4,
            'SCREEN': 16384,
            'KBD': 24576
            }

        for i in range(0, 16):
            self.table[f'R{i}'] = i

    def addEntry(self, symbol, address):
        if not self.contains(symbol):
            self.table[symbol] = address

    def contains(self, symbol):
        return symbol in self.table

    def getAddress(self, symbol):
        return self.table[symbol]


if __name__ == "__main__":
    filename = sys.argv[1]
    result_name = filename.rstrip(".asm") + ".hack"
    with open(filename, 'r') as f:
        asm = f.readlines()
        parser = Parser(asm)
        parser.parse()

    print(result_name)
