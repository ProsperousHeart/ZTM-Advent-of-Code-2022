# https://docs.python.org/3/library/pprint.html
import pprint

from itertools import groupby

pp = pprint.PrettyPrinter(indent=4)

#file_in = "Files/test.txt"
#file_in = "Files/test2.txt"
file_in = "Files/input.txt"
#file_in = "Files/my-test.txt"
dir_struct = []
max_size = 100000
max_space = 70000000
nspace = 30000000


class Dir_CMD:
    curr_csid = 0  # this should increase with each new instance (sid)
    # obj_list = dir_struct  # class object, so each instance has access to it

    def __init__(self, name: str, type: str, sid: int,
                 pid: int, level: int = 0, size: int = 0,
                 req_max: int = max_size):
        """
        TYPES:
            T1  executed command
                cd, ls
            T2  output
        """
        self.name = name
        self.type = type
        self.level = level
        self.size = size
        self.sid = sid  # self ID
        self.pid = pid  # parent ID
        self.req_max = req_max
        self.children = []

    def get_itm_idx(self, name: str = None, itm_sid: int = None):
        """
        Providing the sid for object needed, will return index in the class object obj_list
        """
        print("========== START get_itm_idx ==========")
        # print(name, itm_sid)
        if itm_sid is not None and 0 < itm_sid:
            print(f"Searching for item with SID: {itm_sid}")
            tmp_list = [idx for idx, item in enumerate(dir_struct) if item.sid == itm_sid]
            # print('tmp_list:', tmp_list)
            if len(tmp_list) > 0:
                print(f"========== FOUND @ idx {tmp_list[0]} -- END get_itm_idx ==========")
                return tmp_list[0]
        elif itm_sid == 0:
            # return dir_struct[0]
            print("========== FOUND -- END get_itm_idx ==========")
            return 0
        elif name:
            print(f"Searching for item with name: {name}")
            name_list = [idx for idx, item in enumerate(dir_struct) if item.name == name]
            print(name_list)
            if len(name_list) > 0:
                print(f"========== FOUND @ idx {name_list[0]} -- END get_itm_idx ==========")
                return name_list[0]
        print("========== FAILED -- END get_itm_idx ==========")
        return None

    def make_dict(self):
        return dict(
            name=self.name,
            type=self.type,
            level=self.level,
            size=self.size,
            sid=self.sid,
            pid=self.pid,
            req_max=self.req_max,
            children=self.children
        )

    def __repr__(self):
        return f"""Dir_CMD(
            name="{self.name}",
            type="{self.type}",
            level={self.level},
            size={self.size},
            sid = {self.sid},
            pid = {self.pid},
            req_max = {self.req_max},
            children = {self.children}
)"""

    # def __repr__(self):
    #     return str(self.make_dict())

    # def __str__(self):
    #    return str(pp.pprint(self.make_dict()))
    def __str__(self):
        return f"""Dir_CMD(
            name="{self.name}",
            type="{self.type}",
            level={self.level},
            size={self.size},
            sid = {self.sid},
            pid = {self.pid},
            req_max = {self.req_max},
            children = {self.children}
)"""


class Parser_20221207:
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
        # self.lines = self.read_inv(self.file_str)
        # self.dirs = self.find_dirs()
        # self.add_dirs(self.dirs)
        self.read_inv(self.file_str)

    def read_inv(self, f_str: str):
        """
        TBD
        """

        def new_item(elmnts:list, c_sid:int, c_pid:int, lvl:int,
                     size:int=0, rmax:int=max_size):
            """
            Creates & returns new DirCMD object.
            :param elmnts:
            :param c_sid:
            :param c_pid:
            :param lvl:
            :param size:
            :param rmax:
            :return:
            """
            print("====ADDING ITEM======")
            if len(elmnts) == 3 or elmnts[0] == "dir":
                type = "dir"
                # lvl += 1
            else:
                type = "file"
                if elmnts[0].isdigit():
                    size=int(elmnts[0])
            name = elmnts[-1]
            line_obj = Dir_CMD(name=name,
                               type=type,
                               sid=c_sid,
                               pid=c_pid,
                               level=lvl,
                               size=size,
                               req_max=rmax)
            print(line_obj)
            # line_obj.curr_csid = line_obj.curr_csid + 1  # class SID (S/N) - prepping for next one
            # line_obj.obj_list.append(line_obj)  # to ensure we can tell if a directory has already been checked
            # items.append(line_obj)
            # curr_grp_sid = line_obj.sid
            dir_struct.append(line_obj)

            # need to also append line_obj to parent's children list
            # parent_idx = line_obj.get_itm_idx(itm_sid=line_obj.pid)
            parent_idx = line_obj.pid
            # print("dir_struct:", dir_struct)
            print("parent_idx:", parent_idx)
            print(f"parent (pre): {dir_struct[parent_idx].name} | {dir_struct[parent_idx].type}")
            if parent_idx != c_sid:
                dir_struct[parent_idx].children.append(line_obj)

            # next two lines should be taken care of in cnt_kids() function
            #if line_obj.type == "file":
            #    dir_struct[parent_idx].size += line_obj.size

            print("====end of new item====")
            print("parent (post):", dir_struct[parent_idx])
            return line_obj, c_sid+1, line_obj.level + 1, line_obj.sid

        #def get_dict_idx(parent_id: int, line_list: list):
        #    item = next((idx for (idx, info) in enumerate(line_list)), None)
        #    print('List IDX of parent:', item)
        #    return item

        # def update_dir_level(itm_sid:int, name_str:str):
        def update_dir_level(itm_sid: int):
            # line_obj should be the folder we moved to
            line_o = dir_struct[itm_sid]
            # level should now be 1+ itm_sid's level
            lvl = line_o.level
            # curr_grp_sid should be itm_sid
            curr_grp_sid = itm_sid
            return lvl, curr_grp_sid, line_o

        cmd = []
        # items = []
        try:
            with open(self.file_str, 'r') as file:
                # curr_dir_sid = 0
                level = 0
                curr_csid = 0
                curr_grp_sid = 0     # current folder level's SID (parent)
                line_obj = None
                for line_num, line in enumerate(file):
                    prsd_line = line.strip().split(" ") # [type (action/dir/file), name, option] or []]
                    print(f"prsd_line:\t{prsd_line}")
                    if " ".join(prsd_line[:2]) == "$ cd":
                        print("=== CHANGE DIRECTORY ===")
                        if line_num == 0 and prsd_line[-1] == "/":
                            print("===========START OF FILE=======")
                            line_obj, curr_csid, level, curr_grp_sid = new_item(elmnts=prsd_line,
                                                c_sid=curr_csid,
                                                c_pid=curr_grp_sid,
                                                lvl=level,
                                                rmax=max_size)
                            print("dir_struct", dir_struct)
                        elif prsd_line[-1] == "..":
                            # go up 1 level
                            print("CHANGE DIR:  go up 1 level to parent")
                            # level-=1
                            print("level:", level)
                            line_obj = dir_struct[curr_grp_sid]
                            level, curr_grp_sid, line_obj = update_dir_level(line_obj.pid)
                            print("new level:", level)
                        else:  # CHANGE TO SOME DIRECTORY
                            # check current directory children - if dir != exist, make one
                            tmp_kids = dir_struct[curr_grp_sid].children
                            tmp_kids = [kid for kid in tmp_kids if kid.name == prsd_line[-1]]
                            print([(item.name, item.type) for item in tmp_kids])
                            if len(tmp_kids) == 0:
                                # make new one
                                print("============== CREATING DIR ON CD ===========")
                                print("curr_grp_sid:", curr_grp_sid)
                                line_obj, curr_csid, level, curr_grp_sid = new_item(elmnts=prsd_line,
                                                    c_sid=curr_csid,
                                                    c_pid=curr_grp_sid,
                                                    lvl=level,
                                                    rmax=max_size)
                            else:
                                tmp_kid = tmp_kids[0]
                                print(tmp_kid)
                                del tmp_kids
                                print(f"============== MOVING TO DIR:  {tmp_kid.name} ===========")
                                level, curr_grp_sid, line_obj = update_dir_level(
                                    tmp_kid.sid,
                                    #prsd_line[-1]
                                )
                        print("=== CD completed ===")
                    elif " ".join(prsd_line) == "$ ls":  # do nothing
                        print("level:", level)
                        # curr_grp_sid = line_obj.sid
                        level+=1
                        print("new level:", level)
                        pass
                    else:
                        if prsd_line[0] == "dir":
                            # see if DIR name already associated with current DIR
                            itm_idx = line_obj.get_itm_idx(name=prsd_line[1])
                            # if None, create new item and add to class list
                            print(prsd_line, curr_csid, curr_grp_sid)
                            if not itm_idx:
                                print("===========NEW DIRECTORY=======")
                                line_obj, curr_csid, _, _ = new_item(elmnts=prsd_line,
                                                    c_sid=curr_csid,
                                                    c_pid=curr_grp_sid,
                                                    lvl=level,
                                                    rmax=max_size)
                                # dir_struct.append(line_obj)  # to ensure we can tell if a directory has already been checked
                                # curr_grp_sid = line_obj.sid
                                # curr_csid += 1
                                # level+=1
                        elif prsd_line[0].isdigit():  # add file if not already there
                            # see if FILE name already associated with current DIR
                            tmp = [itm.name for itm in dir_struct[curr_grp_sid].children if itm.name == prsd_line[-1]]
                            if len(tmp) > 0:
                                print("===== ERROR:  file already added =====")
                                #if dir_struct[itm_idx].size != int(prsd_line[0]):
                                #    dir_struct[itm_idx].size = int(prsd_line[0])
                                print("========== UPDATE FILE SIZE??? =============")
                            else:

                            #itm_idx = line_obj.get_itm_idx(name=prsd_line[1])
                            #print(f"Index of file '{prsd_line[-1]}':", itm_idx)
                            ## if not, create new item, add to class list, increase class SID
                            #if not itm_idx:  # make new item
                                print("=======================================NEW FILE=======")
                                tmp_idx = line_obj.get_itm_idx(itm_sid=curr_grp_sid)
                                print("curr_csid:", curr_csid)
                                print("curr_grp_sid:", curr_grp_sid)
                                print("level:", level)
                                print("tmp_idx:", tmp_idx)
                                if tmp_idx >= 0:
                                    print("name:", dir_struct[tmp_idx].name)
                                    curr_grp_sid = dir_struct[tmp_idx].sid
                                    del tmp_idx
                                else:
                                    print("============================================= ERROR - no parent? ==============")
                                line_obj, curr_csid, _, _ = new_item(elmnts=prsd_line,
                                                    c_sid=curr_csid,
                                                    c_pid=curr_grp_sid,
                                                    lvl=level,
                                                    rmax=max_size)
                                # dir_struct.append(line_obj)  # to ensure we can tell if a directory has already been checked
                                # curr_grp_sid = line_obj.sid
                                # curr_csid += 1
                                print("===== end of adding file =====")
                                print(dir_struct[-1])
                            # if so, update size if needed
                        else:
                            print("==== ERROR - no other expected command ====")

        except IOError as err:
            print(f"File does not exist:\t{self.file_str}")
            return


class Parser_old:
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
                            dir_struct.append(
                                ("/", "dir", 0, 0, id_num, parent_id))  # folder name, type, level, size, id, parent ID
                            chg_bool = True
                            level = dir_struct[-1][2] + 1
                            parent_id = dir_struct[-1][-2]
                            print("parent_id:", parent_id)
                        print("moving to:", dir_struct[0])
                        level = dir_struct[0][2] + 1
                    elif parsed_line[0] == "$":
                        if parsed_line[1] == "cd":
                            if parsed_line[2] == "..":
                                print("CHANGE DIR:  go up 1 level")
                                level -= 1
                            else:
                                print(f"CHANGE DIRECTORY: non-root folder ({parsed_line[-1]})")
                                # print("???", [item for indx, item in enumerate(dir_struct) if item[0] == parsed_line[2]])
                                # print(dir_struct)
                                # print(parsed_line)
                                list_idx, line_info = next(((indx, info) for (indx, info) in enumerate(dir_struct) if
                                                            info[0] == parsed_line[2]), None)
                                level = line_info[2]
                                print('line_info:', line_info)
                                print('level:', level)
                                parent_id = line_info[-2]
                                print('parent_id:', parent_id)
                                if level:
                                    print("moving to:", dir_struct[level])
                                    level += 1
                                    print("NEW LEVEL:", level)
                                else:
                                    print("Folder not yet created")
                                    parent_id = None
                        elif parsed_line[1] == "ls":
                            pass
                        else:
                            print("============= ERROR =================")
                    else:  # directory or file
                        print("Directory or file! parent_id:", parent_id)
                        # print("parsed_line:", parsed_line)
                        if parsed_line[0] == "dir":  # directory
                            # level+=1
                            dir_struct.append((parsed_line[1], "dir", level, 0, id_num,
                                               parent_id))  # folder name, type, level, size, id, parent ID
                            chg_bool = True
                        elif parsed_line[0].isdigit():
                            dir_struct.append((parsed_line[1], "file", level, int(parsed_line[0]), id_num, parent_id))
                            chg_bool = True
                            list_idx, parent2update = \
                            [[dir_itm_idx, dir_itm] for dir_itm_idx, dir_itm in enumerate(dir_struct) if
                             dir_itm[-2] == parent_id][0]
                            print("NEXT!!!", parent2update)
                            # print(dir_struct[list_idx])
                            tmp_data = list(dir_struct[list_idx])
                            tmp_data[-3] += int(parsed_line[0])
                            dir_struct[list_idx] = tuple(tmp_data)
                        else:
                            print("============== ERROR ==============")

                    if chg_bool:
                        print('updated dir_struct:', dir_struct)
                        id_num += 1
        except IOError as err:
            print(f"File does not exist:\t{self.file_str}")
            return
        return items

    def find_dirs(self):
        print("STARTING SEARCH")
        dirs = [item for item in dir_struct if item[1] == 'dir']
        print('dirs', dirs)
        print("ENDING SEARCH")
        return dirs

    # ================================================================================

def update_folders(item_list: list):
    tmp_list = sorted([item for item in item_list if item.type != "file"], key = lambda x: x.sid, reverse=True)
    for item in tmp_list:
        item_list[item.pid].size += item.size

def cnt_kids(item:Dir_CMD):
    print(f"+++++ count kids for {item.name} ++++++")
    size = 0
    for kid in item.children:
        if kid.type == "dir":
            print("--directory found as child--")
            if kid.size > 0:
                print("-- adding known size --")
                size += kid.size
            else:
                size += cnt_kids(kid)
        else:
            size += kid.size
    print(f"+++++ end count kids for {item.name} ++++++")
    return size

def sum_sizes(list2chk:list, msize:int=max_size):
    print("========== START SUM SIZES =========")

    dirs = [dir_item for dir_item in list2chk if dir_item.type == "dir"]
    dirs = sorted(dirs, key=lambda x: x.sid, reverse=True)
    pp.pprint([(item.name, item.sid, item.size) for item in dirs])
    for item in dirs:
        if item.size == 0:
            print("***")
            dir_struct[item.sid].size = cnt_kids(item)
            print(f"item '{item.name}' ({item.type}) on level {item.level}" \
                f" with {len(item.children)} children is" \
                f" {dir_struct[item.sid].size} in size!")
        else:
            print(f"Directory '{item.name}' already calculated!")

    # dir_limited = [dir for dir in list2chk if dir.type == "dir" and dir.size <= msize]
    dir_limited = [(item.name, item.size) for item in list2chk if item.type == "dir" and 0 < item.size <= msize]
    print(dir_limited)

    print("========== STop SUM SIZES =========")
    return sum([item[1] for item in dir_limited])


# This section will allow python file to be run from command line
if __name__ == "__main__":
    Parser_20221207(file_in)

    pp.pprint([(item.level, item.name, item.type, item.size, item.pid, item.sid) for item in dir_struct if item.type == "dir" and 0 < item.size <= max_size])
    print(sum([item.size for item in dir_struct if item.type == "dir" and 0 < item.size <= max_size]))


    print("sum sizes:", sum_sizes(dir_struct, max_size))
    # print(update_folders(dir_struct))
    if file_in == "Files/test.txt":
        print("Need to be 95437")
    if file_in == "Files/input.txt":
        print("FINAL:  1297159")
