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
// start of [push constant 0]

@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 0]
// start of [pop that 0]

@THAT 
D=M
@0
D=A+D
@SP
AM=M-1
M=D+M
D=M-D
A=M-D
M=D
// end of [pop that 0]
// start of [push constant 1]

@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 1]
// start of [pop that 1]

@THAT 
D=M
@1
D=A+D
@SP
AM=M-1
M=D+M
D=M-D
A=M-D
M=D
// end of [pop that 1]
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
// start of [push constant 2]

@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 2]
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
// start of [COMPUTE_ELEMENT]

@SP
AM=M-1
D=M
@null$COMPUTE_ELEMENT
D;JNE
// end of [COMPUTE_ELEMENT]
// start of [END]

@null$END
0;JMP
// end of [END]
// start of [COMPUTE_ELEMENT]
(null$COMPUTE_ELEMENT)
// end of [COMPUTE_ELEMENT]
// start of [push that 0]

@THAT 
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
// end of [push that 0]
// start of [push that 1]

@THAT 
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
// end of [push that 1]
// start of [add]

@SP
AM=M-1
D=M
@SP
A=M-1
M=D+M
// end of [add]
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
// start of [push constant 1]

@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 1]
// start of [add]

@SP
AM=M-1
D=M
@SP
A=M-1
M=D+M
// end of [add]
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
// start of [LOOP]

@null$LOOP
0;JMP
// end of [LOOP]
// start of [END]
(null$END)
// end of [END]
(END)
@END
0;JMP