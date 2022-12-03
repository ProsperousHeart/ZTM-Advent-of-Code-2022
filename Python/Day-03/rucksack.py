file_in = "Files/test.txt"
# file_in = "Files/input.txt"

class Parser:
    """Parser class."""

    def __init__(self, file: str):
        """
        Instantiation of class requires the string location for data.
        This creates 4 attributes:
            1. file_str STR     holds info about the file to read
        """

        self.file_str = file
        self.rucks = self.read_inv()

    def read_inv(self):
        """
        Reads in a TXT file. For each line, it:
        1. splits in half
        2. returns a list of tuples
        """

        tup_list = []
        try:
            with open(self.file_str, 'r') as file:
                for line in file:
                    line = line.strip()
                    mid = len(line) // 2
                    print(mid)
                    pt1 = line[:mid]
                    pt2 = line[mid:]
                    tup_list.append((pt1, pt2))
        except IOError as err:
            print(f"File does not exist:\t{self.file_str}")
        return tup_list

    def find_match(self):
        """
        Takes obj's list of tuples and finds the common character between each.

        Returns a list of characters.
        """

        pass

    def convert2num(self):
        """
        Converts each section's characters to numbers, adds them up, and returns the ...
        """

        pass

# This section will allow python file to be run from command line
if __name__ == "__main__":
    cntr = Parser(file_in)
    print(cntr.rucks)
