from Constants import *
import re_patterns


class JackTokenizer:
    def __init__(self, input_file):
        self.lines = []

        slash = -1
        multi_comment = False
        skip_line = False

        with open(input_file, 'r') as f:
            for line in f.readlines():
                line = line.strip()

                remove_single = re_patterns.single_comment.search(line)

                if remove_single:
                    line = line[0:remove_single.start()]

                

                if line == "":
                    continue

                if not multi_comment and not skip_line:
                    self.lines.append(line)
                    print(line)
                skip_line = False


    def hasMoreTokens(self) -> bool:
        return True

    def advance(self) -> None:
        return

    def tokenType(self) -> int:
        return
    
    def keyword(self) -> int:
        return

    def symbol(self) -> str:
        return

    def identifier(self) -> str:
        return

    def intVal(self) -> int:
        return

    def stringVal(self) -> str:
        return


j = JackTokenizer("./ArrayTest/Main.jack")