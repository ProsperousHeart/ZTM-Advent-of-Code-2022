# https://docs.python.org/3/library/pprint.html
import pprint

pp = pprint.PrettyPrinter(indent=4)

# file_in = "Files/test.txt"
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
            dir_struct.append(line_obj)

            # need to also append line_obj to parent's children list
            # parent_idx = line_obj.get_itm_idx(itm_sid=line_obj.pid)
            parent_idx = line_obj.pid
            # print("dir_struct:", dir_struct)
            print("parent_idx:", parent_idx)
            print(f"parent (pre): {dir_struct[parent_idx].name} | {dir_struct[parent_idx].type}")
            if parent_idx != c_sid:
                dir_struct[parent_idx].children.append(line_obj)

            print("====end of new item====")
            print("parent (post):", dir_struct[parent_idx])
            return line_obj, c_sid+1, line_obj.level + 1, line_obj.sid

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
                        elif prsd_line[0].isdigit():  # add file if not already there
                            # see if FILE name already associated with current DIR
                            tmp = [itm.name for itm in dir_struct[curr_grp_sid].children if itm.name == prsd_line[-1]]
                            if len(tmp) > 0:
                                print("===== ERROR:  file already added =====")
                                print("========== UPDATE FILE SIZE??? =============")
                            else:
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
                                print("===== end of adding file =====")
                                print(dir_struct[-1])
                            # if so, update size if needed
                        else:
                            print("==== ERROR - no other expected command ====")

        except IOError as err:
            print(f"File does not exist:\t{self.file_str}")
            return


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


def delete_dir(dir_list: list = dir_struct, max_s: int = max_space,
               spc_need: int = nspace):
    """
    Takes in the list of directories, max space on machine and space needed for work.
    Returns the sum that would be freed up and which directories to choose.
    """

    print("max_s", max_s)
    print("spc_need", spc_need)

    # determine current amount of space available
    # dirs = sorted([item for item in dir_list if item.type == "dir" and item.size >= spc_need], key=lambda x: x.size, reverse=False)
    dirs = sorted([item for item in dir_list if item.type == "dir"], key=lambda x: x.size, reverse=False)
    print("dirs", [(dir_item.name, dir_item.size) for dir_item in dirs])
    avail_spc = max_s - dir_list[0].size
    print(f"avail_spc ({max_s} - {dir_list[0].name} @ {dir_list[0].size}) = ", avail_spc)

    # determine how much is needed to be deleted to reach spc_need
    spc_need = spc_need - avail_spc
    print("spc_need", spc_need)

    # find smallest set of directories to be deleted
    dir_lst = []
    sum2free = 0
    for item in dirs:
        #if sum([itemX.size for itemX in dir_lst]) >= spc_need:
        #   print("Enough has been found!")
        #    break
        #else:
        #    print(f"Adding {item.name} with size {item.size}")
        #    dir_lst.append(item)
        if item.size >= spc_need:
            print(f"Adding {item.name} with size {item.size}")
            dir_lst.append(item)

    # total amount of space that would be freed up
    if len(dir_lst) > 0:
        sum2free = sum([item.size for item in dir_lst])
    print(f"Total for {len(dir_lst)}:", sum2free)
    return (sum2free, dir_lst)


def delete_dir_OLD(dir_list: list = dir_struct, max_s: int = max_space,
               spc_need: int = nspace):

    def del_item(item: Dir_CMD):
        for item in tmp_list[0].children:
            if item.type == "file":
                print(f"Deleting {item.name} ('{item.type}')")
                del dir_struct[item.sid]
            else:
                print(f"Folder {item.name} found!")
                delete_dir(item.children)

    dirs = [dir for dir in dir_list if dir.size >= spc_need]
    if len(dirs) == 0:
        return (False, "NO SINGLE FOLDER WORKS")
    else:
        tmp_list = sorted(dirs, key=lambda x: x.size)
        del dirs
        return (True, tmp_list[0].size)
    print("Following is too high:  43636666")


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

    print("\nDELETION\n")
    sum, dirs = delete_dir(dir_struct, max_space, nspace)
    if sum > 0:
        print([(item.name, item.size) for item in dirs], sum)
        print("Lowest directory size:", dirs[0].size)
    else:
        print("No folders found to be able to delete enough space!")
    print("TOO HIGH:  218928437, 43636666")
