import struct

class ElfHeader:

    ELF_IDENTITY = {
        "magic":        '4s',
        "class":        'B',
        "data":         'B',
        "version":      'B',
        "padding":      '9s',
    }

    ELF_HEADER = {
        "type":         'H',
        "machine":      'H',
        "version":      'I',
        "entry":        'I',
        "phoff":        'I',
        "shoff":        'I',
        "flags":        'I',
        "ehsize":       'H',
        "phentsize":    'H',
        "phnum":        'H',
        "shentsize":    'H',
        "shnum":        'H',
        "shstrndx":     'H',
    }

    def __init__(self, data):
        self._header = self.parse(data)

    def __getitem__(self, key):
        return self._header[key]

    def parse(self, data):

        elf_identity_t = struct.Struct(" ".join(member for member in self.ELF_IDENTITY.values()))
        elf_identity_keys = list(self.ELF_IDENTITY.keys())
        elf_identity_values = elf_identity_t.unpack(data[:16])

        elf_identity = dict( zip( elf_identity_keys, elf_identity_values) )

        elf_header_t = struct.Struct(" ".join(member for member in self.ELF_HEADER.values()))
        elf_header_keys = list(self.ELF_HEADER.keys())
        elf_header_values = elf_header_t.unpack(data[16:52])

        elf_header = dict( zip( elf_header_keys, elf_header_values) )

        elf_header["ident"] = elf_identity

        return elf_header



with open("elfparser\elf_test.axf", "rb") as f:
    elf_buffer = f.read()

elf_header = ElfHeader(elf_buffer)

print(elf_header._header)
print(elf_header["iden"])