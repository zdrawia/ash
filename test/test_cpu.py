import unittest
from src.cpu import CPU


class TestCPU(unittest.TestCase):
    def test_0xa9_lda_immediate_load_data(self):
        cpu = CPU()
        cpu.load_and_run(bytearray([0xA9, 0x05, 0x00]))
        self.assertEqual(cpu.register_a, 0x05)
        self.assertEqual(cpu.status & 0b0000_0010, 0b00)
        self.assertEqual(cpu.status & 0b1000_0000, 0)

    def test_0xa9_lda_zero_flag(self):
        cpu = CPU()
        cpu.load_and_run(bytearray([0xA9, 0x00, 0x00]))
        self.assertEqual(cpu.status & 0b0000_0010, 0b10)

    def test_0xaa_tax_move_a_to_x(self):
        cpu = CPU()
        cpu.load_program(bytearray([0xAA, 0x00]))
        cpu.register_a = 10
        cpu.program_counter = cpu.memory_read_uint16(0xFFFC)
        cpu.run()
        self.assertEqual(cpu.register_x, 10)
