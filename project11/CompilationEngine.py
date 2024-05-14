from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter
from Constants import Kind, Command

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
        self.isExpList = False
        self.labelCnt = 0
        self.isVoid = False
        self.voidSubroutines = []

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
        self._advance()

        # keyword 'class'
        self._advance()

        # identifier "className"
        className = self.tokenizer.identifier()
        self._setClassName(className)
        self._advance()

        while self.tokenizer.hasMoreTokens():
            tokenType = self.tokenizer.tokenType()

            if tokenType == "keyword":
                token = self.tokenizer.keyword()
                self.method_dict[token]()

            elif tokenType == "symbol":
                self._advance()

            elif tokenType == "identifier":
                self._advance()


    def compileClassVarDec(self) -> None:
        symbol = ""

        # kind
        keyword = self.tokenizer.keyword()
        kind = self._getKeyWordKind(keyword)
        self._advance()

        if self.tokenType == "identifier": # classType
            type = self.tokenizer.identifier()

        elif self.tokenType == "keyword": # prmitive type
            type = self.tokenizer.keyword()

        self._advance()

        while symbol != ";":
            name = self.tokenizer.identifier()
            self.symbolTable.define(name, type, kind)
            self._advance()

            symbol = self.tokenizer.symbol()

            self._advance()


    def compileSubroutine(self) -> None:

        self.symbolTable.startSubroutine()

        # function, method, constructor
        funcType = self.tokenizer.keyword()
        self._advance()

        # return type
        if self.tokenType == "keyword":
            returnType = self.tokenizer.keyword()

            if returnType == "void":
                self.isVoid = True

        self._advance()

        # funcName
        funcName = self.tokenizer.identifier()
        self._advance()

        self._advance()

        if funcType == "method":
            self.symbolTable.define("this", self.className, self._getKeyWordKind("arg"))
        self.compileParameterList()

        self._advance()

        # {
        self._advance()

        while self.tokenType == "keyword" and self.tokenizer.keyword() == "var":
            self.compileVarDec()

        funcName = self.className + "." + funcName
        nLocals = self.symbolTable.varCount(Kind.VAR)
        self.vmWriter.writeFunction(funcName, nLocals)

        if funcType == "constructor":
            fieldVarNum = self.symbolTable.varCount(Kind.FIELD)
            self.vmWriter.writePush("constant", fieldVarNum)
            self.vmWriter.writeCall("Memory.alloc", 1)
            self.vmWriter.writePop("pointer", 0)

        elif funcType == "method":
            self.vmWriter.writePush("argument", 0)
            self.vmWriter.writePop("pointer", 0)

        while self.tokenType != "symbol":
            keyword = self.tokenizer.keyword()

            if keyword in self.statements:
                self.compileStatements()
            else:
                self.method_dict[keyword]()

        self.isVoid = False

        # }
        self._advance()


    def compileParameterList(self) -> None:

        symbol = ""
        isCloseParen = False
        kind = self._getKeyWordKind("arg")

        if self.tokenType == "symbol" and self.tokenizer.symbol() == ")":
            isCloseParen = True

        while not isCloseParen:
            type = self.tokenizer.keyword()
            self._advance()

            name = self.tokenizer.identifier()
            self._advance()

            self.symbolTable.define(name, type, kind)

            symbol = self.tokenizer.symbol()
            isCloseParen = True if symbol == ")" else False

            if isCloseParen:
                break

            self._advance()


    def compileVarDec(self) -> None:
        symbol = ""

        # var
        kind = self._getKeyWordKind(self.tokenizer.keyword())
        self._advance()

        if self.tokenType == "identifier": # class type
            type = self.tokenizer.identifier()

        elif self.tokenType == "keyword": # primitive type
            type = self.tokenizer.keyword()

        self._advance()

        while symbol != ";":
            name = self.tokenizer.identifier()
            self.symbolTable.define(name, type, kind)
            self._advance()

            symbol = self.tokenizer.symbol()

            self._advance()


    def compileStatements(self) -> None:
        token = self.getToken()

        while token in self.statements:
            self.method_dict[token]()

            token = self.getToken()


    def compileDo(self) -> None:
        nArgs = 0

        self._advance()

        name = self.tokenizer.identifier()
        self._advance()

        symbol = self.tokenizer.symbol()

        if symbol == ".":
            varIdx = self.symbolTable.indexOf(name)

            if varIdx != None:
                varKind = self.symbolTable.kindOf(name)
                name = self.symbolTable.typeOf(name)
                varSegment = self._kindToSegment(varKind)
                nArgs = 1

                self.vmWriter.writePush(varSegment, varIdx)

            name += self.tokenizer.symbol()
            self._advance()

            name += self.tokenizer.identifier()
            self._advance()

        else:
            self.vmWriter.writePush("pointer", 0)
            name = self.className + "." + name
            nArgs = 1

        nArgs += self.compileExpressionList()

        self._advance()

        self._advance()

        self.vmWriter.writeCall(name, nArgs)
        self.vmWriter.writePop("temp", 0)


    def compileLet(self) -> None:
        arrOp = False

        # let keyword
        self._advance()

        # variable name
        varName = self.tokenizer.identifier()
        varIdx = self.symbolTable.indexOf(varName)
        varKind = self.symbolTable.kindOf(varName)
        varSegment = self._kindToSegment(varKind)

        self._advance()

        if self.tokenType == "symbol" and self.tokenizer.symbol() == "[":
            arrOp = True
            self.vmWriter.writePush(varSegment, varIdx)

            self._advance()

            self.compileExpression()

            self._advance()

            self.vmWriter.writeArithmetic(Command.ADD)
            self.vmWriter.writePop("temp", 0)

            varSegment = "that"
            varIdx = 0

        # "="
        self._advance()

        # right expression
        self.compileExpression()

        if arrOp:
            self.vmWriter.writePush("temp", 0)
            self.vmWriter.writePop("pointer", 1)

        self.vmWriter.writePop(varSegment, varIdx)

        # semicolon
        self._advance()


    def compileWhile(self) -> None:
        loopLabel = self._newLabel()
        escapeLabel = self._newLabel()

        self.vmWriter.writeLabel(loopLabel)

        self._advance()
        self._advance()

        self.compileExpression()
        self.vmWriter.writeArithmetic(Command.NOT)

        self.vmWriter.writeIf(escapeLabel)

        self._advance()
        self._advance()

        self.compileStatements()

        self.vmWriter.writeGoto(loopLabel)


        self.vmWriter.writeLabel(escapeLabel)
        self._advance()


    def compileReturn(self) -> None:
        # return keyword
        self._advance()

        if self.isVoid:
            self.vmWriter.writePush("constant", 0)

        elif self.tokenType != "symbol":
            self.compileExpression()

        # semicolon
        self._advance()

        self.vmWriter.writeReturn()


    def compileIf(self) -> None:
        trueLabel = self._newLabel()
        falseLabel = self._newLabel()

        self._advance()
        self._advance()

        self.compileExpression()
        self.vmWriter.writeArithmetic(Command.NOT)

        self._advance()
        self._advance()

        self.vmWriter.writeIf(falseLabel)

        self.compileStatements()
        self.vmWriter.writeGoto(trueLabel)

        self._advance()

        self.vmWriter.writeLabel(falseLabel)

        if self.tokenType == "keyword" and self.tokenizer.keyword() == "else":
            self._advance()
            self._advance()

            self.compileStatements()
            self._advance()

        self.vmWriter.writeLabel(trueLabel)
        

    def compileExpression(self) -> None:
        self.compileTerm()

        while self.tokenizer.symbol() in self.OP:
            symbol = self.tokenizer.symbol()

            self._advance()

            self.compileTerm()

            if symbol in ["*", "/"]:
                self._mathOp(symbol)

            else:
                op = self._symToCommand(symbol)
                self.vmWriter.writeArithmetic(op)


    def compileTerm(self) -> None:
        if self.tokenType in ["int_const", "string_const"]:
            self._writeConstant()
            self._advance()

        elif self.tokenType == "keyword":
            keyword = self.tokenizer.keyword()

            if keyword == "null":
                self.vmWriter.writePush("constant", 0)

            elif keyword == "this": # return this
                self.vmWriter.writePush("pointer", 0)

            elif keyword == "true":
                self.vmWriter.writePush("constant", 0)
                self.vmWriter.writeArithmetic(Command.NOT)

            elif keyword == "false":
                self.vmWriter.writePush("constant", 0)

            self._advance()

        elif self.tokenType == "identifier": 
            # identifier | identifier '[' expression ']' 
            # identifier(expList) | identifier.functionName(expList)
            name = self.tokenizer.identifier()
            self._advance()

            if self.tokenType == "symbol":
                symbol = self.tokenizer.symbol() 

                if symbol == "[": # array
                    self._advance()

                    varKind = self.symbolTable.kindOf(name)
                    varSegment = self._kindToSegment(varKind)
                    varIdx = self.symbolTable.indexOf(name)

                    self.vmWriter.writePush(varSegment, varIdx)

                    self.compileExpression()

                    self.vmWriter.writeArithmetic(Command.ADD)

                    self.vmWriter.writePop("pointer", 1)
                    self.vmWriter.writePush("that", 0)

                    self._advance()
                
                elif symbol == "(": # method call
                    self.vmWriter.writePush("pointer", 0)

                    nArgs = self.compileExpressionList() + 1
                    self.vmWriter.writeCall(self.className + "." + name, nArgs)

                    self._advance()

                elif symbol == ".": # className.subroutineName(expList)
                    nArgs = 0
                    varIdx = self.symbolTable.indexOf(name)

                    if varIdx != None:
                        varKind = self.symbolTable.kindOf(name)
                        varSegment = self._kindToSegment(varKind)
                        name = self.symbolTable.typeOf(name)
                        nArgs = 1

                        self.vmWriter.writePush(varSegment, varIdx)

                    name += self.tokenizer.symbol()

                    self._advance()
                    name += self.tokenizer.identifier()

                    # (
                    self._advance()

                    nArgs += self.compileExpressionList()
                    self.vmWriter.writeCall(name, nArgs)

                    # )
                    self._advance()

                else:
                    varKind = self.symbolTable.kindOf(name)
                    varSegment = self._kindToSegment(varKind)
                    varIdx = self.symbolTable.indexOf(name)

                    self.vmWriter.writePush(varSegment, varIdx)


        elif self.tokenType == "symbol": # '(' expression ')' | unary op
            symbol = self.tokenizer.symbol()

            if symbol == "(":
                self._advance()

                self.compileExpression()
                self._advance()

            elif symbol in ["~", "-"]:
                symbol = self.tokenizer.symbol()
                command = self._symToCommand(symbol, unary=True)
                self._advance()

                self.compileTerm()
                self.vmWriter.writeArithmetic(command)


    def compileExpressionList(self) -> int:
        is_empty = False
        prevType = self.tokenType
        symbol = self.tokenizer.symbol()
        nArgs = 0
        self.isExpList = True

        self._advance()

        if self.tokenType == 'symbol' and self.tokenizer.symbol() == ")":
            is_empty = True

        if prevType == 'symbol' and symbol != "(":
            if not is_empty:
                self.compileExpression()

                while self.tokenType == 'symbol' and symbol == ",":
                    self._advance()
                    self.compileExpression()

        if prevType == 'symbol' and symbol == "(":
            if not is_empty:
                self.compileExpression()
                nArgs += 1

                if self.tokenType == "symbol":
                    symbol = self.tokenizer.symbol()

                while self.tokenType == 'symbol' and symbol == ",":
                    self._advance()
                    nArgs += 1
                    self.compileExpression()

                    if self.tokenType == "symbol":
                        symbol = self.tokenizer.symbol()

        self.isExpList = False
        return nArgs

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


    def _writeConstant(self):
        if self.tokenType == "string_const":
            token = self.tokenizer.stringVal()
            self.vmWriter.writePush("constant", len(token))
            self.vmWriter.writeCall("String.new", 1)
            
            for c in token:
                self.vmWriter.writePush("constant", ord(c))
                self.vmWriter.writeCall("String.appendChar", 2)
            
        elif self.tokenType == "int_const":
            token = self.tokenizer.intVal()
            self.vmWriter.writePush("constant", token)


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
        
    def _symToCommand(self, symbol:str, unary:bool=False) -> Command:
        if unary:
            if symbol == "-":
                return Command.NEG
            
            elif symbol == "~":
                return Command.NOT 

        else:
            if symbol == "+":
                return Command.ADD

            elif symbol == "-":
                return Command.SUB
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

        
    def _newLabel(self):
        label = "LABEL" + str(self.labelCnt)
        self.labelCnt += 1
        return label

    def _mathOp(self, op):
        if op == "*":
            self.vmWriter.writeCall("Math.multiply", 2)
        elif op == "/":
            self.vmWriter.writeCall("Math.divide", 2)
