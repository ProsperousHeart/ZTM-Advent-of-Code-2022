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
        self.rucks = self.read_inv()        # list of tuples
        self.matches = self.find_match()    # list of characters that match
        self.add_Ms = self.convert2num()    # number

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
                    # print(mid)
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

        match_list = []
        for tup in self.rucks:
            print(f"Sets |\t{set(tup[0])} - {set(tup[1])}")
            match_list.append([item for item in set(tup[0]) if item in set(tup[1])][0])
        print(f"Matches:\t{match_list}")
        return match_list

    def convert2num(self):
        """
        Converts each section's characters to numbers, adds them up,
        and returns the sum or priorities.
        """

        pass

# This section will allow python file to be run from command line
if __name__ == "__main__":
    cntr = Parser(file_in)
    # print(cntr.rucks)
