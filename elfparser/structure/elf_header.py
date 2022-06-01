import struct

class ElfHeader(dict):
    """ELF Header object"""

    # elf header data structure by type
    ELF_HEADER_T = {
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

    # elf type
    E_TYPE = {
        0:              "ET_NONE",
        1:              "ET_REL",
        2:              "ET_EXEC",
        3:              "ET_DYN",
        4:              "ET_CORE",
        0xFF00:         "ET_LOPROC",
        0xFFFF:         "ET_HIPROC"
    }

    # elf machine type
    E_MACHINE = {
        0:              "ET_NONE",
        1:              "EM_M32",
        2:              "EM_SPARC",
        3:              "EM_386",
        4:              "EM_68K",
        5:              "EM_88K",
        7:              "EM_860",
        8:              "EM_MIPS",
        10:             "EM_MIPS_RS4_BE",
        40:             "EM_ARM"
    }

    # elf version type
    E_VERSION = {
        0:              "EV_NONE",
        1:              "EV_CURRENT"
    }

    # elf identity data structure by type
    ELF_IDENTITY_T = {
        "magic":        '4s',
        "class":        'B',
        "data":         'B',
        "version":      'B',
        "padding":      '9s',
    }

    # elf identity magic constant
    EI_MAGIC = b'\x7fELF'

    # elf identity class type
    EI_CLASS = {
        0:              "ELFCLASSNONE",
        1:              "ELFCLASS32",
        2:              "ELFCLASS64"
    }

    # elf identity data type
    EI_DATA = {
        0:              "ELFDATANONE",
        1:              "ELFDATA2LSB",
        2:              "ELFDATA2MSB"
    }

    # elf identity version type
    EI_VERSION = E_VERSION

    
    def __init__(self, data):

        super(ElfHeader, self).__init__()
        
        self.__parse(data)

        self.__validate()
        
    def __parse(self, data):
        """parse binary array as elf header structure"""

        # create elf identidity dictionary
        elf_identity_t = struct.Struct(" ".join(member for member in self.ELF_IDENTITY_T.values()))
        elf_identity_keys = list(self.ELF_IDENTITY_T.keys())
        elf_identity_values = elf_identity_t.unpack(data[:16])

        elf_identity = dict( zip( elf_identity_keys, elf_identity_values) )

        # create elf header dictionary
        elf_header_t = struct.Struct(" ".join(member for member in self.ELF_HEADER_T.values()))
        elf_header_keys = list(self.ELF_HEADER_T.keys())
        elf_header_values = elf_header_t.unpack(data[16:52])

        elf_header = dict( zip( elf_header_keys, elf_header_values) )

        # combine elf identity and elf header
        header = dict({"ident":elf_identity})
        header.update(elf_header)

        # set object's data
        self.update(header)

    def __validate(self):
        """validate elf header is correct magic, version, and machine type"""

        # check identity magic
        if self["ident"]["magic"] != b'\x7fELF':
            raise ValueError

        # check machine is ARM
        if self["machine"] != 40:
            raise ValueError

        # check class
        if self["ident"]["class"] != 1:
            raise ValueError

        # check version
        if self["ident"]["version"] != 1:
            raise ValueError


