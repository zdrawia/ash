from .log import logger


class CPU:
    def __init__(self):
        self.register_a:      int = 0
        self.register_x:      int = 0
        self.status:          int = 0
        self.program_counter: int = 0

    def lda(self, value: int) -> None:
        self.register_a = value
        self.update_zero_and_negative_flags(self.register_a)

    def tax(self) -> None:
        self.register_x = self.register_a
        self.update_zero_and_negative_flags(self.register_x)

    def update_zero_and_negative_flags(self, result: int):
        if result == 0:
            self.status |= 0b0000_0010
        else:
            self.status &= 0b1111_1101

        if result & 0b1000_0000 != 0:
            self.status |= 0b1000_0000
        else:
            self.status &= 0b0111_1111

    def interpret(self, program: list[int]) -> None:
        """
        Interprets the given program.

        Args:
            program (list[int]): The program to be interpreted.

        Returns:
            None: This function does not return anything.
        """
        self.program_counter = 0

        while True:
            opcode = program[self.program_counter]
            logger.debug(f"opcode encountered: {hex(opcode)}")
            self.program_counter += 1

            match opcode:
                case 0xA9:
                    param = program[self.program_counter]
                    self.program_counter += 1

                    self.lda(param)
                case 0xAA:
                    self.tax()
                case 0x00:
                    break
                case _: pass
