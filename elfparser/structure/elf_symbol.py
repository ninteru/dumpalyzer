import struct

class ElfSymbol(dict):
    """ELF Symbol object"""

    # symbol structure byte encoding
    ELF_SYMBOL = {
        "name":     'I',    # index into the object file's symbol string table
        "value":    'I',    # value of the associated symbol. may be an absolute value, an address, and so on
        "size":     'I',    # this member holds 0 if the symbol ha no size or an unknown size
        "info":     'B',    # specifies the symbol's type and binding attributes
        "other":    'B',    # holds 0 and has no defined meaning
        "shndx":    'H'     # every symbol table entry is "defined" in relation to some other section; this member holds the relevant section header table index
    }

    # symbol info binding attribute values
    STB_LOCAL   = 0     # local symbols are not visible outside the object file
    STB_GLOBAL  = 1     # global symbosl are visible to all object files being combined
    STB_WEAK    = 2     # weak symbols resemble global symbols, but their definitions have lower precedence
    STB_LOPROC  = 13    # reserved for processor-specific semantics
    STB_HIPROC  = 15

    # symbol info type attribute values
    STT_NOTYPE  = 0     # the symbol's type is not specified
    STT_OBJECT  = 1     # the symbol is associated with a data object, such as a variable, an array, and so on
    STT_FUNC    = 2     # the symbol is associated with a function or other executable code
    STT_SECTION = 3     # the symbol is associated with a section. (primarily for relocation)
    STT_FILE    = 4     # a file symbol has STB_LOCAL binding, its section index is SHN_ABS, and it precedes the other STB_LOCAL symbols for the file, if it is present
    STT_LOPROC  = 13    # reserved for processor-specific semantics
    STT_HIPROC  = 15

    # 
    SHN_ABS     = 0     # has an absolute value that will not change because of relocation
    SHN_COMMON  = 0     # labels a common block which has not yet been allocated. the symbol's value gives alignment constraints
    SHN_UNDEF   = 0     # undefined


    def __init__(self, buffer):

        self._symbol = self.parse(buffer)

        self.validate()

        super(ElfSymbol, self).__init__(self._symbol)


    def parse(self, buffer):
        """given a buffer of Elf32_Sym size parse into a symbol object"""
    
        # parse buffer as symbol struct
        elf_symbol_t = struct.Struct(" ".join(member for member in self.ELF_SYMBOL.values()))
        
        elf_symbol_keys = list(self.ELF_SYMBOL.keys())
        elf_symbol_values = elf_symbol_t.unpack(buffer)

        # create dict() of symbol struct members and their parsed values
        elf_symbol = dict( zip( elf_symbol_keys, elf_symbol_values) )

        # prepend name string dictionary entry for future population
        symbol = dict({"name_str":''})
        symbol.update(elf_symbol)
        
        return symbol


    def validate(self):
        pass


    def set_name(self, name):
        """set string representation name of the symbol. typically found in the string table"""
        
        self["name_str"] = name


    def get_info(self):
        """interpret symbol's type and binding attributes"""

        bind = self["info"] >> 4
        type = self["info"] & 0x0F

        info = dict({
            "bind": bind,
            "type": type
        })

        return info
