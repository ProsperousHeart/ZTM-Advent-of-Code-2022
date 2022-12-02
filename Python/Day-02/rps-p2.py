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
        """
        This class function creates a list of tuples based on
        the text in the file provided. No error checking.
        Returns a list of tuples.
        """
        tup_list = []
        try:
            with open(self.file_str, 'r') as file:
                for line in file:
                    tup_list.append(tuple(line.split()))
        except IOError as err:
            print(f"File does not exist:\t{self.file_str}")
        return tup_list

    def calc_points(self):
        """
        Calculates points based on a list of tuples.
        """

        def get_match_choice_pts(item):
            """
            Takes in a string, returns point for choice.
            """
            choice_dict = {
                "X": 1,
                "Y": 2,
                "Z": 3
            }
            return choice_dict[item.upper()]

        def check_win(item):
            """
            Takes a tuple and determines who was winner (or tie).
            Returns point(s) for the round.
            """

            choices = {
                "X": "A",
                "Y": "B",
                "Z": "C"
            }
            opponent = item[0].upper()
            my_choice = choices[item[1].upper()]

            if opponent == my_choice:
                return 3;
            elif (opponent == "A" and my_choice == "C") or (opponent == "B" and my_choice == "A") or (opponent == "C" and my_choice == "B"):
                return 0
            else:
                return 6

        total = 0
        for pair in self.choices:
            choice_pt = get_match_choice_pts(pair[1])
            # print(f"choice points:\t{choice_pt}")
            match_pt = check_win(pair)
            # print(f"Match Point:\t{match_pt}")
            # print(f"Total:\t{choice_pt + match_pt}")
            total += choice_pt + match_pt
        return total


# This section will allow python file to be run from command line
if __name__ == "__main__":
    findings = RPS(input_file)
    print(findings.choices)
    print(findings.points)
