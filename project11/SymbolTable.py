from Constants import Kind


class SymbolTable:
    def __init__(self) -> None:
        # table element 
        # key -> identifier
        # value -> [type, kind, index]

        self.classTable = {}
        self.classMemCnt = [0, 0] # static, field

        self.subroutineTable = {}
        self.subroutineMemCnt = [0, 0] # arg, var
        

    def startSubroutine(self) -> None:
        self.subroutineTable.clear()
        self.subroutineMemCnt = [0, 0]


    def define(self, name:str, type:str, kind:Kind) -> None:
        if kind == Kind.STATIC:
            idx = self.classMemCnt[0]
            self.classMemCnt[0] += 1
            self.classTable[name] = [type, kind, idx]

        elif kind == Kind.FIELD:
            idx = self.classMemCnt[1]
            self.classMemCnt[1] += 1
            self.classTable[name] = [type, kind, idx]

        elif kind == Kind.ARG:
            idx = self.subroutineMemCnt[0]
            self.subroutineMemCnt[0] += 1
            self.subroutineTable[name] = [type, kind, idx]

        elif kind == Kind.VAR:
            idx = self.subroutineMemCnt[1]
            self.subroutineMemCnt[1] += 1
            self.subroutineTable[name] = [type, kind, idx]


    def varCount(self, kind:Kind) -> int:
        if kind == Kind.STATIC:
            return self.classMemCnt[0]
            
        elif kind == Kind.FIELD:
            return self.classMemCnt[1]
            
        elif kind == Kind.ARG:
            return self.subroutineMemCnt[0]
            
        elif kind == Kind.VAR:
            return self.subroutineMemCnt[1]
            

    def kindOf(self, name:str) -> Kind:
        var = self.classTable.get(name)
        var = var if var else self.subroutineTable.get(name)

        if var is None:
            return None
        return var[1]


    def typeOf(self, name:str) -> str:
        var = self.classTable.get(name)
        var = var if var else self.subroutineTable.get(name)
        
        if var is None:
            return None
        return var[0]


    def indexOf(self, name:str) -> int:
        var = self.classTable.get(name)
        var = var if var else self.subroutineTable.get(name)

        if var is None:
            return None
        return var[2]
