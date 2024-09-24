class C64Emulator:
    def __init__(self):
        # Initialize C64 memory (64KB)
        self.memory = [0] * 65536

        # 6510 CPU registers
        self.pc = 0x0000  # Program Counter
        self.sp = 0xFF    # Stack Pointer
        self.a = 0x00     # Accumulator
        self.x = 0x00     # X register
        self.y = 0x00     # Y register
        self.status = 0x00  # Status Register

        # Flags
        self.carry = False
        self.zero = False
        self.interrupt_disable = False
        self.decimal_mode = False
        self.break_command = False
        self.overflow = False
        self.negative = False

    def reset(self):
        # Reset the CPU to default state
        self.pc = self.read_word(0xFFFC)  # Read reset vector
        self.sp = 0xFF
        self.a = self.x = self.y = 0x00
        self.status = 0x00
        print(f"C64 Emulator Reset: PC set to {self.pc:04X}")

    def read_word(self, address):
        # Read two bytes from memory and combine them into a word
        lo = self.memory[address]
        hi = self.memory[address + 1]
        return (hi << 8) | lo

    def load_program(self, program, start_address):
        # Load a program into memory starting at the given address
        for i, byte in enumerate(program):
            self.memory[start_address + i] = byte

    def execute(self):
        # A simple method to emulate execution of instructions
        while True:
            opcode = self.memory[self.pc]
            if opcode == 0xA9:  # LDA immediate
                self.a = self.memory[self.pc + 1]
                self.pc += 2
                self.set_flags(self.a)
            elif opcode == 0x00:  # BRK
                print("Break command encountered. Halting execution.")
                break
            else:
                print(f"Unknown opcode {opcode:02X} at address {self.pc:04X}")
                break

            print(f"PC: {self.pc:04X}, A: {self.a:02X}, X: {self.x:02X}, Y: {self.y:02X}")

    def set_flags(self, result):
        self.zero = (result == 0)
        self.negative = (result & 0x80 != 0)


# Example usage:
emulator = C64Emulator()

# A simple program that loads an immediate value into the accumulator (LDA #$01)
program = [
    0xA9, 0x01,  # LDA #$01
    0x00         # BRK (Break)
]

emulator.reset()
emulator.load_program(program, 0x0801)  # Load the program into memory starting at $0801
emulator.pc = 0x0801  # Set PC to start of the program
emulator.execute()
