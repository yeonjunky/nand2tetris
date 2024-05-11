import sys

from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter
from Constants import Kind, Segment, Command, Tokentype

class CompilationEngine:
    OP = ["+", "-", "*", "/", "<", ">", "&", "|", "="]

    def __init__(self, input_file, output_file):
        self.tokenizer = JackTokenizer(input_file)
        self.symbolTable = SymbolTable()
        self.vmWriter = VMWriter(output_file)

        # TODO: delete open and close func
        self.output_file = open(output_file, 'w')
        self.outFileName = ""

        self.tokenType = None
        self.indentLevel = 0
        self.isExpList = False
        self.labelCnt = 0

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
        self.vmWriter.close()


    def compileClass(self) -> None:
        self.write("<class>\n")
        self.indentLevel += 1
        self._advance()

        # keyword 'class'
        self._writeKeyword()
        self._advance()

        # identifier "className"
        self._writeIdentifier()
        className = self.tokenizer.identifier()
        self._setClassName(className)
        self._advance()

        while self.tokenizer.hasMoreTokens():
            tokenType = self.tokenizer.tokenType()

            if tokenType == "keyword":
                token = self.tokenizer.keyword()
                self.method_dict[token]()

            elif tokenType == "symbol":
                self._writeSymbol()
                self._advance()

            elif tokenType == "identifier":
                self._writeIdentifier()
                self._advance()

        # closing curly brace
        self._writeSymbol()

        self.indentLevel -= 1
        self.write("</class>\n")


    def compileClassVarDec(self) -> None:
        symbol = ""

        self.write("<classVarDec>\n")
        self.indentLevel += 1

        # kind
        self._writeKeyword()
        self._advance()
        kind = self.tokenizer.keyword()

        if self.tokenType == "identifier": # classType
            type = self.tokenizer.identifier()
            self._writeIdentifier()

        elif self.tokenType == "keyword": # prmitive type
            type = self.tokenizer.keyword()
            self._writeKeyword()

        self._advance()

        while symbol != ";":
            name = self.tokenizer.identifier()
            self.symbolTable.define(name, type, kind)
            self._writeIdentifier()
            self._advance()

            symbol = self.tokenizer.symbol()

            self._writeSymbol()
            self._advance()

        self.indentLevel -= 1
        self.write("</classVarDec>\n")


    def compileSubroutine(self) -> None:
        self.write("<subroutineDec>\n")
        self.indentLevel += 1
        varDecCnt = 0
        isVoid = False

        self.symbolTable.startSubroutine()

        # function, method, constructor
        funcType = self.tokenizer.keyword()
        self._writeKeyword()
        self._advance()

        # type
        if self.tokenType == "keyword":
            returnType = self.tokenizer.keyword()

            if returnType == "void":
                isVoid = True
            self._writeKeyword()

        elif self.tokenType == "identifier":
            self._writeIdentifier()

        self._advance()

        # funcName
        funcName = self.tokenizer.identifier()
        self._writeIdentifier()
        self._advance()

        self._writeSymbol()
        self._advance()

        self.compileParameterList()

        self._writeSymbol()
        self._advance()

        self.write("<subroutineBody>\n")
        self.indentLevel += 1

        # {
        self._writeSymbol()
        self._advance()

        while self.tokenType == "keyword" and self.tokenizer.keyword() == "var":
            self.compileVarDec()

        funcName = self.className + "." + funcName
        nLocals = self.symbolTable.varCount(Kind.VAR)
        self.vmWriter.writeFunction(funcName, nLocals)

        while self.tokenType != "symbol":
            keyword = self.tokenizer.keyword()

            if keyword in self.statements:
                self.compileStatements()
            else:
                self.method_dict[keyword]()

        # }
        self._writeSymbol()
        self._advance()

        self.indentLevel -= 1
        self.write("</subroutineBody>\n")

        self.indentLevel -= 1
        self.write("</subroutineDec>\n")


    def compileParameterList(self) -> None:
        self.write("<parameterList>\n")
        self.indentLevel += 1

        symbol = ""
        isCloseParen = False
        kind = self._getKeyWordKind("arg")

        if self.tokenType == "symbol" and self.tokenizer.symbol() == ")":
            isCloseParen = True

        while not isCloseParen:
            type = self.tokenizer.keyword()
            self._writeKeyword()
            self._advance()

            name = self.tokenizer.identifier()
            self._writeIdentifier()
            self._advance()

            # self.symbolTable.define(name, type, kind)

            symbol = self.tokenizer.symbol()
            isCloseParen = True if symbol == ")" else False

            if isCloseParen:
                break

            self._writeSymbol()
            self._advance()


        self.indentLevel -= 1
        self.write("</parameterList>\n")


    def compileVarDec(self) -> None:
        self.write("<varDec>\n")
        self.indentLevel += 1
        symbol = ""

        # var
        kind = self._getKeyWordKind(self.tokenizer.keyword())
        self._writeKeyword()
        self._advance()

        if self.tokenType == "identifier": # class type
            type = self.tokenizer.identifier()
            self._writeIdentifier()

        elif self.tokenType == "keyword": # primitive type
            type = self.tokenizer.keyword()
            self._writeKeyword()

        self._advance()

        while symbol != ";":
            name = self.tokenizer.identifier()
            self.symbolTable.define(name, type, kind)
            self._writeIdentifier()
            self._advance()

            symbol = self.tokenizer.symbol()

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
        name = self.tokenizer.identifier()
        self._advance()

        symbol = self.tokenizer.symbol()

        if symbol == ".":
            self._writeSymbol()
            name += self.tokenizer.symbol()
            self._advance()

            self._writeIdentifier()
            name += self.tokenizer.identifier()
            self._advance()

        self._writeSymbol()
        nArgs = self.compileExpressionList()

        self._writeSymbol()
        self._advance()

        self._writeSymbol()
        self._advance()

        self.vmWriter.writeCall(name, nArgs)

        self.indentLevel -= 1
        self.write("</doStatement>\n")


    def compileLet(self) -> None:
        self.write("<letStatement>\n")
        self.indentLevel += 1

        # let keyword
        self._writeKeyword()
        self._advance()

        # variable name
        self._writeIdentifier()
        
        varName = self.tokenizer.identifier()
        varIdx = self.symbolTable.indexOf(varName)

        varKind = self.symbolTable.kindOf(varName)
        varSegment = self._kindToSegment(varKind)

        self._advance()

        if self.tokenType == "symbol" and self.tokenizer.symbol() == "[":
            self.vmWriter.writePush(varSegment, varIdx)

            self._writeSymbol()
            self._advance()

            self.compileExpression()

            self._writeSymbol()
            self._advance()

            self.vmWriter.writeArithmetic(Command.ADD)
            self.vmWriter.writePop("pointer", 1)

            varSegment = "that"
            varIdx = 0

        # write "="
        self._writeSymbol()
        self._advance()

        # right expression
        self.compileExpression()

        self.vmWriter.writePop(varSegment, varIdx)

        # semicolon
        self._writeSymbol()
        self._advance()

        self.indentLevel -= 1
        self.write("</letStatement>\n")


    def compileWhile(self) -> None:
        self.write("<whileStatement>\n")
        self.indentLevel += 1

        loopLabel = "LABEL_" + str(self.labelCnt)
        self.labelCnt += 1
        escapeLabel = "LABEL_" + str(self.labelCnt)

        self.vmWriter.writeLabel(loopLabel)


        self._writeKeyword()
        self._advance()

        self._writeSymbol()
        self._advance()

        self.compileExpression()
        self.vmWriter.writeArithmetic(Command.NOT)

        self.vmWriter.writeIf(escapeLabel)

        self._writeSymbol()
        self._advance()

        self._writeSymbol()
        self._advance()

        self.compileStatements()

        self.vmWriter.writeGoto(loopLabel)

        self._writeSymbol()

        self.vmWriter.writeLabel(escapeLabel)
        self._advance()
        self.indentLevel -= 1
        self.write("</whileStatement>\n")


    def compileReturn(self) -> None:
        self.write("<returnStatement>\n")
        self.indentLevel += 1

        self._writeKeyword()
        self._advance()

        if self.tokenType != "symbol":
            self.compileExpression()

        self._writeSymbol()
        self._advance()

        self.vmWriter.writeReturn()

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
            symbol = self.tokenizer.symbol()
            op = self._symToCommand(symbol)

            self._advance()

            self.compileTerm()

            self.vmWriter.writeArithmetic(op)


        self.indentLevel -= 1
        self.write("</expression>\n")


    def compileTerm(self) -> None:
        self.write("<term>\n")
        self.indentLevel += 1

        if self.tokenType in ["int_const", "string_const"]:
            self._writeConstant()
            self._advance()

        elif self.tokenType == "keyword":
            self._writeKeyword()
            self._advance()

        elif self.tokenType == "identifier": 
            # identifier | identifier '[' expression ']' 
            # identifier(expList) | identifier.functionName(expList)
            name = self.tokenizer.identifier()

            self._writeIdentifier()
            self._advance()

            if self.tokenType == "symbol":
                symbol = self.tokenizer.symbol() 

                if symbol == "[": # array
                    self._writeSymbol()
                    self._advance()

                    varKind = self.symbolTable.kindOf(name)
                    varSegment = self._kindToSegment(varKind)
                    varIdx = self.symbolTable.indexOf(name)

                    self.vmWriter.writePush(varSegment, varIdx)

                    self.compileExpression()

                    self.vmWriter.writeArithmetic(Command.ADD)

                    self.vmWriter.writePop("pointer", 1)
                    self.vmWriter.writePush("that", 0)

                    self._writeSymbol()
                    self._advance()
                
                elif symbol == "(": # method call
                    self._writeSymbol()
                    self.compileExpressionList()

                    self._writeSymbol()
                    self._advance()

                elif symbol == ".": # className.subroutineName(expList)
                    name += self.tokenizer.symbol()
                    self._writeSymbol()

                    self._advance()
                    self._writeIdentifier()
                    name += self.tokenizer.identifier()

                    # (
                    self._advance()
                    self._writeSymbol()

                    nArgs = self.compileExpressionList()
                    self.vmWriter.writeCall(name, nArgs)

                    # )
                    self._writeSymbol()
                    self._advance()

                else:
                    varKind = self.symbolTable.kindOf(name)
                    varSegment = self._kindToSegment(varKind)
                    varIdx = self.symbolTable.indexOf(name)

                    self.vmWriter.writePush(varSegment, varIdx)



        elif self.tokenType == "symbol": # '(' expression ')' | unary op
            symbol = self.tokenizer.symbol()

            if symbol == "(":
                self._writeSymbol()
                self._advance()

                self.compileExpression()

                self._writeSymbol()
                self._advance()

            elif symbol in ["~", "-"]:
                self._writeSymbol()
                self._advance()

                self.compileTerm()

        self.indentLevel -= 1
        self.write("</term>\n")


    def compileExpressionList(self) -> int:
        is_empty = False
        prevType = self.tokenType
        symbol = self.tokenizer.symbol()
        nArgs = 0
        self.isExpList = True

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
                nArgs += 1

                if self.tokenType == "symbol":
                    symbol = self.tokenizer.symbol()

                while self.tokenType == 'symbol' and symbol == ",":
                    self._writeSymbol()
                    self._advance()
                    nArgs += 1
                    self.compileExpression()

                    if self.tokenType == "symbol":
                        symbol = self.tokenizer.symbol()

        self.indentLevel -= 1
        self.write("</expressionList>\n")
        self.isExpList = False

        return nArgs

    def write(self, line, indent=True):
        if indent:
            line = str("  " * self.indentLevel) + line

        self.output_file.write(
            str(line)
        )

        # print(line, end="")
        # pass


    def _writeSymbol(self):
        symbol = self.tokenizer.symbol()

        if symbol == "<":
            symbol = "&lt;"
        elif symbol == ">":
            symbol = "&gt;"
        elif symbol == "&":
            symbol = "&amp;"

        self.write("<" + self.tokenizer.tokenType() + "> "
                   + symbol)
        self.write(" </" + self.tokenizer.tokenType() + ">\n", indent=False)

    # TODO: getToken 없애기
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
            self.vmWriter.writePush("constant", len(token))
            self.vmWriter.writeCall("String.new", 1)
            
            for c in token:
                self.vmWriter.writePush("constant", ord(c))
                self.vmWriter.writeCall("String.appendChar", 2)
            
        elif self.tokenType == "int_const":
            type = "integerConstant"
            token = self.tokenizer.intVal()
            
            self.vmWriter.writePush("constant", token)

        self.write("<" + type + "> ")
        self.write(token, indent=False)
        self.write(" </" + type + ">\n", indent=False)

    def _getKeyWordKind(self, kind):
        if kind == "static":
            return Kind.STATIC
        
        elif kind == "field":
            return Kind.FIELD
        
        elif kind == "arg":
            return Kind.ARG
        
        elif kind == "var":
            return Kind.VAR
        
    def _setClassName(self, className):
        self.className = className

    def _kindToSegment(self, kind:Kind) -> str: 
        kind = kind.name.lower()

        if kind == "static":
            return "static"

        elif kind == "field":
            return "this"

        elif kind == "arg":
            return "argument"

        elif kind == "var":
            return "local"
        
    def _symToCommand(self, symbol:str) -> Command:
        if symbol == "+":
            return Command.ADD

        elif symbol == "-":
            return Command.SUB

        elif symbol == "~":
            return Command.NEG

        elif symbol == "=":
            return Command.EQ
        
        elif symbol == ">":
            return Command.GT
        
        elif symbol == "<":
            return Command.LT
        
        elif symbol == "&":
            return Command.AND
        
        elif symbol == "|":
            return Command.OR
        
        elif symbol == "~":
            return Command.NOT
