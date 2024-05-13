from Constants import *
import re_patterns


class JackTokenizer:
    def __init__(self, input_file):
        self.code = None

        with open(input_file, 'r') as f:
            self.code = f.read()

        self._clearComments()

        self._tokenType = None
        self._currToken = None
        self.rePatterns = [
            re_patterns.keyword, 
            re_patterns.symbol_pattern, 
            re_patterns.identifier_pattern, 
            re_patterns.int_const_pattern, 
            re_patterns.str_const_pattern
        ]

    def hasMoreTokens(self) -> bool:
        if re_patterns.empty_text.fullmatch(self.code):
            return False
        return True

    def advance(self) -> None:
        for p in self.rePatterns:
            match_result = p.match(self.code)

            if match_result:
                pattern = p
                break

        self._currToken = match_result.group(1)
        self.code = p.sub("", self.code, count=1)

        if pattern == re_patterns.keyword:
            self._tokenType = Tokentype.KEYWORD

        elif pattern == re_patterns.symbol_pattern:
            self._tokenType = Tokentype.SYMBOL

        elif pattern == re_patterns.identifier_pattern:
            self._tokenType = Tokentype.IDENTIFIER

        elif pattern == re_patterns.int_const_pattern:
            self._tokenType = Tokentype.INT_CONST

        elif pattern == re_patterns.str_const_pattern:
            self._tokenType = Tokentype.STRING_CONST

    def tokenType(self) -> str:
        return self._tokenType.name.lower()
    
    def keyword(self) -> str:
        return self._currToken

    def symbol(self) -> str:
        return self._currToken

    def identifier(self) -> str:
        return self._currToken

    def intVal(self) -> int:
        return int(self._currToken)

    def stringVal(self) -> str:
        return self._currToken
    
    def _clearComments(self):
        self.code = re_patterns.comment_pattern.sub("", self.code)

