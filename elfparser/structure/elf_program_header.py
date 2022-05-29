import struct


class ElfProgramHeader:

    ELF_PROGRAM_HEADER = {
        "type":         'I',
        "offset":       'I',
        "vaddr":        'I',
        "paddr":        'I',
        "filesz":       'I',
        "memsz":        'I',
        "flags":        'I',
        "align":        'I'
    }

    # PH_TYPE = [
    #     "unused",
    #     "loadable segment",
    #     "dynamic linking info",
    #     "interpreter",
    #     "auxiliary info",
    #     "reserved",
    #     "program header table"
    # ]


    def __init__(self, data):

        self._program_header = self.parse(data)

        self.validate()

        super(ElfProgramHeader, self).__init__(self._program_header)

    def parse(self, data):

        elf_program_header_t = struct.Struct(" ".join(member for member in self.ELF_PROGRAM_HEADER.values()))
        elf_program_header_keys = list(self.ELF_PROGRAM_HEADER.keys())
        elf_program_header_values = elf_program_header_t.unpack(data)

        elf_program_header = dict( zip( elf_program_header_keys, elf_program_header_values) )

        return elf_program_header

    def validate(self):
        pass
    