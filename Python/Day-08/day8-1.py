import pandas as pd

# https://docs.python.org/3/library/pprint.html
import pprint
pp = pprint.PrettyPrinter(indent=4)

file_in = "Files/test.txt"
# file_in = "Files/input.txt"

# Requiorements:
# 1. count # of trees visible from outside the grid when looking directly at a row or column
# 2. look at rows and columns in a line
# 3. each number in a row represent's a single tree's height (0-9)
# 4. tree is seen if all other trees between it and an edge of the grid are shorter than it
# 5. only consider trees in same row or col (only look up, down, left, or right from any tree)
# 6. all trees on the edge are visible (meaning 1st / last row/col)

class Parser:
    """Parser class."""

    def __init__(self, file: str):
        self.file_str = file
        self.df = self.read_inv(self.file_str)
        self.out_cnt = self.cnt_out()
        self.mid = self.get_mid()
        self.top = self.top_view()
        self.left = self.lft_cnt()
        self.right = self.rt_cnt()


    def read_inv(self, f_str: str):
        """
        TBD
        """
        tmp_lst = []
        try:
            with open(self.file_str, 'r') as file:
                for line in file:
                    line = list(line.strip())
                    tmp_lst.append(line)

        except IOError as err:
            print(f"File does not exist:\t{self.file_str}")
            return
        else:
            # pp.pprint(tmp_lst)
            df = pd.DataFrame(tmp_lst)
            del tmp_lst
            return df


    def cnt_out(self):
        shape = self.df.shape
        # print(f"rows: {shape[0]}\tcols: {shape[1]}")
        border = 2 * shape[1]           # top and bottom rows
        border += (2 * shape[0]) - 4    # 1st and last column minus corners
        return border


    def get_mid(self) -> pd.DataFrame:
        """
        updates column names and returns new DataFrame
        """

        df = self.df
        tmp = df.iloc[1:-1]
        # print(tmp)
        tmp = tmp.iloc[:, 1:-1]
        # print(tmp)
        return tmp

    def cnt_itms(self, itm_lst: list) -> list:
        if len(itm_lst) > 0:
            print("... attmepting to count items ...")
            pp.pprint(itm_lst)
            tmp_list = []
            far = None
            cnt = 0
            chk_bool = False
            for line in itm_lst:
                far = line[0]
                next_h = far
                for tree in line[1:]:
                    ## if not all(itm >= item[0] for itm in line):
                    ##     tmp_list.append((item[0], line))
                    #if not any(far < itm for itm in line[1:]):
                    #    print("found something taller than outside")
                    #    tmp_list.append((line[1], line))
                    if tree > next_h:
                        cnt += 1
                        next_h = tree
                        chk_bool = True
                tmp_list.append((cnt, line))
            return tmp_list

        else:
            return []

    def top_view(self):
        # mid_DF = self.mid
        # pp.pprint(mid_DF)
        print("iterating through columns")
        # col_list = [list(mid_DF[col]) for col in mid_DF]
        col_list = [list(self.df[col]) for col in self.df]
        pp.pprint(col_list)

        tmp_list = []
        for col in col_list:
            if col[1] > col[0]:
                if not all(item >= col[1] for item in col[1:]):
                    tmp_list.append((col[1], col))
        print(tmp_list)
        return len(tmp_list)

    def lft_cnt(self):
        print("view from left...")
        # row_list = [list(row) for idx, row in mid_DF.iterrows()]
        row_list = [list(row) for idx, row in self.df.iloc[1:-1].iterrows()]
        # print(row_list)
        row_list = self.cnt_itms(row_list)
        pp.pprint(row_list)
        # return len(row_list)
        cnt = sum([item[0] for item in row_list])
        return cnt

    def rt_cnt(self):
        print("view from right...")
        row_list = [list(row)[::-1] for idx, row in self.df.iloc[1:-1].iterrows()]
        print(row_list)
        row_list = self.cnt_itms(row_list)
        print("rt_cnt row list:")
        pp.pprint(row_list)
        return len(row_list)


# This section will allow python file to be run from command line
if __name__ == "__main__":
    tmp = Parser(file_in)
    pp.pprint(tmp.df)
    out_cnt = tmp.out_cnt
    print(out_cnt)
    inner_DF = tmp.mid
    top_cnt = tmp.top
    # print(tmp.lft_cnt())
    lft_cnt = tmp.left
    rt_cnt = tmp.right

    print("out count:", tmp.out_cnt)
    print("top count:", top_cnt)
    print("left count:", lft_cnt)
    print("right count:", rt_cnt)
