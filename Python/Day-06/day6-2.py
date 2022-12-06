# file_in = "Files/test.txt"
# file_in = "Files/test2.txt"
file_in = "Files/input.txt"

class Parser:
    """Parser class."""

    def __init__(self, file: str):
        self.file_str = file
        self.lines = self.read_inv()
        self.sopms = self.get_loc(4)
        self.somms = self.get_loc(14)

    def read_inv(self, ):
        """
        TBD
        """

        try:
            with open(self.file_str, 'r') as file:
                return [line for line in file]
        except IOError as err:
            print(f"File does not exist:\t{self.file_str}")
            return

    def get_loc(self, num_chars: int = 4):
        """
        Goes through each line in test file and searches for the first substring of 4 consecutive unique characters.
        """

        idx_list = []
        print("num_chars:", num_chars)
        for itm_str in self.lines:
            tmp_str = ''
            idx = 0
            for char_str in itm_str:
                if len(set(tmp_str)) == num_chars:
                    print(f"unique {num_chars}:",
                          tmp_str, idx)
                    tmp_str = ''
                    idx_list.append(idx)
                    idx = 0
                    break
                elif len(tmp_str) == num_chars:
                    tmp_str = tmp_str[-(num_chars-1):idx]
                tmp_str += char_str
                idx += 1
        # print(idx_list)
        return idx_list


# This section will allow python file to be run from command line
if __name__ == "__main__":
    prsr = Parser(file_in)
    # print(prsr.lines)
    print(prsr.sopms)
    print(prsr.somms)
