// start of [push constant 3030]

@3030
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 3030]
// start of [pop pointer 0]

@3
D=A
@0
D=A+D
@SP
AM=M-1
M=D+M
D=M-D
A=M-D
M=D
// end of [pop pointer 0]
// start of [push constant 3040]

@3040
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 3040]
// start of [pop pointer 1]

@3
D=A
@1
D=A+D
@SP
AM=M-1
M=D+M
D=M-D
A=M-D
M=D
// end of [pop pointer 1]
// start of [push constant 32]

@32
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 32]
// start of [pop this 2]

@THIS
D=M
@2
D=A+D
@SP
AM=M-1
M=D+M
D=M-D
A=M-D
M=D
// end of [pop this 2]
// start of [push constant 46]

@46
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 46]
// start of [pop that 6]

@THAT 
D=M
@6
D=A+D
@SP
AM=M-1
M=D+M
D=M-D
A=M-D
M=D
// end of [pop that 6]
// start of [push pointer 0]

@3
D=A
@0
D=A+D
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// end of [push pointer 0]
// start of [push pointer 1]

@3
D=A
@1
D=A+D
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// end of [push pointer 1]
// start of [add]

@SP
AM=M-1
D=M
@SP
A=M-1
M=D+M
// end of [add]
// start of [push this 2]

@THIS
D=M
@2
D=A+D
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// end of [push this 2]
// start of [sub]

@SP
AM=M-1
D=M
@SP
A=M-1
M=M-D
// end of [sub]
// start of [push that 6]

@THAT 
D=M
@6
D=A+D
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// end of [push that 6]
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