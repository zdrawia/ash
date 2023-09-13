class uint8(int):
    def __new__(cls, *args, **kwargs):
        # Wrap int into uint8
        args = (args[0] & 0xFF,)
        return super().__new__(cls, *args, **kwargs)

    def __add__(self, other):
        return uint8(super().__add__(other))

    def __sub__(self, other):
        return uint8(super().__sub__(other))

    def __rshift__(self, other):
        return uint8(super().__rshift__(other))

    def __lshift__(self, other):
        return uint8(super().__lshift__(other))

    def __and__(self, other):
        return uint8(super().__and__(other))

    def __xor__(self, other):
        return uint8(super().__xor__(other))

    def __or__(self, other):
        return uint8(super().__or__(other))

    def __invert__(self):
        return uint8(super().__invert__())

    def __radd__(self, other):
        return uint8(super().__radd__(other))

    def __rsub__(self, other):
        return uint8(super().__rsub__(other))

    def __rlshift__(self, other):
        return uint8(super().__rlshift__(other))

    def __rrshift__(self, other):
        return uint8(super().__rrshift__(other))

    def __rand__(self, other):
        return uint8(super().__rand__(other))

    def __rxor__(self, other):
        return uint8(super().__rxor__(other))

    def __ror__(self, other):
        return uint8(super().__ror__(other))

    def __neg__(self):
        return uint8(super().__neg__())

    def increment(self):
        return uint8(super().__add__(1))

class uint16(int):
    def __new__(cls, *args, **kwargs):
        # Wrap int into uint16
        args = (args[0] & 0xFFFF,)
        return super().__new__(cls, *args, **kwargs)

    def __add__(self, other):
        return uint16(super().__add__(other))

    def __sub__(self, other):
        return uint16(super().__sub__(other))

    def __rshift__(self, other):
        return uint16(super().__rshift__(other))

    def __lshift__(self, other):
        return uint16(super().__lshift__(other))

    def __and__(self, other):
        return uint16(super().__and__(other))

    def __xor__(self, other):
        return uint16(super().__xor__(other))

    def __or__(self, other):
        return uint16(super().__or__(other))

    def __invert__(self):
        return uint16(super().__invert__())

    def __radd__(self, other):
        return uint16(super().__radd__(other))

    def __rsub__(self, other):
        return uint16(super().__rsub__(other))

    def __rlshift__(self, other):
        return uint16(super().__rlshift__(other))

    def __rrshift__(self, other):
        return uint16(super().__rrshift__(other))

    def __rand__(self, other):
        return uint16(super().__rand__(other))

    def __rxor__(self, other):
        return uint16(super().__rxor__(other))

    def __ror__(self, other):
        return uint16(super().__ror__(other))

    def __neg__(self):
        return uint16(super().__neg__())

    def increment(self):
        return uint16(super().__add__(1))