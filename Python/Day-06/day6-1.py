file_in = "Files/test.txt"
# file_in = "Files/input.txt"

class Parser:
    """Parser class."""

    def __init__(self, file: str):
        self.file_str = file


    def read_inv(self, f_str: str):
        """
        TBD
        """

        try:
            with open(self.file_str, 'r') as file:
                # for line in file:
                #    pass
                pass
        except IOError as err:
            print(f"File does not exist:\t{self.file_str}")
            return



# This section will allow python file to be run from command line
if __name__ == "__main__":
    Parser(file_in)
