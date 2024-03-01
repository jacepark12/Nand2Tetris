// start of [SimpleFunction.test 2]

(SimpleFunction.SimpleFunction.test)
@2
D=A
(SimpleFunction.SimpleFunction.test_PUSH_LOCAL_VAR_K)
@SimpleFunction.SimpleFunction.test_END_PUSH
D;JEQ
@SP
A=M
M=0
@SP
M=M+1
D=D-1
@SimpleFunction.SimpleFunction.test_PUSH_LOCAL_VAR_K
0;JMP
(SimpleFunction.SimpleFunction.test_END_PUSH)
// end of [SimpleFunction.test 2]
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
// start of [push local 1]

@LCL
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
// end of [push local 1]
// start of [add]

@SP
AM=M-1
D=M
@SP
A=M-1
M=D+M
// end of [add]
// start of [not]

@SP
A=M-1
M=!M
// end of [not]
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
// start of []

// FRAME=LCL
@LCL
D=M
@FRAME // temp 0
M=D
//RET = *(FRAME-5)
@5
D=D-A
A=D
D=M
@RET
M=D
// *ARG = pop()
@SP
AM=M-1
D=M
@ARG
A=M
M=D
// SP = ARG+1
@ARG
D=M
@SP
M=D+1
// THAT =*(FRAME-1)
@FRAME
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
// THIS =*(FRAME-2)
@FRAME
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
// ARG =*(FRAME-3)
@FRAME
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
// LCL =*(FRAME-4)
@FRAME
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
// goto RET
@RET
D=M
A=D
0;JMP
// end of []
(END)
@END
0;JMP