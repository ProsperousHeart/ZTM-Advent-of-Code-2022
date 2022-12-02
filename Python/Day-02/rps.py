# read the data - create pairs of choices in a list/tuple
# for each set of choices, calculate choice score & round outcome
# return total points

test_file = r"Files\Test.txt"
input_file = r"Files\StrategyGuide.txt"


class RPS:
    """This class is the Rock, Paper, Scissors point determinator."""
    def __init__(self, file: str):
        """
        Instantiation of class requires the string location for data.
        This creates 4 attributes:
            1. file_str STR     holds info about the file to read
            2. choices  list    list of tuples with choices
            3. points   INT     total number of points
        """
        self.file_str = file
        self.choices = self.read_guide()
        self.points = self.calc_points()

    def read_guide(self):
        tup_list = []
        try:
            with open(self.file_str, 'r') as file:
                for line in file:
                    tup_list.append(tuple(line.split()))
        except IOError as err:
            print(f"File does not exist:\t{self.file_str}")
        return tup_list

    def calc_points(self):
        def check_win(item):

            pass
        for pair in self.choices:
            pass


# This section will allow python file to be run from command line
if __name__ == "__main__":
    findings = RPS(test_file)
    print(findings.choices)
