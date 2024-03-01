// start of [Class1.set 0]

(Class1.Class1.set)
@0
D=A
(Class1.Class1.set_PUSH_LOCAL_VAR_K)
@Class1.Class1.set_END_PUSH
D;JEQ
@SP
A=M
M=0
@SP
M=M+1
D=D-1
@Class1.Class1.set_PUSH_LOCAL_VAR_K
0;JMP
(Class1.Class1.set_END_PUSH)
// end of [Class1.set 0]
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
// start of [pop static 0]

@Class1.0
D=A
@SP
AM=M-1
M=D+M
D=M-D
A=M-D
M=D
// end of [pop static 0]
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
// start of [pop static 1]

@Class1.1
D=A
@SP
AM=M-1
M=D+M
D=M-D
A=M-D
M=D
// end of [pop static 1]
// start of [push constant 0]

@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 0]
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
// start of [Class1.get 0]

(Class1.Class1.get)
@0
D=A
(Class1.Class1.get_PUSH_LOCAL_VAR_K)
@Class1.Class1.get_END_PUSH
D;JEQ
@SP
A=M
M=0
@SP
M=M+1
D=D-1
@Class1.Class1.get_PUSH_LOCAL_VAR_K
0;JMP
(Class1.Class1.get_END_PUSH)
// end of [Class1.get 0]
// start of [push static 0]

@Class1.0
D=M
@SP
A=M
M=D
@SP
M=M+1
// end of [push static 0]
// start of [push static 1]

@Class1.1
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
// start of [push constant 6]

@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 6]
// start of [push constant 8]

@8
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 8]
// start of [Class1.set 2]

@Sys.Class1.set$return-address
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
@2
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
@Sys.Class1.set
0;JMP
(Sys.Class1.set$return-address)
// end of [Class1.set 2]
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
// start of [push constant 23]

@23
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 23]
// start of [push constant 15]

@15
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 15]
// start of [Class2.set 2]

@Sys.Class2.set$return-address
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
@2
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
@Sys.Class2.set
0;JMP
(Sys.Class2.set$return-address)
// end of [Class2.set 2]
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
// start of [Class1.get 0]

@Sys.Class1.get$return-address
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
@Sys.Class1.get
0;JMP
(Sys.Class1.get$return-address)
// end of [Class1.get 0]
// start of [Class2.get 0]

@Sys.Class2.get$return-address
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
@Sys.Class2.get
0;JMP
(Sys.Class2.get$return-address)
// end of [Class2.get 0]
// start of [END]
(Sys.Class2.get$END)
// end of [END]
// start of [END]

@Sys.Class2.get$END
0;JMP
// end of [END]
// start of [Class2.set 0]

(Class2.Class2.set)
@0
D=A
(Class2.Class2.set_PUSH_LOCAL_VAR_K)
@Class2.Class2.set_END_PUSH
D;JEQ
@SP
A=M
M=0
@SP
M=M+1
D=D-1
@Class2.Class2.set_PUSH_LOCAL_VAR_K
0;JMP
(Class2.Class2.set_END_PUSH)
// end of [Class2.set 0]
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
// start of [pop static 0]

@Class2.0
D=A
@SP
AM=M-1
M=D+M
D=M-D
A=M-D
M=D
// end of [pop static 0]
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
// start of [pop static 1]

@Class2.1
D=A
@SP
AM=M-1
M=D+M
D=M-D
A=M-D
M=D
// end of [pop static 1]
// start of [push constant 0]

@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 0]
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
// start of [Class2.get 0]

(Class2.Class2.get)
@0
D=A
(Class2.Class2.get_PUSH_LOCAL_VAR_K)
@Class2.Class2.get_END_PUSH
D;JEQ
@SP
A=M
M=0
@SP
M=M+1
D=D-1
@Class2.Class2.get_PUSH_LOCAL_VAR_K
0;JMP
(Class2.Class2.get_END_PUSH)
// end of [Class2.get 0]
// start of [push static 0]

@Class2.0
D=M
@SP
A=M
M=D
@SP
M=M+1
// end of [push static 0]
// start of [push static 1]

@Class2.1
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