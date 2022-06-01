import sys

sys.path[0:0] = ['.']

from pprint import pprint as pp
from elfparser.elfparser import ElfParser

if __name__ == '__main__':

    with open("test\elf_test.axf", "rb") as f:
        buffer = f.read()

    elf = ElfParser(buffer)

    pp(elf, sort_dicts=False)