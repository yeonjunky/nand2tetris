import CompilationEngine
import os
import re
import sys

class JackAnalyzer:
    jackFileRe = re.compile(r"[A-Za-z0-9]+.jack")
    JACKSUFFIX = ".jack$"
    XMLSUFFIX = ".xml"


    def __init__(self, target) -> None:
        self.target = target

        if os.path.isdir(target):
            self.compileFolder()

        elif os.path.isfile(target) and self.jackFileRe.match(os.path.basename(target)):
            self.compileFile()

        else:
            print("invalid file or folder path")


    def compileFile(self):
        outputFile = self.fileOutputPath(self.target)
        CompilationEngine.CompilationEngine(self.target, outputFile)


    def compileFolder(self):
        jackFiles = []

        for i in os.listdir(self.target):
            if self.jackFileRe.match(i):
                if self.target[-1] != "/":
                    self.target += "/"

                jackFiles.append(self.target + i)

        for f in jackFiles:
            outputFile = self.fileOutputPath(f)
            CompilationEngine.CompilationEngine(f, outputFile)


    def fileOutputPath(self, file):
        return re.sub(self.JACKSUFFIX, self.XMLSUFFIX, file)


if __name__ == "__main__":
    print("compiling " + sys.argv[1])
    JackAnalyzer(sys.argv[1])
    print("compile finished!")
