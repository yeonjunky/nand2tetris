import re

comment_pattern = re.compile(r'//[^\n]*\n|/\*(.*?)\*/', re.DOTALL|re.MULTILINE)
empty_text = re.compile(r"\s*")


keyword = re.compile(r"\s*(class|method|function|constructor|int|boolean|char|void|var|static|field|let|do|if|else|while|return|true|false|null|this)\s*")

symbol_pattern = re.compile(r"\s*([{}()\[\].,;+\-*/&|<>=~])\s*")

identifier_pattern = re.compile(r"\s*([a-zA-z_][a-zA-Z0-9]*)\s*")

int_const_pattern = re.compile(r"\s*(\d+)\s*")

str_const_pattern = re.compile(r"\s*\"(.*)\"\s*")
