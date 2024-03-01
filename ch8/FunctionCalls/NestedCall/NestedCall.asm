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
// start of [push constant 4000]

@4000
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 4000]
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
// start of [push constant 5000]

@5000
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 5000]
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
// start of [Sys.main 0]

@Sys.Sys.main$return-address
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
@0
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
@Sys.Sys.main
0;JMP
(Sys.Sys.main$return-address)
// end of [Sys.main 0]
// start of [pop temp 1]

@5
D=A
@1
D=A+D
@SP
AM=M-1
M=D+M
D=M-D
A=M-D
M=D
// end of [pop temp 1]
// start of [LOOP]
(Sys.Sys.main$LOOP)
// end of [LOOP]
// start of [LOOP]

@Sys.Sys.main$LOOP
0;JMP
// end of [LOOP]
// start of [Sys.main 5]

(Sys.Sys.main)
@5
D=A
(Sys.Sys.main_PUSH_LOCAL_VAR_K)
@Sys.Sys.main_END_PUSH
D;JEQ
@SP
A=M
M=0
@SP
M=M+1
D=D-1
@Sys.Sys.main_PUSH_LOCAL_VAR_K
0;JMP
(Sys.Sys.main_END_PUSH)
// end of [Sys.main 5]
// start of [push constant 4001]

@4001
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 4001]
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
// start of [push constant 5001]

@5001
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 5001]
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
// start of [push constant 200]

@200
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 200]
// start of [pop local 1]

@LCL
D=M
@1
D=A+D
@SP
AM=M-1
M=D+M
D=M-D
A=M-D
M=D
// end of [pop local 1]
// start of [push constant 40]

@40
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 40]
// start of [pop local 2]

@LCL
D=M
@2
D=A+D
@SP
AM=M-1
M=D+M
D=M-D
A=M-D
M=D
// end of [pop local 2]
// start of [push constant 6]

@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 6]
// start of [pop local 3]

@LCL
D=M
@3
D=A+D
@SP
AM=M-1
M=D+M
D=M-D
A=M-D
M=D
// end of [pop local 3]
// start of [push constant 123]

@123
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 123]
// start of [Sys.add12 1]

@Sys.Sys.add12$return-address
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
@Sys.Sys.add12
0;JMP
(Sys.Sys.add12$return-address)
// end of [Sys.add12 1]
// start of [pop temp 0]

@5
D=A
@0
D=A+D
@SP
AM=M-1
M=D+M
D=M-D
A=M-D
M=D
// end of [pop temp 0]
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
// start of [push local 2]

@LCL
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
// end of [push local 2]
// start of [push local 3]

@LCL
D=M
@3
D=A+D
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// end of [push local 3]
// start of [push local 4]

@LCL
D=M
@4
D=A+D
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// end of [push local 4]
// start of [add]

@SP
AM=M-1
D=M
@SP
A=M-1
M=D+M
// end of [add]
// start of [add]

@SP
AM=M-1
D=M
@SP
A=M-1
M=D+M
// end of [add]
// start of [add]

@SP
AM=M-1
D=M
@SP
A=M-1
M=D+M
// end of [add]
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
// start of [Sys.add12 0]

(Sys.Sys.add12)
@0
D=A
(Sys.Sys.add12_PUSH_LOCAL_VAR_K)
@Sys.Sys.add12_END_PUSH
D;JEQ
@SP
A=M
M=0
@SP
M=M+1
D=D-1
@Sys.Sys.add12_PUSH_LOCAL_VAR_K
0;JMP
(Sys.Sys.add12_END_PUSH)
// end of [Sys.add12 0]
// start of [push constant 4002]

@4002
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 4002]
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
// start of [push constant 5002]

@5002
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 5002]
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
// start of [push constant 12]

@12
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 12]
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
(END)
@END
0;JMP