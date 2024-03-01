// start of [Main.fibonacci 0]

(Main.Main.fibonacci)
@0
D=A
(Main.Main.fibonacci_PUSH_LOCAL_VAR_K)
@Main.Main.fibonacci_END_PUSH
D;JEQ
@SP
A=M
M=0
@SP
M=M+1
D=D-1
@Main.Main.fibonacci_PUSH_LOCAL_VAR_K
0;JMP
(Main.Main.fibonacci_END_PUSH)
// end of [Main.fibonacci 0]
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
// start of [lt]

@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@PUSHTRUE_0
D;JLT
@PUSHFALSE_0
D;JGE
(PUSHTRUE_0)
@SP
A=M
M=-1
@END_0
0;JMP
(PUSHFALSE_0)
@SP
A=M
M=0
@END_0
0;JMP
(END_0)
@SP
M=M+1
// end of [lt]
// start of [N_LT_2]

@SP
AM=M-1
D=M
@null$N_LT_2
D;JNE
// end of [N_LT_2]
// start of [N_GE_2]

@null$N_GE_2
0;JMP
// end of [N_GE_2]
// start of [N_LT_2]
(null$N_LT_2)
// end of [N_LT_2]
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
// start of [N_GE_2]
(null$N_GE_2)
// end of [N_GE_2]
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
// start of [Main.fibonacci 1]

@Main.Main.fibonacci$return-address
D=A
@SP
A=M
M=D
@SP
M=M+1
// push lcl
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// push arg
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// push this
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// push that
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
@Main.Main.fibonacci
0;JMP
(Main.Main.fibonacci$return-address)
// end of [Main.fibonacci 1]
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
// start of [Main.fibonacci 1]

@Main.Main.fibonacci$return-address
D=A
@SP
A=M
M=D
@SP
M=M+1
// push lcl
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// push arg
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// push this
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// push that
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
@Main.Main.fibonacci
0;JMP
(Main.Main.fibonacci$return-address)
// end of [Main.fibonacci 1]
// start of [add]

@SP
AM=M-1
D=M
@SP
A=M-1
M=D+M
// end of [add]
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
// start of [Sys.init 0]

(Sys.Sys.init)
@0
D=A
(Sys.Sys.init_PUSH_LOCAL_VAR_K)
@Sys.Sys.init_END_PUSH
D;JEQ
@SP
A=M
M=0
@SP
M=M+1
D=D-1
@Sys.Sys.init_PUSH_LOCAL_VAR_K
0;JMP
(Sys.Sys.init_END_PUSH)
// end of [Sys.init 0]
// start of [push constant 4]

@4
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 4]
// start of [Main.fibonacci 1]

@Sys.Main.fibonacci$return-address
D=A
@SP
A=M
M=D
@SP
M=M+1
// push lcl
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// push arg
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// push this
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// push that
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
@Sys.Main.fibonacci
0;JMP
(Sys.Main.fibonacci$return-address)
// end of [Main.fibonacci 1]
// start of [END]
(Sys.Main.fibonacci$END)
// end of [END]
// start of [END]

@Sys.Main.fibonacci$END
0;JMP
// end of [END]
(END)
@END
0;JMP