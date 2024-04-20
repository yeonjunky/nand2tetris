import sys

from JackTokenizer import JackTokenizer

class CompilationEngine:
    OP = ["+", "-", "*", "/", "<", ">", "&", "|", "="]

    def __init__(self, input_file, output_file):
        self.tokenizer = JackTokenizer(input_file)
        self.output_file = open(output_file, 'w')

        self.tokenType = None
        self.closing_stack = []
        self.indentLevel = 0
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
        self.indentLevel += 1

        self._advance()

        # keyword 'class'
        self._writeKeyword()
        self._advance()

        # identifier "className"
        self._writeIdentifier()
        self._advance()

        while self.tokenizer.hasMoreTokens():
            tokenType = self.tokenizer.tokenType()

            if tokenType == "keyword":
                token = self.getToken()
                self.method_dict[token]()

            elif tokenType == "symbol":
                self._writeSymbol()
                self._advance()

            elif tokenType == "identifier":
                self._writeIdentifier()
                self._advance()

        self._writeSymbol()

        self.indentLevel -= 1
        self.write("</class>")


    def compileClassVarDec(self) -> None:
        self.write("<classVarDec>\n")
        self.indentLevel += 1

        self._writeKeyword()
        self._advance()

        self._writeKeyword()
        self._advance()

        self._writeIdentifier()
        self._advance()

        self._writeSymbol()
        self._advance()

        self.indentLevel -= 1
        self.write("</classVarDec>\n")


    def compileSubroutine(self) -> None:
        self.write("<subroutineDec>\n")
        self.indentLevel += 1

        # function, method, constructor
        self._writeKeyword()
        self._advance()

        # type
        self._writeKeyword()
        self._advance()

        # funcName
        self._writeIdentifier()
        self._advance()

        self._writeSymbol()
        self._advance()

        self.compileParameterList()

        self._writeSymbol()
        self._advance()

        self.write("<subroutineBody>\n")
        self.indentLevel += 1

        self._writeSymbol()
        self._advance()

        while self.tokenType != "symbol":
            keyword = self.tokenizer.keyword()

            if keyword in self.statements:
                self.compileStatements()
            else:
                self.method_dict[keyword]()

        self._writeSymbol()
        self._advance()

        self.indentLevel -= 1
        self.write("</subroutineBody>\n")

        self.indentLevel -= 1
        self.write("</subroutineDec>\n")


    def compileParameterList(self) -> None:
        #TODO: while 문 고치기
        self.write("<parameterList>\n")
        self.indentLevel += 1

        while self.tokenType != "symbol":
            
            self.write("<" + self.tokenType + "> "
                       + self.getToken())
            self.write(" </" + self.tokenType + ">\n")

            self._advance()

        self.indentLevel -= 1
        self.write("</parameterList>\n")


    def compileVarDec(self) -> None:
        self.write("<varDec>\n")
        self.indentLevel += 1
        symbol = ""

        self._writeKeyword()
        self._advance()

        if self.tokenType == "identifier":
            self._writeIdentifier()

        elif self.tokenType == "keyword":
            self._writeKeyword()

        self._advance()

        while symbol != ";":
            self._writeIdentifier()
            self._advance()

            symbol = self.tokenizer.symbol()

            if symbol == ",":
                self._writeSymbol()
                self._advance()

        self._writeSymbol()
        self._advance()

        self.indentLevel -= 1
        self.write("</varDec>\n")


    def compileStatements(self) -> None:
        token = self.getToken()

        self.write("<statements>\n")
        self.indentLevel += 1

        while token in self.statements:
            self.method_dict[token]()

            token = self.getToken()

        self.indentLevel -= 1
        self.write("</statements>\n")


    def compileDo(self) -> None:
        self.write("<doStatement>\n")
        self.indentLevel += 1

        self._writeKeyword()
        self._advance()

        self._writeIdentifier()
        self._advance()

        self._writeSymbol()
        self._advance()

        self._writeIdentifier()
        self._advance()

        self._writeSymbol()
        self.compileExpressionList()

        self._writeSymbol()
        self._advance()

        self._writeSymbol()
        self._advance()

        self.indentLevel -= 1
        self.write("</doStatement>\n")


    def compileLet(self) -> None:
        token = self.getToken()

        self.write("<letStatement>\n")
        self.indentLevel += 1

        self._writeKeyword()
        self._advance()

        self._writeIdentifier()
        self._advance()

        if self.tokenType == "symbol" and self.tokenizer.symbol() == "[":
            self._writeSymbol()
            self._advance()

            self.compileExpression()

            self._writeSymbol()
            self._advance()

        self._writeSymbol()
        self._advance()

        self.compileExpression()

        # semicolon
        self._writeSymbol()
        self._advance()

        self.indentLevel -= 1
        self.write("</letStatement>\n")


    def compileWhile(self) -> None:
        self.write("<whileStatement>\n")
        self.indentLevel += 1

        self._writeKeyword()
        self._advance()

        self._writeSymbol()
        self._advance()

        self.compileExpression()

        self._writeSymbol()
        self._advance()

        self._writeSymbol()
        self._advance()

        self.compileStatements()

        self._writeSymbol()
        self._advance()
        self.indentLevel -= 1
        self.write("</whileStatement>\n")


    def compileReturn(self) -> None:
        self.write("<returnStatement>\n")
        self.indentLevel += 1

        self._writeKeyword()
        self._advance()

        self._writeSymbol()
        self._advance()

        self.indentLevel -= 1
        self.write("</returnStatement>\n")


    def compileIf(self) -> None:
        self.write("<ifStatement>\n")
        self.indentLevel += 1

        self._writeKeyword()
        self._advance()

        self._writeSymbol()
        self._advance()

        self.compileExpression()

        self._writeSymbol()
        self._advance()

        self._writeSymbol()
        self._advance()

        self.compileStatements()

        self._writeSymbol()
        self._advance()

        if self.tokenType == "keyword" and self.tokenizer.keyword() == "else":
            self._writeKeyword()
            self._advance()

            self._writeSymbol()
            self._advance()

            self.compileStatements()

            self._writeSymbol()
            self._advance()
        
        self.indentLevel -= 1
        self.write("</ifStatement>\n")


    def compileExpression(self) -> None:
        self.write("<expression>\n")
        self.indentLevel += 1

        self.compileTerm()

        while self.tokenizer.symbol() in self.OP:
            self._writeSymbol()
            self._advance()

            self.compileTerm()

        self.indentLevel -= 1
        self.write("</expression>\n")


    def compileTerm(self) -> None:
        self.write("<term>\n")
        self.indentLevel += 1

        if self.tokenType in ["int_const", "string_const"]:
            self._writeConstant()
            self._advance()

        if self.tokenType == "keyword":
            self._writeKeyword()
            self._advance()

        elif self.tokenType == "identifier":
            self._writeIdentifier()
            self._advance()

            if self.tokenType == "symbol":
                symbol = self.tokenizer.symbol()

                if symbol == "[":
                    self._writeSymbol()
                    self._advance()

                    self.compileExpression()

                    self._writeSymbol()
                    self._advance()
                
                elif symbol == "(":
                    self._writeSymbol()
                    self.compileExpressionList()

                    self._writeSymbol()
                    self._advance()

                elif symbol == ".":
                    self._writeSymbol()

                    self._advance()
                    self._writeIdentifier()

                    self._advance()
                    self._writeSymbol()

                    self.compileExpressionList()

                    self._writeSymbol()
                    self._advance()

        self.indentLevel -= 1
        self.write("</term>\n")


    def compileExpressionList(self) -> None:
        is_empty = False
        prevType = self.tokenType
        symbol = self.tokenizer.symbol()

        self.write("<expressionList>\n")
        self.indentLevel += 1

        self._advance()

        if self.tokenType == 'symbol' and self.tokenizer.symbol() == ")":
            is_empty = True

        if prevType == 'symbol' and symbol != "(":
            if not is_empty:
                self.compileExpression()

                while self.tokenType == 'symbol' and symbol == ",":
                    self._writeSymbol()
                    self._advance()
                    self.compileExpression()

        if prevType == 'symbol' and symbol == "(":
            if not is_empty:
                self.compileExpression()

        self.indentLevel -= 1
        self.write("</expressionList>\n")



    def write(self, line, indent=True):
        if indent:
            line = str("  " * self.indentLevel) + line

        self.output_file.write(
            str(line)
        )

        print(line, end="")


    def _writeSymbol(self):
        symbol = self.tokenizer.symbol()

        if symbol == "<":
            symbol = "&lt;"
        elif symbol == ">":
            symbol = "&gt;"

        self.write("<" + self.tokenizer.tokenType() + "> "
                   + symbol)
        self.write(" </" + self.tokenizer.tokenType() + ">\n", indent=False)


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

    
    def _writeKeyword(self):
        self.write("<keyword> ")
        self.write(self.tokenizer.keyword(), indent=False)
        self.write(" </keyword>\n", indent=False)

    def _writeIdentifier(self):
        self.write("<identifier> ")
        self.write(self.tokenizer.identifier(), indent=False)
        self.write(" </identifier>\n", indent=False)

    def _writeConstant(self):
        if self.tokenType == "string_const":
            type = "stringConstant"
            token = self.tokenizer.stringVal()

        elif self.tokenType == "int_const":
            type = "integerConstant"
            token = self.tokenizer.intVal()

        self.write("<" + type + "> ")
        self.write(token, indent=False)
        self.write(" </" + type + ">\n", indent=False)
        



c = CompilationEngine(sys.argv[1], sys.argv[2])