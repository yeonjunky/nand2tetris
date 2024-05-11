import sys
import os
import re

from CompilationEngine import CompilationEngine


class JackCompiler:
    jackFileRe = re.compile(r"[A-Za-z0-9]+.jack")
    JACKSUFFIX = ".jack$"
    VMSUFFIX = ".vm"

    def __init__(self, target) -> None:
        self.target = target


    def compile(self):
        if os.path.isdir(self.target):
            self.compileFolder()

        elif os.path.isfile(self.target) and \
            self.jackFileRe.match(os.path.basename(self.target)):
            self.compileFile()


    def compileFolder(self):
        jackFiles = []

        for i in os.listdir(self.target):
            if self.jackFileRe.match(i):
                if self.target[-1] != "/":
                    self.target += "/"

                jackFiles.append(self.target + i)

        for f in jackFiles:
            output = self.outputPath(f)
            CompilationEngine(f, output)


    def compileFile(self):
        output = self.outputPath(self.target)
        CompilationEngine(self.target, output)


    def outputPath(self, file:str):
        return re.sub(self.JACKSUFFIX, self.VMSUFFIX, file)
    

if __name__ == "__main__":
    print("compiling " + sys.argv[1])
    jackCompiler = JackCompiler(sys.argv[1])
    jackCompiler.compile()
    print("compile finished!")

