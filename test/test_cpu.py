import unittest
from src.cpu import CPU
from src.utils import to_c_array_uint8


class TestCPU(unittest.TestCase):
    def test_0xa9_lda_immediate_load_data(self):
        cpu = CPU()
        cpu.interpret(to_c_array_uint8([0xA9, 0x05, 0x00]))
        self.assertEqual(cpu.register_a.value, 0x05)
        self.assertEqual(cpu.status.value & 0b0000_0010, 0b00)
        self.assertEqual(cpu.status.value & 0b1000_0000, 0)

    def test_0xa9_lda_zero_flag(self):
        cpu = CPU()
        cpu.interpret(to_c_array_uint8([0xA9, 0x00, 0x00]))
        self.assertEqual(cpu.status.value & 0b0000_0010, 0b10)

    def test_0xaa_tax_move_a_to_x(self):
        cpu = CPU()
        cpu.register_a.value = 10
        cpu.interpret(to_c_array_uint8([0xAA, 0x00]))
        self.assertEqual(cpu.register_x.value, 10)