import unittest
from src.cpu import CPU
from src.types import uint16, uint8


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
        cpu.program_counter = cpu.memory_read_uint16(uint16(0xFFFC))
        cpu.run()
        self.assertEqual(cpu.register_x, 10)

    def test_5_ops_working_together(self):
        cpu = CPU()
        cpu.load_and_run(bytearray([0xA9, 0xC0, 0xAA, 0xE8, 0x00]))
        self.assertEqual(cpu.register_x, 0xC1)

    def test_inx_overflow(self):
        cpu = CPU()
        cpu.load_and_run(bytearray([0xA9, 0xFF, 0xAA, 0xE8, 0xE8, 0x00]))
        self.assertEqual(cpu.register_x, 1)

    def test_lda_from_memory(self):
        cpu = CPU()
        cpu.memory_write(uint16(0x10), uint8(0x55))
        cpu.load_and_run(bytearray([0xA5, 0x10, 0x00]))
        self.assertEqual(cpu.register_a, 0x55)
