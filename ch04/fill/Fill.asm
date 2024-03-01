// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen
// by writing 'black' in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen by writing
// 'white' in every pixel;
// the screen should remain fully clear as long as no key is pressed.

//// Replace this comment with your code.

// R0 => saves if screen should be black or not
// R1 => saves current state of screen
// R2 => saves offset relative to screen memory starting address
// R3 => temp for saving current address for current handling pixel
// R4 => Debugging
    @0
    D=A
    @R0
    M=D
    @offset
    M=0
    @8191
    D=A
    @R2
    M=D
(LOOP1)
    // checks if keyboard is pressed
    @24576
    D=M
    @R4
    M=D
    @TO_BLACK
    D; JGT
    @TO_WHITE
    D; JEQ
(END1)
    @LOOP1
    0; JMP

(LOOP2)
    @offset
    D=M
    @R2
    D=D-M
    @END2
    D; JGT
    @SCREEN
    D=A
    @offset
    D=D+M
    @R3
    M=D
    // paint it
    // load if should be white or black
    @R0
    D=M
    @R3
    A=M
    M=D
    @1
    D=A
    @offset
    M=D+M
    @LOOP2
    0;JMP
(END2)
    @offset
    M=0
    @8191
    D=A
    @R2
    M=D
    @LOOP1
    0; JMP
(TO_BLACK)
    @R0
    M=-1
    @LOOP2
    0; JMP
(TO_WHITE)
    @R0
    M=0
    @LOOP2
    0; JMP

