from .log import logger, historical


class CPU:
    """
     _____________________
    |   Flags reference   |
    |_____________________|
    |    |0bxxxx_xxxx|    |
    |    |  *NVB DIZC|    |
    |    |___________|    |
    |                     |
    |N - Negative Flag    |
    |V - Overflow Flag    |
    |B - Break Command    |
    |D - Decimal Mode Flag|
    |I - Interrupt Disable|
    |Z - Zero Flag        |
    |C - Carry Flag       |
    |_____________________|

    """
    def __init__(self):
        self.register_a:      int = 0
        self.register_x:      int = 0
        self.register_y:      int = 0
        self.status:          int = 0
        self.program_counter: int = 0
        self.memory:          bytearray = bytearray(0xFFFF)

    def memory_read(self, address: int) -> int:
        return self.memory[address]

    def memory_write(self, address: int, data: int) -> None:
        self.memory[address] = data

    def memory_read_uint16(self, position: int) -> int:
        lo = self.memory_read(position)
        hi = self.memory_read(position + 1)
        return (hi << 8) | lo

    def memory_write_uint16(self, position: int, data: int) -> None:
        hi = data >> 8
        lo = data & 0xFF
        self.memory_write(position, lo)
        self.memory_write(position + 1, hi)

    @historical
    def reset(self):
        self.register_a = 0
        self.register_x = 0
        self.register_y = 0
        self.status = 0
        self.program_counter = self.memory_read_uint16(0xFFFC)

    def load_program(self, program: bytearray) -> None:
        self.memory[0x8000:0x8000 + len(program)] = program
        self.memory_write_uint16(0xFFFC, 0x8000)

    def load_and_run(self, program: bytearray, reset: bool = True) -> None:
        self.load_program(program)
        if reset: self.reset()
        self.run()

    def run(self) -> None:
        while True:
            instruction = self.memory_read(self.program_counter)
            self.program_counter += 1

            match instruction:
                case 0xA9:
                    param = self.memory_read(self.program_counter)
                    self.program_counter += 1

                    self.lda(param)
                case 0xAA:
                    self.tax()
                case 0x00:
                    break
                case _:
                    pass

    @historical
    def lda(self, value: int) -> None:
        """
        Loads a byte of memory into the accumulator setting the zero and negative flags as appropriate.
        Args:
            value: The byte of memory to be loaded

        Returns:
            None: This function does not return anything.
        """
        self.register_a = value
        self.update_zero_and_negative_flags(self.register_a)

    @historical
    def ldx(self, value: int) -> None:
        """
        Loads a byte of memory into the X register setting the zero and negative flags as appropriate.
        Args:
            value: The byte of memory to be loaded

        Returns:
            None: This function does not return anything.
        """
        self.register_x = value
        self.update_zero_and_negative_flags(self.register_x)

    @historical
    def ldy(self, value: int) -> None:
        """
        Loads a byte of memory into the Y register setting the zero and negative flags as appropriate.
        Args:
            value: The byte of memory to be loaded

        Returns:
            None: This function does not return anything.
        """
        self.register_y = value
        self.update_zero_and_negative_flags(self.register_y)

    @historical
    def tax(self) -> None:
        """
        Copies the current contents of the accumulator into the X register
        and sets the zero and negative flags as appropriate.

        Returns:
            None: This function does not return anything.
        """
        self.register_x = self.register_a
        self.update_zero_and_negative_flags(self.register_x)

    @historical
    def inx(self) -> None:
        """
        Adds one to the X register setting the zero and negative flags as appropriate.

        Returns:
            None: This function does not return anything.
        """
        self.register_x += 1
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
