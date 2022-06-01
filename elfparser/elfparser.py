from .structure.elf_header import ElfHeader

from .structure.elf_program_header import ElfProgramHeader
from .structure.elf_section_header import ElfSectionHeader

from .structure.elf_string import ElfString
from .structure.elf_symbol import ElfSymbol

from pprint import pprint

class ElfParser(dict):

    def __init__(self, buffer):

        self.__buffer = buffer

        super(ElfParser, self).__init__()

        self.__parse_header()
        self.__parse_section_header_table()
        self.__parse_program_header_table()
        self.__parse_symbol_table()
        
    def __parse_header(self):
        """create elf header from first 52 bytes of the buffer"""

        self["header"] = ElfHeader(self.__buffer[:52])
        
    def __parse_section_header_table(self):
        """create section header table from buffer"""

        e_shoff     = self["header"]["shoff"]
        e_shentsize = self["header"]["shentsize"]
        e_shnum     = self["header"]["shnum"]

        e_shend     = e_shoff + (e_shentsize * e_shnum)

        self["sh_table"] = [ElfSectionHeader(self.__buffer[i:i+e_shentsize]) for i in range(e_shoff, e_shend, e_shentsize)]

        self.__parse_section_string_table()

    def __parse_program_header_table(self):
        """create program header table from buffer"""

        e_phoff     = self["header"]["phoff"]
        e_phentsize = self["header"]["phentsize"]
        e_phnum     = self["header"]["phnum"]

        e_phend     = e_phoff + (e_phentsize * e_phnum)

        self["ph_table"] = [ElfProgramHeader(self.__buffer[i:i+e_phentsize]) for i in range(e_phoff, e_phend, e_phentsize)]

    def __parse_symbol_table(self):
        """create symbol table from buffer"""

        # symbol table is identified by section header type (2)
        symtab_sh           = next(header for header in self["sh_table"] if header["type"] == 2)
        symtab_sh_offset    = symtab_sh["offset"]
        symtab_sh_size      = symtab_sh["size"]
        symtab_sh_entsize   = symtab_sh["entsize"]
        symtab_sh_end       = symtab_sh_offset + symtab_sh_size

        self["symtab"] = [ElfSymbol(self.__buffer[i:i+symtab_sh_entsize]) for i in range(symtab_sh_offset, symtab_sh_end, symtab_sh_entsize)]

        self.__parse_symbol_string_table(symtab_sh["link"])

    def __parse_section_string_table(self):

        e_shstrndx = self["header"]["shstrndx"]

        shstrtab = self["sh_table"][e_shstrndx]

        shstrtab_offset = shstrtab["offset"]
        shstrtab_size   = shstrtab["size"]

        shstrtab_end    = shstrtab_offset + shstrtab_size

        sh_strings = ElfString(self.__buffer[shstrtab_offset:shstrtab_end])

        for section in self["sh_table"]:
            section.set_name(sh_strings.get_string(section["name"]))

    def __parse_symbol_string_table(self, link):

        symtab_strtab_sh = self["sh_table"][link]
        symtab_strtab_sh_offset = symtab_strtab_sh["offset"]
        symtab_strtab_sh_size   = symtab_strtab_sh["size"]

        symtab_strings = ElfString(self.__buffer[symtab_strtab_sh_offset:symtab_strtab_sh_offset+symtab_strtab_sh_size])

        for symbol in self["symtab"]:
            symbol.set_name(symtab_strings.get_string(symbol["name"]))

