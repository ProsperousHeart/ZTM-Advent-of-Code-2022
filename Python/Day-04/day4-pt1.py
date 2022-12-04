# file_in = "Files/test.txt"
file_in = "Files/input.txt"

class Parser:
    """Parser class."""

    def __init__(self, file: str):
        """
        Instantiation of class requires the string location for data.
        This creates 4 attributes:
            1. file_str STR     holds info about the file to read
        """

        self.file_str = file
        self.elves = self.read_inv()        # list of tuples
        self.full_strs = self.convert2num()
        self.matches = self.convert_str()    # list of characters that match
        self.count = self.count()  # self.convert2num()    # number

    def read_inv(self):
        """
        Reads in a TXT file. Every 3 lines it groups together.
        Returns a list of tuples.
        """

        rtn_list = []
        try:
            with open(self.file_str, 'r') as file:
                for line in file:
                    line = line.strip()
                    elf1, elf2 = line.split(',')
                    # print(elf1, elf2)
                    rtn_list.append((elf1, elf2))
        except IOError as err:
            print(f"File does not exist:\t{self.file_str}")
        return rtn_list

    def convert2num(self):  # (2-4,6-8)
        tup2rtn = []
        #print(self.elves)
        for pair in self.elves:
            temp_lst = []
            #print("convert2num pair:\t", pair)
            for item in pair:
                #print('convert2num', item)
                start, end = item.split('-')

                temp_lst.append([num for num in range(int(start), int(end) + 1)])
                # print(temp_lst[-1])
            tup2rtn.append(tuple(temp_lst))

        return tuple(tup2rtn)

    def convert_str(self):
        """
        Creates a list of tuples, where:
        1. element 1    elf1's number line
        2. element 2    elf2's number line
        """

        #print("============convertstr===================")
        orig_list = self.full_strs
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

    def count(self):
        """
        Takes obj's list of tuples and finds the common character between each.

        Returns a list of characters.
        """

        return sum(self.matches)

# This section will allow python file to be run from command line
if __name__ == "__main__":
    cntr = Parser(file_in)
    # print(cntr.matches)
    print(cntr.count)
