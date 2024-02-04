@17
D=A
@SP
A=M
M=D
@SP
M=M+1

@17
D=A
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
D=M-D
M=-1
@jump0
D;JEQ
@SP
A=M-1
M=0
(jump0)

@17
D=A
@SP
A=M
M=D
@SP
M=M+1

@16
D=A
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
D=M-D
M=-1
@jump1
D;JEQ
@SP
A=M-1
M=0
(jump1)

@16
D=A
@SP
A=M
M=D
@SP
M=M+1

@17
D=A
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
D=M-D
M=-1
@jump2
D;JEQ
@SP
A=M-1
M=0
(jump2)

@892
D=A
@SP
A=M
M=D
@SP
M=M+1

@891
D=A
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
D=M-D
M=-1
@jump3
D;JLT
@SP
A=M-1
M=0
(jump3)

@891
D=A
@SP
A=M
M=D
@SP
M=M+1

@892
D=A
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
D=M-D
M=-1
@jump4
D;JLT
@SP
A=M-1
M=0
(jump4)

@891
D=A
@SP
A=M
M=D
@SP
M=M+1

@891
D=A
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
D=M-D
M=-1
@jump5
D;JLT
@SP
A=M-1
M=0
(jump5)

@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

@32766
D=A
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
D=M-D
M=-1
@jump6
D;JGT
@SP
A=M-1
M=0
(jump6)

@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

@32767
D=A
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
D=M-D
M=-1
@jump7
D;JGT
@SP
A=M-1
M=0
(jump7)

@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

@32766
D=A
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
D=M-D
M=-1
@jump8
D;JGT
@SP
A=M-1
M=0
(jump8)

@57
D=A
@SP
A=M
M=D
@SP
M=M+1

@31
D=A
@SP
A=M
M=D
@SP
M=M+1

@53
D=A
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

@112
D=A
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

@SP
A=M-1
M=-M

@SP
AM=M-1
D=M
@SP
A=M-1
M=M&D

@82
D=A
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
M=M|D

@SP
A=M-1
M=!M

(END)
@END
0;JMP
