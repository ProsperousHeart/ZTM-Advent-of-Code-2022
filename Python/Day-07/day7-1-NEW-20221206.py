# https://docs.python.org/3/library/pprint.html
import pprint

from itertools import groupby

pp = pprint.PrettyPrinter(indent=4)

# file_in = "Files/test.txt"
file_in = "Files/test2.txt"
# file_in = "Files/input.txt"

dir_struct = [
]

max_size = 100000

class Dir_CMD:
    def __init__(self, name:str, type:str, sid:int, pid:int, level:int=0, size:int=0):
        """
        TYPES:
            T1  executed command
                cd, ls
            T2  output
        """
        self.name = name
        self.type = type
        self.sid = sid  # self ID
        self.pid = pid  # parent ID
        self.size = size
        self.level = level

    def make_dict(self):
        return dict(
            name=self.name,
            type=self.type,
            level=self.level,
            size=self.size,
            sid = self.sid,
            pid = self.pid
        )

    def __repr__(self):
        return f"""Dir_CMD(
            name={self.name},
            type={self.type},
            level={self.level},
            size={self.size},
            sid = {self.sid},
            pid = {self.pid}
)"""
    # def __repr__(self):
    #     return str(self.make_dict())

    # def __str__(self):
    #    return str(pp.pprint(self.make_dict()))
    def __str__(self):
        return f"""Dir_CMD(
            name={self.name},
            type={self.type},
            level={self.level},
            size={self.size},
            sid = {self.sid},
            pid = {self.pid}
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
        self.dirs = self.find_dirs()
        self.add_dirs(self.dirs)

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
                loc = 0
                level = 0
                id_num = 1
                parent_id = None
                for line_num, line in enumerate(file):
                    # print(line_num)
                    parsed_line = line.strip().split(" ")
                    print('next line:', parsed_line)
                    chg_bool = False
                    if " ".join(parsed_line) == "$ cd /":
                        if line_num == 0:
                            print("===========START OF FILE=======")
                            parent_id = 0
                            dir_struct.append(("/", "dir", 0, 0, id_num, parent_id))  # folder name, type, level, size, id, parent ID
                            chg_bool = True
                            level = dir_struct[-1][2] + 1
                            parent_id = dir_struct[-1][-2]
                            print("parent_id:", parent_id)
                        print("moving to:", dir_struct[0])
                        level = dir_struct[0][2]+1
                    elif parsed_line[0] == "$":
                        if parsed_line[1] == "cd":
                            if parsed_line[2] == "..":
                                print("CHANGE DIR:  go up 1 level")
                                level-=1
                            else:
                                print(f"CHANGE DIRECTORY: non-root folder ({parsed_line[-1]})")
                                # print("???", [item for indx, item in enumerate(dir_struct) if item[0] == parsed_line[2]])
                                # print(dir_struct)
                                # print(parsed_line)
                                list_idx, line_info = next(((indx, info) for (indx, info) in enumerate(dir_struct) if info[0] == parsed_line[2]), None)
                                level = line_info[2]
                                print('line_info:', line_info)
                                print('level:', level)
                                parent_id = line_info[-2]
                                print('parent_id:', parent_id)
                                if level:
                                    print("moving to:", dir_struct[level])
                                    level+=1
                                    print("NEW LEVEL:", level)
                                else:
                                    print("Folder not yet created")
                                    parent_id = None
                        elif parsed_line[1] == "ls":
                            # dir_item = next((info for (indx, info) in enumerate(dir_struct) if info[1] == "dir" and info[2] == loc), None)
                            # print("dir_item", dir_item)
                            pass
                        else:
                            print("============= ERROR =================")
                    else: # directory or file
                        print("Directory or file! parent_id:", parent_id)
                        # print("parsed_line:", parsed_line)
                        if parsed_line[0] == "dir":  # directory
                            # level+=1
                            dir_struct.append((parsed_line[1], "dir", level, 0, id_num, parent_id))  # folder name, type, level, size, id, parent ID
                            chg_bool = True
                        elif parsed_line[0].isdigit():
                            dir_struct.append((parsed_line[1], "file", level, int(parsed_line[0]), id_num, parent_id))
                            chg_bool = True
                            list_idx, parent2update = [[dir_itm_idx, dir_itm] for dir_itm_idx, dir_itm in enumerate(dir_struct) if dir_itm[-2] == parent_id][0]
                            print("NEXT!!!", parent2update)
                            # print(dir_struct[list_idx])
                            tmp_data = list(dir_struct[list_idx])
                            tmp_data[-3] += int(parsed_line[0])
                            dir_struct[list_idx] = tuple(tmp_data)
                        else:
                            print("============== ERROR ==============")

                    if chg_bool:
                        print('updated dir_struct:', dir_struct)
                        id_num+=1
        except IOError as err:
            print(f"File does not exist:\t{self.file_str}")
            return
        return items

    def add_dirs(self, dirs):

        pids = list(set([item[-1] for item in dirs]))
        print("pids", pids)
        for pid in reversed(pids):
            if pid != 0:
                items = [item for item in dirs if item[-1] == pid]
                print(items)
                total = sum([item[-3] for item in dirs if item[-1] == pid])
                print(pid, total)
                # print("looking...", [(idx, item) for idx, item in enumerate(dir_struct) if item[-2] == pid])
                idx2update = [idx for idx, item in enumerate(dir_struct) if item[-2] == pid][0]
                tmp = list(dir_struct[idx2update])
                print("tmp", tmp)
                tmp[-3]+=total
                print("tmp", tmp)
                dir_struct[idx2update] = tuple(tmp)
            else:
                items = [item for item in dirs if item[-1] == pid]
                print(items)
                total = sum([item[-3] for item in dir_struct if item[1] != "dir"])
                print(pid, total)
                # print("add them up")
                # items = [item for item in dirs if item[-1] == pid]
                # print(items)
                tmp = list(dir_struct[0])
                # print("tmp", tmp)
                # tmp[-3]+=sum([item[-3] for item in self.dirs if item[-1] == items[0][-2]])
                tmp[-3] = total
                # print("tmp", tmp)
                dir_struct[0] = tuple(tmp)

        self.dirs = self.find_dirs()


    def add_dirs_original(self, dirs):
        print("add_dirs...")
        for item in dirs:
            print(item)
            if item[-1] != 0:
                print("not root")
                parent_idx, parent_dir = [(idx, dir) for idx, dir in enumerate(dirs) if dir[-2] == item[-1]][0]
                parent_dir = list(parent_dir)
                print(parent_idx, parent_dir)
                parent_dir[-3]+=item[-3]
                dir_struct[parent_idx] = tuple(parent_dir)
                print(dir_struct)

    def find_dirs(self):
        print("STARTING SEARCH")
        dirs = [item for item in dir_struct if item[1] == 'dir']
        print('dirs', dirs)
        print("ENDING SEARCH")
        return dirs

    def get_kids(self, name:str, pid:int):
        # for item in dir_struct:
            # print(pid, item[-1])
            # if item[-1] == pid:
            #     print(item)
        return [item for item in dir_struct if item[-1] == pid and item[0] != name]

    def get_sizes_old2(self, dirs):
        # dirs = self.dirs
        data = []
        for dir_item in dirs:
            # does this item have any folder items?
            kids = self.get_kids(dir_item[0], dir_item[-2])
            print(f"{dir_item[0]}:", kids)
            if len(kids) == 0:
                print("======= ERROR ===========")
            else:
                tmp_dirs = [item for item in kids if item[1] == "dir"]
                if (any(tmp_dirs)):
                    print("DIRECTORY FOUND!!!")
                    print("tmp_dirs", tmp_dirs)
                    for dir_itm in tmp_dirs:
                        print(dir_itm)
                        self.get_sizes([dir_itm])
                else:
                    size = sum([item[-3] for item in kids])
                    data.append((dir_item[0], size))
        return data

    def get_sizes_old(self):
        print("STARTING SIZE COUNT")
        totals = []
        dirs = self.dirs
        for item in dirs:
            print("next item:", item)
            item_id = item[-2]
            parent_id = item[-1]
            print(f"item_id ({item_id})\tparent_id ({parent_id})")
            # item_files = [file_info for file_info in dir_struct if file_info[-1] == item_id]
            item_files = self.get_kids(item[0], item_id)
            print("new files:", item_files)
            total_num = sum([item[3] for item in item_files])
            print("total_num:", total_num)
            totals.append((item[0], total_num))
        print("totals:")
        pp.pprint(totals)
        print("ENDING SIZE COUNT")


# This section will allow python file to be run from command line
if __name__ == "__main__":
    obj = Parser(file_in)
    # for item in reversed(obj.lines):
    #     # print(item.make_dict())
    #     print(item)
    # pp.pprint(dir_struct)
    # obj.find_dirs()
    # print(obj.dirs)
    # pp.pprint(obj.get_sizes(obj.dirs))
    print("final list", dir_struct)
    under = [directory for directory in dir_struct if directory[1] == "dir" and 0 < directory[-3] <= max_size]
    pp.pprint(under)
    sum_list = [item[-3] for item in under]
    total_size = sum(sum_list)
    pp.pprint(total_size) # 1144079 is wrong, too low
    # print(dir_struct)
