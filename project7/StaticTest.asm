@111
D=A
@SP
A=M
M=D
@SP
M=M+1

@333
D=A
@SP
A=M
M=D
@SP
M=M+1

@888
D=A
@SP
A=M
M=D
@SP
M=M+1

@StaticTest.8
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D

@StaticTest.3
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D

@StaticTest.1
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D

@StaticTest.3
D=M
@SP
A=M
M=D
@SP
M=M+1

@StaticTest.1
D=M
@SP
A=M
M=D
@SP
M=M+1

@SP
AM=M-1
D=M
@SP
A=M-1
M=M-D

@StaticTest.8
D=M
@SP
A=M
M=D
@SP
M=M+1

@SP
AM=M-1
D=M
@SP
A=M-1
M=M+D

(END)
@END
0;JMP
