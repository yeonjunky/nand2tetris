import re

comment_pattern = re.compile(r'//[^\n]*\n|/\*(.*?)\*/', re.DOTALL|re.MULTILINE)
empty_text = re.compile(r"\s*")

# do miscompile double to 'do' and 'uble'. solved adding $ 
keyword = re.compile(r"^\s*(class|method|function|constructor|int|boolean|char|void|var|static|field|let|do$|if|else|while|return|true|false|null|this)\s*")

symbol_pattern = re.compile(r"\s*([{}()\[\].,;+\-*/&|<>=~])\s*")

identifier_pattern = re.compile(r"\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*")

int_const_pattern = re.compile(r"\s*(\d+)\s*")

str_const_pattern = re.compile(r"\s*\"(.*)\"\s*")
