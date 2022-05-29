from ctypes import sizeof
import struct

class ElfSectionHeader(dict):

    ELF_SECTION_HEADER = {
        "name":         'I',
        "type":         'I',
        "flags":        'I',
        "addr":         'I',
        "offset":       'I',
        "size":         'I',
        "link":         'I',
        "info":         'I',
        "addralign":    'I',
        "entsize":      'I',
    }

    # SH_TYPE = [
    #     "inactive",
    #     "information determined by program",
    #     "symbol table",
    #     "string table",
    #     "relocation entry w/ addends",
    #     "symbol hash table",
    #     "dynamic linking",
    #     "note",
    #     "occupies no space in file",
    #     "relocation entry",
    #     "reserved",
    #     "symbol table"
    # ]

    # SH_FLAGS = [
    #     "",
    #     "data that is writable during process execution",
    #     "occupies memory during process execution",
    #     "",
    #     "executable machine instructions"
    # ]

    def __init__(self, data):

        self._section_header = self.parse(data)

        self.validate()

        super(ElfSectionHeader, self).__init__(self._section_header)

    def parse(self, data):

        elf_section_header_t = struct.Struct(" ".join(member for member in self.ELF_SECTION_HEADER.values()))
        elf_section_header_keys = list(self.ELF_SECTION_HEADER.keys())
        elf_section_header_values = elf_section_header_t.unpack(data)

        elf_section_header = dict( zip( elf_section_header_keys, elf_section_header_values) )

        section_header = dict({"name_str":''})
        section_header.update(elf_section_header)

        return section_header

    def validate(self):
        pass

    def set_name(self, name):
        self["name_str"] = name