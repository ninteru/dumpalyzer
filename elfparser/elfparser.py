from structure.elf_header import ElfHeader
from structure.elf_program_header import ElfProgramHeader
from structure.elf_section_header import ElfSectionHeader
from structure.elf_string import ElfString
from structure.elf_symbol import ElfSymbol

from pprint import pprint

class ElfParser(dict):

    def __init__(self, elf_buffer):

        self._buffer = elf_buffer

        elf_header = ElfHeader(elf_buffer[:52])
        
        e_shoff     = elf_header["shoff"]
        e_shentsize = elf_header["shentsize"]
        e_shnum     = elf_header["shnum"]
        e_shend     = e_shoff + ( e_shentsize * e_shnum )

        sh_table_buffers = [elf_buffer[i:i+e_shentsize] for i in range(e_shoff, e_shend, e_shentsize)]

        elf_sh_table = [ElfSectionHeader(sh_buffer) for sh_buffer in sh_table_buffers]

        e_phoff     = elf_header["phoff"]
        e_phentsize = elf_header["phentsize"]
        e_phnum     = elf_header["phnum"]
        e_phend     = e_phoff + ( e_phentsize * e_phnum )

        ph_table_buffers = [elf_buffer[i:i+e_phentsize] for i in range(e_phoff, e_phend, e_phentsize)]

        elf_ph_table = [ElfProgramHeader(ph_buffer) for ph_buffer in ph_table_buffers]

        e_shstrndx              = elf_header["shstrndx"]
        string_table_sh         = elf_sh_table[e_shstrndx]
        string_table_sh_offset  = string_table_sh["offset"]
        string_table_sh_size    = string_table_sh["size"]

        elf_sh_string_table = ElfString(elf_buffer[string_table_sh_offset:string_table_sh_offset+string_table_sh_size])

        for sh in elf_sh_table:
            name = elf_sh_string_table.get_string(sh["name"])
            sh.set_name(name)

        symbol_table_sh = next(header for header in elf_sh_table if header["type"] == 2)
        symbol_table_sh_offset  = symbol_table_sh["offset"]
        symbol_table_sh_size    = symbol_table_sh["size"]
        symbol_table_sh_entsize = symbol_table_sh["entsize"]
        symbol_table_sh_end     = symbol_table_sh_offset + symbol_table_sh_size

        elf_symbol_table = [ElfSymbol(elf_buffer[i:i+symbol_table_sh_entsize]) for i in range(symbol_table_sh_offset, symbol_table_sh_end, symbol_table_sh_entsize)]

        symbol_table_string_table_sh = elf_sh_table[symbol_table_sh["link"]]
        symbol_table_string_table_sh_offset = symbol_table_string_table_sh["offset"]
        symbol_table_string_table_sh_size   = symbol_table_string_table_sh["size"]

        elf_symbol_string_table = ElfString(elf_buffer[symbol_table_string_table_sh_offset:symbol_table_string_table_sh_offset+symbol_table_string_table_sh_size])

        for symbol in elf_symbol_table:
            name = elf_symbol_string_table.get_string(symbol["name"])
            symbol.set_name(name)

        elf = dict()
        elf["header"] = elf_header
        elf["sh_table"] = elf_sh_table
        elf["ph_table"] = elf_ph_table
        elf["symbols"] = elf_symbol_table

        super(ElfParser, self).__init__(elf)

with open("elfparser\elf_test.axf", "rb") as f:
    elf_buffer = f.read()

elf = ElfParser(elf_buffer)

pprint(elf, sort_dicts=False)