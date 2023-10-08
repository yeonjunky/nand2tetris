// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.
  @sum
  M=0

  @i
  M=0

(MULTLOOP)
  @R1
  D=M

  @i
  D=D-M
  @RESULT
  D;JLE // break the loop
  
  @R0 // if R1-i < 0 is not true
  D=M // continue the following code

  @sum
  M=M+D

  @i
  M=M+1

  @MULTLOOP
  0;JMP // back to (MULLOOP)

  (RESULT)
  // break the loop
  @sum
  D=M

  @R2
  M=D

(END)
  @END // ended all computation
  0;JMP // dive into infinite loop

