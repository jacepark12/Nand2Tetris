// start of [push constant 111]

@111
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 111]
// start of [push constant 333]

@333
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 333]
// start of [push constant 888]

@888
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 888]
// start of [pop static 8]

@StaticTest.8
D=A
@SP
AM=M-1
M=D+M
D=M-D
A=M-D
M=D
// end of [pop static 8]
// start of [pop static 3]

@StaticTest.3
D=A
@SP
AM=M-1
M=D+M
D=M-D
A=M-D
M=D
// end of [pop static 3]
// start of [pop static 1]

@StaticTest.1
D=A
@SP
AM=M-1
M=D+M
D=M-D
A=M-D
M=D
// end of [pop static 1]
// start of [push static 3]

@StaticTest.3
D=M
@SP
A=M
M=D
@SP
M=M+1
// end of [push static 3]
// start of [push static 1]

@StaticTest.1
D=M
@SP
A=M
M=D
@SP
M=M+1
// end of [push static 1]
// start of [sub]

@SP
AM=M-1
D=M
@SP
A=M-1
M=M-D
// end of [sub]
// start of [push static 8]

@StaticTest.8
D=M
@SP
A=M
M=D
@SP
M=M+1
// end of [push static 8]
// start of [add]

@SP
AM=M-1
D=M
@SP
A=M-1
M=D+M
// end of [add]
(END)
@END
0;JMP