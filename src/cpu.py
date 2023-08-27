import ctypes
from .log import logger


class CPU:
    def __init__(self):
        self.register_a:      ctypes.c_uint8  = ctypes.c_uint8(0)
        self.register_x:      ctypes.c_uint8  = ctypes.c_uint8(0)
        self.status:          ctypes.c_uint8  = ctypes.c_uint8(0)
        self.program_counter: ctypes.c_uint16 = ctypes.c_uint16(0)

    def lda(self, value: int) -> None:
        self.register_a.value = value
        self.update_zero_and_negative_flags(self.register_a)

    def tax(self) -> None:
        self.register_x = self.register_a
        self.update_zero_and_negative_flags(self.register_x)

    def update_zero_and_negative_flags(self, result: ctypes.c_uint8):
        if result.value == 0:
            self.status.value |= 0b0000_0010
        else:
            self.status.value &= 0b1111_1101

        if result.value & 0b1000_0000 != 0:
            self.status.value |= 0b1000_0000
        else:
            self.status.value &= 0b0111_1111

    def interpret(self, program: ctypes.Array[ctypes.c_uint8]) -> None:
        """
        Interprets the given program.

        Args:
            program (ctypes.Array[ctypes.c_uint8]): The program to be interpreted.

        Returns:
            None: This function does not return anything.
        """
        self.program_counter.value = 0

        while True:
            opcode = program[self.program_counter.value]
            logger.debug(f"opcode encountered: {hex(opcode)}")
            self.program_counter.value += 1

            match opcode:
                case 0xA9:
                    param = program[self.program_counter.value]
                    self.program_counter.value += 1

                    self.lda(param)
                case 0xAA:
                    self.tax()
                case 0x00:
                    break
                case _: pass
