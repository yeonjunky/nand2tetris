// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// 1-1. detect keydown -> keyboard memory map > 0 is true ; goto 2
// 2. set all the screen register to -1(which is 1111111111111111 in binary)
// 1-2. detect keyup -> opposite with 1 keyboard memory map == 0 ; goto 3
// 3. set all the screen register to 0(same as keyboard memory map value)

// Put your code here.
// initialize the program
  @isclear 
  M=1

  @i
  M=0

  @8192
  D=A
  @numscrregi
  M=D

  @pixval
  M=0

  @target
  M=0


//initialize end

(LOOP)
  @KBD
  D=M
  
  @isclear
  D=D+M

  D=D-1

  @FILL
  D;JGT

  D=D+1

  @CLEAR
  D;JEQ

  @LOOP
  0;JMP

(FILL)
  @i
  M=0

  @isclear
  M=0

  (PERFORMFILL)
  @numscrregi
  D=M

  @i
  D=D-M

  @LOOP
  D;JLE // break loop

  @SCREEN
  D=A

  @i
  AD=D+M
  M=-1
  
  @i
  M=M+1

  @PERFORMFILL
  0;JMP


(CLEAR)
  @i
  M=0

  @isclear
  M=1

  (PERFORMCLEAR)
  @numscrregi
  D=M
  
  @i
  D=D-M

  @LOOP
  D;JLT // break loop

  @SCREEN
  D=A

  @i
  AD=D+M
  
  M=0
  
  @i
  M=M+1

  @PERFORMCLEAR
  0;JMP

(END)
  @END
  0;JMP