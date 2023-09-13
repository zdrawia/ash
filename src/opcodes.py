from dataclasses import dataclass

from src.addressingmode import AddressingMode


@dataclass
class Opcode:
    code: int
    mnemonic: str
    len: int
    cycles: int
    mode: AddressingMode

CPU_OPCODES = [
    Opcode(0x00, "BRK", 1, 7, AddressingMode.NoneAddressing),
    Opcode(0xAA, "TAX", 1, 2, AddressingMode.NoneAddressing),
    Opcode(0xE8, "INX", 1, 2, AddressingMode.NoneAddressing),
    Opcode(0xA9, "LDA", 2, 2, AddressingMode.Immediate),
    Opcode(0xA5, "LDA", 2, 3, AddressingMode.ZeroPage),
    Opcode(0xB5, "LDA", 2, 4, AddressingMode.ZeroPage_X),
    Opcode(0xAD, "LDA", 3, 4, AddressingMode.Absolute),
    Opcode(0xBD, "LDA", 3, 4, AddressingMode.Absolute_X),
    Opcode(0xB9, "LDA", 3, 4, AddressingMode.Absolute_Y),
    Opcode(0xA1, "LDA", 2, 6, AddressingMode.Indirect_X),
    Opcode(0xB1, "LDA", 2, 5, AddressingMode.Indirect_Y),
    Opcode(0x85, "STA", 2, 3, AddressingMode.ZeroPage),
    Opcode(0x95, "STA", 2, 4, AddressingMode.ZeroPage_X),
    Opcode(0x8D, "STA", 3, 4, AddressingMode.Absolute),
    Opcode(0x9D, "STA", 3, 5, AddressingMode.Absolute_X),
    Opcode(0x99, "STA", 3, 5, AddressingMode.Absolute_Y),
    Opcode(0x81, "STA", 2, 6, AddressingMode.Indirect_X),
    Opcode(0x91, "STA", 2, 6, AddressingMode.Indirect_Y),
]

OPCODES_MAP = {opcode.code: opcode for opcode in CPU_OPCODES}
