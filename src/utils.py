import ctypes


def to_c_array_uint8(data: list) -> ctypes.Array[ctypes.c_uint8]:
    """
    Converts a list of integers to a C array of unsigned 8-bit integers.

    Args:
        data (list): The list of integers to be converted.

    Returns:
        ctypes.Array[ctypes.c_uint8]: The converted C array of unsigned 8-bit integers.
    """
    return (ctypes.c_uint8 * len(data))(*data)
