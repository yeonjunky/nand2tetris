// initialize
@256
D=A
@SP
M=D
@Sys.init.return0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@0
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(Sys.init.return0)


//function Sys.init 0
(Sys.init)
D=0

//push constant 4000	// tests that THIS and THAT are handled correctly
@4000
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop pointer 0
@R3
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

//push constant 5000
@5000
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop pointer 1
@R4
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

//call Sys.main 0
@Sys.main.return1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@0
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.main
0;JMP
(Sys.main.return1)

//pop temp 1
@R6
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

//label LOOP
(NestedCall.LOOP)

//goto LOOP
@NestedCall.LOOP
0;JMP

//function Sys.main 5
(Sys.main)
D=0
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M
M=D
@SP
M=M+1

//push constant 4001
@4001
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop pointer 0
@R3
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

//push constant 5001
@5001
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop pointer 1
@R4
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

//push constant 200
@200
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop local 1
@LCL
D=M
@1
A=A+D
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

//push constant 40
@40
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop local 2
@LCL
D=M
@2
A=A+D
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

//push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop local 3
@LCL
D=M
@3
A=A+D
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

//push constant 123
@123
D=A
@SP
A=M
M=D
@SP
M=M+1

//call Sys.add12 1
@Sys.add12.return2
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.add12
0;JMP
(Sys.add12.return2)

//pop temp 0
@R5
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

//push local 0
@LCL
D=M
@0
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1

//push local 1
@LCL
D=M
@1
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1

//push local 2
@LCL
D=M
@2
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1

//push local 3
@LCL
D=M
@3
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1

//push local 4
@LCL
D=M
@4
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1

//add
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M+D

//add
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M+D

//add
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M+D

//add
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M+D

//return
@LCL
D=M
@R13
M=D
@R13
D=M
@5
D=D-A
A=D
D=M
@R14
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@R13
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
@R13
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@R13
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@R13
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@R14
A=M
0;JMP

//function Sys.add12 0
(Sys.add12)
D=0

//push constant 4002
@4002
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop pointer 0
@R3
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

//push constant 5002
@5002
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop pointer 1
@R4
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

//push argument 0
@ARG
D=M
@0
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1

//push constant 12
@12
D=A
@SP
A=M
M=D
@SP
M=M+1

//add
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M+D

//return
@LCL
D=M
@R13
M=D
@R13
D=M
@5
D=D-A
A=D
D=M
@R14
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@R13
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
@R13
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@R13
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@R13
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@R14
A=M
0;JMP

