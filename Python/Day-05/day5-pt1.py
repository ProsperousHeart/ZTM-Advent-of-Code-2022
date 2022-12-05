# file_in = "Files/test.txt"
# file_in = "Files/test-moves-only.txt"
# file_in = "Files/input.txt"
file_in = "Files/input-moves-only.txt"

class Parser:
    """Parser class."""

    rows_test = {
        1: list('ZN'),
        2: list('MCD'),
        3: list('P')
    }

    rows_full = {
        1: 'NDMQBPZ',
        2: 'CLZQMDHV',
        3: 'QHRDVFZG',
        4: 'HGDFN',
        5: 'NFQ',
        6: 'DQVZFBT',
        7: 'QMTZDVSH',
        8: 'MGFPNQ',
        9: 'BWRM',
    }

    def __init__(self, file: str):
        self.file_str = file
        # self.rows = self.rows_test  # not best practice
        self.rows = self.rows_full  # not best practice
        self.steps = self.read_inv(file)

        self.move()
        self.top_gun()


    def read_inv(self, f_str: str):
        """
        TBD
        """
        num_list = []
        try:
            with open(self.file_str, 'r') as file:
                for line in file:
                    parsed = line.strip().split(' ')
                    num_list.append([int(item) for item in parsed if item.isdigit()])
        except IOError as err:
            print(f"File does not exist:\t{self.file_str}")
            return
        print(num_list)
        return num_list

    def move(self, ):
        """
        Takes in a list of lists, where each element has 3 integers.
        1st: number of items to move to another row / column (in reverse)
        2nd: column/row to remove items from
        3rd: column/row to move items to
        """
        rows = self.rows
        steps = self.steps

        print("Before:\t", self.rows)
        for step in steps:
            print('=======\nbefore', rows)
            print('step', step)
            tmp_list = list(rows[step[1]])
            to_mv = tmp_list[-step[0]:]
            del tmp_list[-step[0]:]
            rows[step[1]] = tmp_list
            to_mv.reverse()
            print(f"to_mv (type: {type(to_mv)}:\t{to_mv}")

            print('to_mv:\t', to_mv)
            print("before:\t", rows[step[2]])
            rows[step[2]] += ''.join(to_mv)
            print("after:\t", rows[step[2]])
            print('after', rows)

        # print("After:\t", self.rows)

    def top_gun(self):
        """
        Returns list (in order) each column's top item or each row's last item.
        """
        str2rtn = []
        print(self.rows)
        for row, items in self.rows.items():
            str2rtn.extend(items[-1])

        print(''.join(str2rtn))



# This section will allow python file to be run from command line
if __name__ == "__main__":
    cntr = Parser(file_in)
    pass
