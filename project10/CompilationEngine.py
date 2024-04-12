from JackTokenizer import JackTokenizer
from Constants import Tokentype

class CompilationEngine:
    def __init__(self, input_file, output_file):
        self.tokenizer = JackTokenizer(input_file)
        self.output_file = open(output_file, 'w')

        self.tokenType = None
        self.closing_stack = []
        self.method_dict = {
            'method': self.compileSubroutine,
            'function': self.compileSubroutine,
            'constructor': self.compileSubroutine,

            'static': self.compileClassVarDec,
            'field': self.compileClassVarDec,

            'var': self.compileVarDec,
            'let': self.compileLet,

            'if': self.compileIf,
            'while': self.compileWhile,

            'do': self.compileDo,
            'return': self.compileReturn,
        }

        self.statements = ["let", "while", "do", "return", "if"]

        self.compileClass()

        self.output_file.close()
        

    def compileClass(self) -> None:
        self.write("<class>\n")

        # keyword 'class'
        self._advance()
        self.write("<" + self.tokenType + "> " 
                   + self.getToken())
        self.write(" </" + self.tokenType + ">\n")

        self._advance()

        # identifier "className"
        self.write("<" + self.tokenType + "> "
                   + self.getToken())
        self.write(" </" + self.tokenType + ">\n")

        while self.tokenizer.hasMoreTokens():
            self._advance()
            tokenType = self.tokenizer.tokenType()

            if tokenType == "keyword":
                keyword = self.getToken()
                self.method_dict[keyword]()

            elif tokenType == "symbol":
                self.handleSymbol()

        self.write("</class>")


    def compileClassVarDec(self) -> None:
        pass


    def compileSubroutine(self) -> None:
        self.write("<SubroutineDec>\n")

        # function, method, constructor
        self.write("<" + self.tokenType + "> "
                   + self.getToken())
        self.write(" </" + self.tokenType + ">\n")

        self._advance()

        # type
        self.write("<" + self.tokenType + "> "
                   + self.getToken())
        self.write(" </" + self.tokenType + ">\n")

        self._advance()

        # funcName
        self.write("<" + self.tokenType + "> "
                   + self.getToken())
        self.write(" </" + self.tokenType + ">\n")

        self._advance()

        self.handleSymbol()

        self._advance()
        self.compileParameterList()

        self.write("<subroutineBody>\n")

        self._advance()
        self.handleSymbol()

        self._advance()

        while self.tokenType != "symbol":
            keyword = self.tokenizer.keyword()

            if keyword in self.statements:
                self.compileStatements()
            else:
                self.method_dict[keyword]()

            self._advance()

        self.handleSymbol()

        self.write("</subroutineBody>\n")



    def compileParameterList(self) -> None:
        self.write("<parameterList>\n")

        while self.tokenType != "symbol":
            
            self.write("<" + self.tokenType + "> "
                       + self.getToken())
            self.write(" </" + self.tokenType + ">\n")

            self._advance()

        self.write("</parameterList>\n")

        self.handleSymbol()


    def compileVarDec(self) -> None:
        self.write("<varDec>\n")
        keyword = self.getToken()

        while keyword != ";":
            if self.tokenType == "symbol":
                self.handleSymbol()

            else:
                self.write("<" + self.tokenType + ">")
                self.write(" " + keyword + " ")
                self.write("</" + self.tokenType + ">\n")

            self._advance()
            keyword = self.getToken()

        self.handleSymbol()

        self.write("</varDec>\n")


    def compileStatements(self) -> None:
        keyword = self.getToken()

        self.write("<statements>\n")

        while keyword in self.statements:
            self.method_dict[keyword]()

        self.write("</statements>\n")


    def compileDo(self) -> None:
        pass


    def compileLet(self) -> None:
        pass


    def compileWhile(self) -> None:
        pass


    def compileReturn(self) -> None:
        pass


    def compileIf(self) -> None:
        pass


    def compileExpression(self) -> None:
        pass


    def compileTerm(self) -> None:
        pass


    def complileExpressionList(self) -> None:
        pass


    def write(self, line):
        # self.output_file.write(
        #     line
        # )
        print(line, end="")


    def handleSymbol(self):
        self.write("<" + self.tokenizer.tokenType() + "> "
                   + self.tokenizer.symbol())
        self.write(" </" + self.tokenizer.tokenType() + ">\n")


    def getToken(self):
        if self.tokenType == "keyword":
            return self.tokenizer.keyword()
        
        if self.tokenType == "symbol":
            return self.tokenizer.symbol()
        
        if self.tokenType == "identifier":
            return self.tokenizer.identifier()
        
        if self.tokenType == "int_const":
            return self.tokenizer.intVal()
        
        if self.tokenType == "string_const":
            return self.tokenizer.stringVal()


    def _updateTokenType(self):
        self.tokenType = self.tokenizer.tokenType()


    def _advance(self):
        self.tokenizer.advance()
        self._updateTokenType()

c = CompilationEngine("./ArrayTest/Main.jack", "./ArrayTest/Main.xml")