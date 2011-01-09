class BrainFuck(object):
    def __init__(self, program):
        self.memory = [0] * 30000
        self.pointer = 0
        self.program = program

    def run(self, input=''):
        output = ''
        p = level = argi = 0

        while p < len(self.program):
            c = self.program[p]

            if c == '>':
                self.pointer += 1
                self.pointer %= len(self.memory)
            elif c == '<':
                self.pointer -= 1
                self.pointer %= len(self.memory)
            elif c == '+':
                self.memory[self.pointer] += 1
                self.memory[self.pointer] %= 256
            elif c == '-':
                self.memory[self.pointer] -= 1
                self.memory[self.pointer] %= 256
            elif c == '.':
                output += chr(self.memory[self.pointer])
            elif c == ',':
                try:
                    d = ord(input[argi])
                    argi += 1
                except IndexError:
                    d = -1 # EOS
                self.memory[self.pointer] = d
            elif c == '[':
                if not self.memory[self.pointer]:
                    p += 1
                    while level or self.program[p] != ']':
                        if self.program[p] == '[':
                            level += 1
                        elif self.program[p] == ']':
                            level -= 1
                        p += 1

            elif c == ']':
                p -= 1
                while level or self.program[p] != '[':
                    if self.program[p] == '[':
                        level += 1
                    elif self.program[p] == ']':
                        level -= 1
                    p -= 1
                p -= 1

            p += 1

        return output

    def compile(self, output):
        def line(data, ident):
            return '%s%s\n' % (' ' * ident * 4, data)

        id = open(output, 'wt')
        id.write('''import sys
def main():
    input = sys.argv[1] if len(sys.argv) > 1 else ''
    memory = [0] * 30000
    pointer = argi = 0
''')

        level = 1
        for c in self.program:
            if c == '>':
                id.write(line('pointer += 1', level))
                id.write(line('pointer %= 30000', level))
            elif c == '<':
                id.write(line('pointer -= 1', level))
                id.write(line('pointer %= 30000', level))
            elif c == '+':
                id.write(line('memory[pointer] += 1', level))
                id.write(line('memory[pointer] %= 256', level))
            elif c == '-':
                id.write(line('memory[pointer] -= 1', level))
                id.write(line('memory[pointer] %= 256', level))
            elif c == '.':
                id.write(line('print chr(memory[pointer])', level))
            elif c == ',':
                id.write(line('try:', level))
                id.write(line('pointer = ord(input[argi])', level + 1))
                id.write(line('argi += 1', level + 1))
                id.write(line('except IndexError:', level))
                id.write(line('pointer = -1', level + 1))
            elif c == '[':
                id.write(line('while memory[pointer]:', level))
                level += 1
            elif c == ']':
                level -=1

        id.write('''
if __name__ == '__main__':
    main()''')
        id.close()

if __name__ == '__main__':
    # Bubble sort example
    print BrainFuck('''
        >>>>>,+[>>>,+]<<<[<<<[>>
        >[-<<<-<+>[>]>>]<<<[<]>>
        [>>>+<<<-]<[>+>>>+<<<<-]
        <<]>>>[-.[-]]>>>[>>>]<<<]
    ''').compile('bublesort.py') #run('4231')
