import textwrap
from typing import List, Optional

END_LINES = ["(END)\n", "@END\n", "0;JMP"]


class CommandMarker:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        def wrapper(*args, **kwargs):
            command_string = " ".join([str(x) for x in args])
            if instance.debug_mode:
                instance.output_lines.append(f"// start of [{command_string}]\n")

            result = self.func(instance, *args, **kwargs)
            if instance.debug_mode:
                instance.output_lines.append(f"// end of [{command_string}]\n")
            return result

        return wrapper


class CodeWriter:

    def __init__(self):
        self.debug_mode: bool = True
        self.output_lines: List[str] = []
        self._file_name = ""
        self.label_index = 0
        self._current_function_name: Optional[str] = None

    @property
    def file_name(self) -> str:
        return self._file_name

    @file_name.setter
    def file_name(self, file_name: str):
        self._file_name = file_name

    @property
    def current_function_name(self) -> str:
        return (
            self._current_function_name
            if self._current_function_name is not None
            else "null"
        )

    # TODO : add function name validator
    @current_function_name.setter
    def current_function_name(self, value):
        self._current_function_name = value

    @CommandMarker
    def write_label(self, label: str):
        label = f"{self.current_function_name}${label}"
        self.output_lines.append(f"({label})\n")

    @CommandMarker
    def write_goto(self, label: str):
        asm_command = textwrap.dedent(
            f"""
            @{self.current_function_name}${label}
            0;JMP
        """
        )
        self.output_lines.append(asm_command)

    @CommandMarker
    def write_if(self, label: str):
        asm_command = textwrap.dedent(
            f"""
            @SP
            AM=M-1
            D=M
            @{self.current_function_name}${label}
            D;JNE
            """
        )
        self.output_lines.append(asm_command)

    # TODO : Push 부분은 추상화한번 더 할 수 있음
    @CommandMarker
    def write_call(self, function_name: str, num_args: int):
        function_name = f"{self.file_name}.{function_name}"
        self.current_function_name = function_name
        asm_command = textwrap.dedent(
            f"""
            @{function_name}$return-address
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
            @{num_args}
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
            @{function_name}
            0;JMP
            ({function_name}$return-address)
            """
        )
        self.output_lines.append(asm_command)

    @CommandMarker
    def write_return(self):
        asm_command = textwrap.dedent(
            f"""
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
            """
        )
        self.output_lines.append(asm_command)

    @CommandMarker
    def write_function(self, function_name: str, num_locals: int):
        function_name = f"{self.file_name}.{function_name}"
        asm_command = textwrap.dedent(
            f"""
            ({function_name})
            @{num_locals}
            D=A
            ({function_name}_PUSH_LOCAL_VAR_K)
            @{function_name}_END_PUSH
            D;JEQ
            @SP
            A=M
            M=0
            @SP
            M=M+1
            D=D-1
            @{function_name}_PUSH_LOCAL_VAR_K
            0;JMP
            ({function_name}_END_PUSH)
            """
        )
        self.output_lines.append(asm_command)

    @CommandMarker
    def write_arithmetic(self, command: str):
        asm_command = ""
        if command == "add":
            asm_command = textwrap.dedent(
                """
                @SP
                AM=M-1
                D=M
                @SP
                A=M-1
                M=D+M
                """
            )
        elif command == "sub":
            asm_command = textwrap.dedent(
                """
                @SP
                AM=M-1
                D=M
                @SP
                A=M-1
                M=M-D
                """
            )
        elif command == "neg":
            asm_command = textwrap.dedent(
                """
                @SP
                A=M-1
                M=-M
                """
            )
        elif command == "eq":
            asm_command = textwrap.dedent(
                f"""
                @SP
                AM=M-1
                D=M
                @SP
                AM=M-1
                D=M-D
                @PUSHTRUE_{self.label_index}
                D;JEQ
                @PUSHFALSE_{self.label_index}
                D;JNE
                (PUSHTRUE_{self.label_index})
                @SP
                A=M
                M=-1
                @END_{self.label_index}
                0;JMP
                (PUSHFALSE_{self.label_index})
                @SP
                A=M
                M=0
                @END_{self.label_index}
                0;JMP
                (END_{self.label_index})
                @SP
                M=M+1
                """
            )
            self.label_index += 1
        elif command == "gt":
            asm_command = textwrap.dedent(
                f"""
                @SP
                AM=M-1
                D=M
                @SP
                AM=M-1
                D=M-D
                @PUSHTRUE_{self.label_index}
                D;JGT
                @PUSHFALSE_{self.label_index}
                D;JLE
                (PUSHTRUE_{self.label_index})
                @SP
                A=M
                M=-1
                @END_{self.label_index}
                0;JMP
                (PUSHFALSE_{self.label_index})
                @SP
                A=M
                M=0
                @END_{self.label_index}
                0;JMP
                (END_{self.label_index})
                @SP
                M=M+1
                """
            )
            self.label_index += 1
        elif command == "lt":
            asm_command = textwrap.dedent(
                f"""
                @SP
                AM=M-1
                D=M
                @SP
                AM=M-1
                D=M-D
                @PUSHTRUE_{self.label_index}
                D;JLT
                @PUSHFALSE_{self.label_index}
                D;JGE
                (PUSHTRUE_{self.label_index})
                @SP
                A=M
                M=-1
                @END_{self.label_index}
                0;JMP
                (PUSHFALSE_{self.label_index})
                @SP
                A=M
                M=0
                @END_{self.label_index}
                0;JMP
                (END_{self.label_index})
                @SP
                M=M+1
                """
            )
            self.label_index += 1
        elif command == "and":
            asm_command = textwrap.dedent(
                """
                @SP
                AM=M-1
                D=M
                @SP
                A=M-1
                M=D&M
                """
            )
        elif command == "or":
            asm_command = textwrap.dedent(
                """
                @SP
                AM=M-1
                D=M
                @SP
                A=M-1
                M=D|M
                """
            )
        elif command == "not":
            asm_command = textwrap.dedent(
                """
                @SP
                A=M-1
                M=!M
                """
            )

        if asm_command != "":
            self.output_lines.append(asm_command)

    @CommandMarker
    def write_push_pop(self, command: str, segment: str, index: int):
        PREDEFINED_SEGMENTS = {
            "argument": "ARG",
            "local": "LCL",
            "this": "THIS",
            "that": "THAT ",
        }

        FIXED_SEGMENTS = {"pointer": "3", "temp": "5"}

        asm_command = ""
        if command == "pop":
            if segment in PREDEFINED_SEGMENTS:
                asm_command = textwrap.dedent(
                    f"""
                    @{PREDEFINED_SEGMENTS[segment]}
                    D=M
                    @{index}
                    D=A+D
                    @SP
                    AM=M-1
                    M=D+M
                    D=M-D
                    A=M-D
                    M=D
                    """
                )
            elif segment in FIXED_SEGMENTS:
                asm_command = textwrap.dedent(
                    f"""
                    @{FIXED_SEGMENTS[segment]}
                    D=A
                    @{index}
                    D=A+D
                    @SP
                    AM=M-1
                    M=D+M
                    D=M-D
                    A=M-D
                    M=D
                    """
                )
            elif segment == "static":
                asm_command = textwrap.dedent(
                    f"""
                    @{self._file_name}.{index}
                    D=A
                    @SP
                    AM=M-1
                    M=D+M
                    D=M-D
                    A=M-D
                    M=D
                    """
                )
        elif segment == "constant" and command == "push":
            asm_command = textwrap.dedent(
                f"""
                @{index}
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
                """
            )
        elif command == "push":
            if segment in PREDEFINED_SEGMENTS:
                asm_command = textwrap.dedent(
                    f"""
                    @{PREDEFINED_SEGMENTS[segment]}
                    D=M
                    @{index}
                    D=A+D
                    A=D
                    D=M
                    @SP
                    A=M
                    M=D
                    @SP
                    M=M+1
                    """
                )
            elif segment in FIXED_SEGMENTS:
                asm_command = textwrap.dedent(
                    f"""
                    @{FIXED_SEGMENTS[segment]}
                    D=A
                    @{index}
                    D=A+D
                    A=D
                    D=M
                    @SP
                    A=M
                    M=D
                    @SP
                    M=M+1
                    """
                )
            elif segment == "static":
                asm_command = textwrap.dedent(
                    f"""
                    @{self._file_name}.{index}
                    D=M
                    @SP
                    A=M
                    M=D
                    @SP
                    M=M+1
                    """
                )

        if asm_command != "":
            self.output_lines.append(asm_command)

