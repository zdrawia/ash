from enum import Enum, auto


class AddressingMode(Enum):
    Immediate      = auto()
    ZeroPage       = auto()
    ZeroPage_X     = auto()
    ZeroPage_Y     = auto()
    Absolute       = auto()
    Absolute_X     = auto()
    Absolute_Y     = auto()
    Indirect_X     = auto()
    Indirect_Y     = auto()
    NoneAddressing = auto()