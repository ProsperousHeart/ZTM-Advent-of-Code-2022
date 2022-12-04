# file_in = "Files/test.txt"
file_in = "Files/input.txt"

class Parser:
    """Parser class."""

    def __init__(self, file: str):
        """
        Instantiation of class requires the string location for data.
        """

        self.file_str = file
        self.elves = self.read_inv(self.file_str)        # list of tuples
        self.full_strs = self.convert2num(self.elves)
        self.matches = self.convert_str(self.full_strs)    # list of characters that match
        self.cnt = self.count(self.matches)  # self.convert2num()    # number
        # self.count2 = self.count(self.pt2())
        self.cnt2 = self.count(self.pt2(self.full_strs))

    def read_inv(self, f_str: str):
        """
        Reads in a TXT file. Every 3 lines it groups together.
        Returns a list of tuples.
        """

        rtn_list = []
        try:
            with open(f_str, 'r') as file:
                for line in file:
                    line = line.strip()
                    elf1, elf2 = line.split(',')
                    # print(elf1, elf2)
                    rtn_list.append((elf1, elf2))
        except IOError as err:
            print(f"File does not exist:\t{f_str}")
        return rtn_list

    def convert2num(self, elves: list):  # (2-4,6-8)
        """
        Creates a list of tuples, where:
        1. element 1    elf1's number line
        2. element 2    elf2's number line
        """
        tup2rtn = []
        #print(self.elves)
        for pair in elves:
            temp_lst = []
            #print("convert2num pair:\t", pair)
            for item in pair:
                #print('convert2num', item)
                start, end = item.split('-')

                temp_lst.append([num for num in range(int(start), int(end) + 1)])
                # print(temp_lst[-1])
            tup2rtn.append(tuple(temp_lst))

        return tuple(tup2rtn)

    def convert_str(self, full_nums: list):
        """
        Takes in list of tuples. returns list of booleans where
        true if one item of a pair is found within another.
        """

        #print("============convertstr===================")
        orig_list = full_nums
        # print(orig_list)
        list2rtn = []
        for item in orig_list: # will be a 2 element tuple
            elf1, elf2 = item
            # print(elf1, elf2)
            # if (elf1 in elf2) or (elf2 in elf1):
            test1 = all(itm in elf1 for itm in elf2)
            test2 = all(itm in elf2 for itm in elf1)
            if test1 or test2:
                #print(True)
                list2rtn.append(True)
            else:
                #print(False)
                list2rtn.append(False)
        #print(list2rtn)
        return list2rtn

    def count(self, list2chk):
        """
        Takes in a list of booleans. Returns count of True.
        """

        return sum(list2chk)

    def pt2(self, full_strs):
        """
        Takes in list of tuples. returns list of booleans where
        true if any item of a pair is found within another.
        """
        tmp_lst = full_strs
        # print(tmp_lst)
        list2rtn = []
        for item in tmp_lst:  # tuple
            if set(item[0]).intersection(item[1]):
                list2rtn.append(True)
            else:
                list2rtn.append(False)
        return list2rtn

# This section will allow python file to be run from command line
if __name__ == "__main__":
    cntr = Parser(file_in)
    # print(cntr.matches)
    print('# where 1 is in another:\t\t', cntr.cnt)
    print('and item of one list is in the other:\t', cntr.cnt2)
