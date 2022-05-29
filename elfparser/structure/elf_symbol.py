import struct

class ElfSymbol(dict):

    ELF_SYMBOL = {
        "name":     'I',
        "value":    'I',
        "size":     'I',
        "info":     'B',
        "other":    'B',
        "shndx":    'H'
    }

    def __init__(self, buffer):
        pass

    def parse(self, buffer):
        pass

    def set_name(self, name):
        pass