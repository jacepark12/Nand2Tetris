// start of [push constant 0]

@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 0]
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
// start of [LOOP]
(null$LOOP)
// end of [LOOP]
// start of [push argument 0]

@ARG
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
// end of [push argument 0]
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
// start of [add]

@SP
AM=M-1
D=M
@SP
A=M-1
M=D+M
// end of [add]
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
// start of [push argument 0]

@ARG
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
// end of [push argument 0]
// start of [push constant 1]

@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 1]
// start of [sub]

@SP
AM=M-1
D=M
@SP
A=M-1
M=M-D
// end of [sub]
// start of [pop argument 0]

@ARG
D=M
@0
D=A+D
@SP
AM=M-1
M=D+M
D=M-D
A=M-D
M=D
// end of [pop argument 0]
// start of [push argument 0]

@ARG
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
// end of [push argument 0]
// start of [LOOP]

@SP
AM=M-1
D=M
@null$LOOP
D;JNE
// end of [LOOP]
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
(END)
@END
0;JMP