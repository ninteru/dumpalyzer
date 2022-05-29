

class ElfString:

    def __init__(self, buffer):
        
        self._string_table = buffer

    def get_string(self, index):
        
        string = ""

        size = len(self._string_table)

        while(index < size):
            if self._string_table[index] == 0:
                break

            string += chr(self._string_table[index])
            index += 1

        return string