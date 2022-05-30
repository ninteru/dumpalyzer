import struct

class ElfHeader(dict):

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

    EM_ARM = 40

    ELF_CLASS_NONE  = 0
    ELF_CLASS_32    = 1
    ELF_CLASS_64    = 2

    def __init__(self, data):

        self._header = self.parse(data)

        self.validate()
        
        super(ElfHeader, self).__init__(self._header)

    def parse(self, data):

        elf_identity_t = struct.Struct(" ".join(member for member in self.ELF_IDENTITY.values()))
        elf_identity_keys = list(self.ELF_IDENTITY.keys())
        elf_identity_values = elf_identity_t.unpack(data[:16])

        elf_identity = dict( zip( elf_identity_keys, elf_identity_values) )

        elf_header_t = struct.Struct(" ".join(member for member in self.ELF_HEADER.values()))
        elf_header_keys = list(self.ELF_HEADER.keys())
        elf_header_values = elf_header_t.unpack(data[16:52])

        elf_header = dict( zip( elf_header_keys, elf_header_values) )

        header = dict({"ident":elf_identity})
        header.update(elf_header)

        return header

    def validate(self):

        # check identity magic
        print(self._header["ident"])
        if self._header["ident"]["magic"] != b'\x7fELF':
            raise ValueError

        # check machine is ARM
        if self._header["machine"] != 40:
            raise ValueError

        # check class
        if self._header["ident"]["class"] != self.ELF_CLASS_32:
            raise ValueError
