// start of [push constant 7]

@7
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 7]
// start of [push constant 8]

@8
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 8]
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