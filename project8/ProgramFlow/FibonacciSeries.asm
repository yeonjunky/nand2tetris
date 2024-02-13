//push argument 1         // sets THAT, the base address of the
@ARG
D=M
@1
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1

//pop pointer 1           // that segment, to argument[1]
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

//push constant 0         // sets the series' first and second
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop that 0              // elements to 0 and 1, respectively
@THAT
D=M
@0
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

//push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop that 1
@THAT
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

//push argument 0         // sets n, the number of remaining elements
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

//push constant 2         // to be computed to argument[0] minus 2,
@2
D=A
@SP
A=M
M=D
@SP
M=M+1

//sub                     // since 2 elements were already computed.
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M-D

//pop argument 0
@ARG
D=M
@0
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

//label LOOP
(FibonacciSeries.LOOP)

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

//if-goto COMPUTE_ELEMENT // if n > 0, goto COMPUTE_ELEMENT
@SP
M=M-1
A=M
D=M
@FibonacciSeries.COMPUTE_ELEMENT
D;JGT

//goto END                // otherwise, goto END
@FibonacciSeries.END
0;JMP

//label COMPUTE_ELEMENT
(FibonacciSeries.COMPUTE_ELEMENT)

//// that[2] = that[0] + that[1]
//push that 0
@THAT
D=M
@0
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1

//push that 1
@THAT
D=M
@1
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

//pop that 2
@THAT
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

//// THAT += 1 (updates the base address of that)
//push pointer 1
@R4
D=M
@SP
A=M
M=D
@SP
M=M+1

//push constant 1
@1
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

//// updates n-- and loops
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

//push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

//sub
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M-D

//pop argument 0
@ARG
D=M
@0
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

//goto LOOP
@FibonacciSeries.LOOP
0;JMP

//label END
(FibonacciSeries.END)

