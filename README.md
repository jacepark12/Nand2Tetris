# Nand2Tetris
* Project of [The Elements of Computing Systems](https://www.nand2tetris.org/)
* [Review blog](https://jspark.blog/elements-of-computing-system/)

# Completed Projects
- [x] 1. Boolean Logic
- [x] 2. Boolean Arithmetic
- [x] 3. Sequential Logic
- [x] 4. Machine Language
- [x] 5. Computer Architecture
- [x] 6. Assembler
- [x] 7. Virtual Machine I: Stack Arithmetic
- [x] 8. Virtual Machine II: ProgramControl
- [x] 9. High-Level Language
- [x] 10. Compiler I: Syntax Analys
- [x] 11. Compiler II: Code Generation
- [x] 12. Operating System

# Chapter 1. Boolean Logic

- [x] Xor
- [x] Not16
- [x] Mux
- [x] DMux
- [x] Mux16
- [x] Mux4Way16

# Chapter 2. Boolean Arithmetic

- [x] HalfAdder
- [x] FullAdder
- [x] Inc16
- [x] ALU

# Chapter 3. Sequential Logic

- [x] 1 Bit register
- [x] 16 Bit register
- [x] RAM8
- [x] PC

# Chapter 4. Machine Language

- [x] Mult.asm (Multiplication Program)
- [x] Fill.asm (I/O-Handling Program)

# Chapter 5. Computer Architecture

- [x] Memory
- [x] 16-bit 6-opcode CPU
- [x] Computer Chip

# Chapter 6. Assembler

- [x] Assembler (python)
    - [x] Add.asm
    - [x] Max.asm

# Chapter. 7 Virtual Machine I: Stack Arithmetic
* [vm_translater/code_writer.py](https://github.com/jacepark12/Nand2Tetris/blob/main/vm_translator/code_writer.py)
- [x] VM-Translator (python)
    - [x] SimpleAdd.vm
    - [x] StackTest.vm
    - [x] BasicTest.vm
    - [x] PointerTest.vm
    - [x] StaticTest.vm

# Chapter 8. Virtual Machine II: ProgramControl
* [vm_translater/code_writer.py](https://github.com/jacepark12/Nand2Tetris/blob/main/vm_translator/code_writer.py)

## Marker feature for easy debugging
https://github.com/jacepark12/Nand2Tetris/blob/02795f861fff8435742314408dfb20e3af773a80/vm_translator/code_writer.py#L7-L22

* Command marker decorator inserts comment while writing asm code.
```
// start of [push constant 10]
@10
D=A
@SP
A=M
M=D
@SP
M=M+1
// end of [push constant 10]
```

- [x] VM-Translator (python)
    - [x] ProgramFlow/BasicLoop
    - [x] ProgramFlow/FibonacciSeries
    - [x] FunctionCalls/SimpleFunction
    - [x] FunctionCalls/FibonacciElement
    - [x] FunctionCalls/StaticsTest

# Chapter 10. Compiler I: Syntax Analys
* [tokenizer.py](https://github.com/jacepark12/Nand2Tetris/blob/main/compiler/tokenizer.py)
- [x] JackAnalyzer

# Chapter 11. Compiler II: Code Generation

## Class definition for rule define
https://github.com/jacepark12/Nand2Tetris/blob/02795f861fff8435742314408dfb20e3af773a80/compiler/rule.py#L34-L57

## Example rule definition for parser
https://github.com/jacepark12/Nand2Tetris/blob/02795f861fff8435742314408dfb20e3af773a80/compiler/rule_definition.py#L10-L34

## Rule processing implementation
https://github.com/jacepark12/Nand2Tetris/blob/02795f861fff8435742314408dfb20e3af773a80/compiler/compile_engine.py#L342-L366

- [x] Seven
- [x] ConvertToBin
- [x] Square
- [X] Average
- [X] Pong
- [X] Complex Array

# Chapter 12. Operating System

- [x] Array.jack
- [x] Math.jack
- [x] Memory.jack
- [x] Sys.jack
- [X] Keyboard.jack
- [X] Screen.jack
- [X] Output.jack
- [X] String.jack
