// start of [push constant 10]

@10
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 10]
// start of [pop local 0]

@LCL
D=M
@0
D=A+D
@SP
AM=M-1
M=D+M
D=M-D
A=M-D
M=D
// end of [pop local 0]
// start of [push constant 21]

@21
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 21]
// start of [push constant 22]

@22
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 22]
// start of [pop argument 2]

@ARG
D=M
@2
D=A+D
@SP
AM=M-1
M=D+M
D=M-D
A=M-D
M=D
// end of [pop argument 2]
// start of [pop argument 1]

@ARG
D=M
@1
D=A+D
@SP
AM=M-1
M=D+M
D=M-D
A=M-D
M=D
// end of [pop argument 1]
// start of [push constant 36]

@36
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 36]
// start of [pop this 6]

@THIS
D=M
@6
D=A+D
@SP
AM=M-1
M=D+M
D=M-D
A=M-D
M=D
// end of [pop this 6]
// start of [push constant 42]

@42
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 42]
// start of [push constant 45]

@45
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 45]
// start of [pop that 5]

@THAT 
D=M
@5
D=A+D
@SP
AM=M-1
M=D+M
D=M-D
A=M-D
M=D
// end of [pop that 5]
// start of [pop that 2]

@THAT 
D=M
@2
D=A+D
@SP
AM=M-1
M=D+M
D=M-D
A=M-D
M=D
// end of [pop that 2]
// start of [push constant 510]

@510
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 510]
// start of [pop temp 6]

@5
D=A
@6
D=A+D
@SP
AM=M-1
M=D+M
D=M-D
A=M-D
M=D
// end of [pop temp 6]
// start of [push local 0]

@LCL
D=M
@0
D=A+D
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// end of [push local 0]
// start of [push that 5]

@THAT 
D=M
@5
D=A+D
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// end of [push that 5]
// start of [add]

@SP
AM=M-1
D=M
@SP
A=M-1
M=D+M
// end of [add]
// start of [push argument 1]

@ARG
D=M
@1
D=A+D
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// end of [push argument 1]
// start of [sub]

@SP
AM=M-1
D=M
@SP
A=M-1
M=M-D
// end of [sub]
// start of [push this 6]

@THIS
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
// end of [push this 6]
// start of [push this 6]

@THIS
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
// end of [push this 6]
// start of [add]

@SP
AM=M-1
D=M
@SP
A=M-1
M=D+M
// end of [add]
// start of [sub]

@SP
AM=M-1
D=M
@SP
A=M-1
M=M-D
// end of [sub]
// start of [push temp 6]

@5
D=A
@6
D=A+D
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// end of [push temp 6]
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