# https://docs.python.org/3/library/pprint.html
import pprint

pp = pprint.PrettyPrinter(indent=4)

file_in = "../Files/test.txt"
# file_in = "Files/input.txt"

dir_struct = [
    ("/", "dir", 0)
]

class Dir_CMD:
    def __init__(self, lvl: int, itm_id: int, type: str, option: str,
                 action: str = None, size: int = 0, parent=None, child=None,
                 fname: str = None):
        """
        TYPES:
            T1  executed command
                cd, ls
            T2  output
        """
        self.id = itm_id
        self.level = lvl
        self.type = type
        self.action = action
        self.option = option
        self.size = size
        self.parent = parent
        self.child = child
        self.fname = fname

    def make_dict(self):
        return dict(id=self.id, level=self.level, type=self.type,
                    action=self.action, option=self.option, size=self.size,
                    parent=self.parent, child=self.child, fname=self.fname)

    def __repr__(self):
        return f"""Dir_CMD(
    id: {self.id}, 
    level: {self.level},
    type: {self.type}, 
    action: "{self.action}", 
    option: "{self.option}", 
    size: {self.size}, 
    parent: {self.parent}, 
    child: {self.child}, 
    fname: "{self.fname}"
)"""
    # def __repr__(self):
    #     return str(self.make_dict())

    # def __str__(self):
    #    return str(pp.pprint(self.make_dict()))
    def __str__(self):
        return f"""Dir_CMD(
    id: {self.id}, 
    level: {self.level},
    type: {self.type}, 
    action: "{self.action}", 
    option: "{self.option}", 
    size: {self.size}, 
    parent: {self.parent}, 
    child: {self.child}, 
    fname: "{self.fname}"
)"""


class Parser:
    """Parser class.

    $   commands you executed
    cd  change directory
        x - 1 level
        .. - out 1 level
        / - switches to outermost directory `/` (home)
    ls  list
        size filename
        directory name

    determine total size of each directory
    find all directories with total size <=100000
    calculate sum of their total sizes
    """

    def __init__(self, file: str):
        self.file_str = file
        self.lines = self.read_inv(self.file_str)

    def read_inv(self, f_str: str):
        """
        TBD
        """
        def get_dict_idx(parent_id: int, line_list: list):
            item = next((idx for (idx, info) in enumerate(line_list)), None)
            print('List IDX of parent:', item)
            return item

        cmd = []
        items = []
        try:
            with open(self.file_str, 'r') as file:
                loc_itm_bool = False
                prior_folder = None
                itm_id = 0
                level = 0
                for line in file:
                    splt_line = line.strip().split(' ')
                    action = None
                    option = None
                    size = 0
                    fname = None
                    if splt_line[0] == "$":
                        if len(splt_line) == 3:  # cd
                            option = splt_line[-1]
                            if option == "/":  # move into home directory
                                level = 0
                                prior_folder = 0
                            elif option == "..":  # move up 1
                                if level > 0:
                                    level-=1
                            else:  # move into particular folder
                                level+=1
                                fname = splt_line[-1]
                                type, action, option = splt_line
                                obj = Dir_CMD(level, itm_id, type, option,
                                              action, size, prior_folder,
                                              None, fname)
                                prior_idx = get_dict_idx(prior_folder, items)
                                if prior_idx:
                                    tmp = items[prior_idx]
                                    tmp.child = obj.id
                                items.append(obj)
                                prior_folder = obj.id
                        else:  # ls
                            pass
                    else:
                        if splt_line[0].isdigit():  # file
                            size = int(splt_line[0])
                            type = "file"
                            fname = splt_line[1]
                            obj = Dir_CMD(level, itm_id, type, option,
                                          action, size, prior_folder,
                                          None, fname)
                            items.append(obj)
                            prior_folder = obj.id
                        elif splt_line[0] == "dir":  # directory
                            type = "dir"
                            level += 1
                            items.append(Dir_CMD(level, itm_id, type, option,
                                                 action, size, prior_folder,
                                                 None, splt_line[1]))
                        itm_id+=1
        except IOError as err:
            print(f"File does not exist:\t{self.file_str}")
            return
        return items


# This section will allow python file to be run from command line
if __name__ == "__main__":
    obj = Parser(file_in)
    for item in reversed(obj.lines):
        # print(item.make_dict())
        print(item)
