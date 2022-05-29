from structure.elf_header import ElfHeader
from structure.elf_program_header import ElfProgramHeader
from structure.elf_section_header import ElfSectionHeader
from structure.elf_string import ElfString

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

        elf = dict()
        elf["header"] = elf_header
        elf["sh_table"] = elf_sh_table
        elf["ph_table"] = elf_ph_table

        super(ElfParser, self).__init__(elf)

with open("elfparser\elf_test.axf", "rb") as f:
    elf_buffer = f.read()

elf = ElfParser(elf_buffer)

pprint(elf, sort_dicts=False)