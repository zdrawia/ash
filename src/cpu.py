from .addressingmode import AddressingMode
from .log import historical, logger
from .opcodes import OPCODES_MAP, Opcode
from .types import uint8, uint16


class CPU:
    """
     _____________________
    |   Flags reference   |
    |_____________________|
    |    |0bxxxx_xxxx|    |
    |    |  NV1B DIZC|    |
    |    |___________|    |
    |                     |
    |1 - No CPU effect    |
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
        self.register_a:      uint8     = uint8(0)
        self.register_x:      uint8     = uint8(0)
        self.register_y:      uint8     = uint8(0)
        self.status:          uint8     = uint8(0)
        self.program_counter: uint16    = uint16(0)
        self.memory:          bytearray = bytearray(0xFFFF)

    def get_operand_address(self, mode: AddressingMode) -> uint16:
        match mode:
            case AddressingMode.Immediate:
                return self.program_counter
            case AddressingMode.ZeroPage:
                return uint16(self.memory_read(self.program_counter))
            case AddressingMode.ZeroPage_X:
                return uint16(self.memory_read(self.program_counter) + self.register_x)
            case AddressingMode.ZeroPage_Y:
                return uint16(self.memory_read(self.program_counter) + self.register_y)
            case AddressingMode.Absolute:
                return self.memory_read_uint16(self.program_counter)
            case AddressingMode.Absolute_X:
                return uint16(self.memory_read_uint16(self.program_counter) + self.register_x)
            case AddressingMode.Absolute_Y:
                return uint16(self.memory_read_uint16(self.program_counter) + self.register_y)
            case AddressingMode.Indirect_X:
                base = self.memory_read(self.program_counter)
                ptr = base + self.register_x
                lo = self.memory_read(uint16(ptr))
                hi = self.memory_read(uint16(ptr + 1))
                return (uint16(hi) << 8) | uint16(lo)
            case AddressingMode.Indirect_Y:
                base = self.memory_read(self.program_counter)
                lo = self.memory_read(uint16(base))
                hi = self.memory_read(uint16(base.increment()))
                deref_base = (uint16(hi) << 8) | uint16(lo)
                return uint16(deref_base + self.register_y)
            case AddressingMode.NoneAddressing:
                logger.error(f"Mode {mode} is not supported!")
                return uint16(-0xE7707)

    def memory_read(self, address: uint16) -> uint8:
        return uint8(self.memory[address])

    def memory_write(self, address: uint16, data: uint8) -> None:
        self.memory[address] = data

    def memory_read_uint16(self, position: uint16) -> uint16:
        lo = uint16(self.memory_read(position))
        hi = uint16(self.memory_read(position.increment()))
        return (hi << 8) | lo

    def memory_write_uint16(self, position: uint16, data: uint16) -> None:
        hi = data >> uint8(8)
        lo = data & uint8(0xFF)
        self.memory_write(position, lo)
        self.memory_write(position.increment(), hi)

    @historical
    def reset(self):
        self.register_a = uint8(0)
        self.register_x = uint8(0)
        self.register_y = uint8(0)
        self.status = uint8(0)
        self.program_counter = uint16(self.memory_read_uint16(uint16(0xFFFC)))

    def load_program(self, program: bytearray) -> None:
        self.memory[0x8000:0x8000 + len(program)] = program
        self.memory_write_uint16(uint16(0xFFFC), uint16(0x8000))

    def load_and_run(self, program: bytearray, reset: bool = True) -> None:
        self.load_program(program)
        if reset: self.reset()
        self.run()

    def run(self) -> None:
        opcodes = OPCODES_MAP

        while True:
            instruction = self.memory_read(self.program_counter)
            self.program_counter += 1
            program_counter_state = self.program_counter

            opcode: Opcode = opcodes.get(instruction, None)
            if opcode is None:
                logger.error(f"Unknown opcode {instruction:x}")
                break

            match instruction:
                case 0xA9 | 0xA5 | 0xB5 | 0xAD | 0xBD | 0xB9 | 0xA1 | 0xB1:
                    self.lda(opcode.mode)
                case 0x85 | 0x95 | 0x8D | 0x9D | 0x99 | 0x81 | 0x91:
                    self.sta(opcode.mode)
                case 0xAA:
                    self.tax()
                case 0xE8:
                    self.inx()
                case 0x00:
                    break
                case _:
                    pass

            if program_counter_state == self.program_counter:
                self.program_counter += opcode.len - 1

    @historical
    def lda(self, mode: AddressingMode) -> None:
        """
        Loads a byte of memory into the accumulator setting the zero and negative flags as appropriate.
        Args:
            mode: The addressing mode

        Returns:
            None: This function does not return anything.
        """
        addr = self.get_operand_address(mode)
        value = self.memory_read(addr)

        self.register_a = value
        self.update_zero_and_negative_flags(self.register_a)

    @historical
    def ldx(self, value: uint8) -> None:
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
    def ldy(self, value: uint8) -> None:
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

    @historical
    def sta(self, mode: AddressingMode) -> None:
        """
        Stores the accumulator to memory.
        Args:
            mode: The addressing mode

        Returns:
            None: This function does not return anything.
        """
        addr = self.get_operand_address(mode)
        self.memory_write(addr, self.register_a)

    def update_zero_and_negative_flags(self, result: uint8):
        if result == 0:
            self.status |= 0b0000_0010
        else:
            self.status &= 0b1111_1101

        if result & 0b1000_0000 != 0:
            self.status |= 0b1000_0000
        else:
            self.status &= 0b0111_1111
