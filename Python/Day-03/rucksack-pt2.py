# file_in = "Files/test.txt"
file_in = "Files/input-pt1.txt"

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
        Reads in a TXT file. Every 3 lines it groups together.
        Returns a list of tuples.
        """

        groups = []
        try:
            with open(self.file_str, 'r') as file:
                trio = 0
                group = []
                for line in file:
                    trio+=1
                    line = line.strip()
                    group.append(line)
                    print(f"GRP: {group}")
                    if trio == 3:
                        trio = 0
                        groups.append(tuple(group))
                        group = []
                        print(f"GRPs: {groups}")
        except IOError as err:
            print(f"File does not exist:\t{self.file_str}")
        return groups

    def find_match(self):
        """
        Takes obj's list of tuples and finds the common character between each.

        Returns a list of characters.
        """

        match_list = []
        for tup in self.rucks:
            match_list.append([item for item in set(tup[0]) if (item in set(tup[1]) and item in set(tup[2]))][0])
        print(f"Matches:\t{match_list}")
        return match_list

    def convert2num(self):
        """
        Converts each section's characters to numbers, adds them up,
        and returns the sum or priorities.
        """

        low_char = 'abcdefghijklmnopqrstuvwxyz'
        pri_list = []
        for char in self.matches:
            priority = 0
            if char.isupper():
                priority+=26
            priority+=1+low_char.index(str(char.lower()))
            pri_list.append(priority)
        return sum(pri_list)

# This section will allow python file to be run from command line
if __name__ == "__main__":
    cntr = Parser(file_in)
    print(cntr.rucks)
    print(cntr.matches)
    print(cntr.add_Ms)
