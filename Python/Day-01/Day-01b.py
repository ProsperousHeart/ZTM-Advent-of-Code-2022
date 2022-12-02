import requests
from bs4 import BeautifulSoup

# day1_url = "https://adventofcode.com/2022/day/1/input"
file_str = r"Files/Day1.txt"


class Elves():
    def __init__(self, file: str, top: int):
        self.file_in = file
        self.elves = self.read2parse()
        self.elves_sorted = self.sort_desc()
        self.top = self.add_top(top)

    def read2parse(self, ):
        cal_list = []
        try:
            with open(self.file_in, 'r') as file_in:
                elf_cals = 0
                for line in file_in:
                    line = line.strip()
                    # print(f"line:\t{line} ({len(line)} + {line.isdigit()})")
                    if len(line) > 0 and line.isdigit():
                        elf_cals += int(line)
                        # print(f"New cals:\t{elf_cals}")
                    else:
                        cal_list.append(elf_cals)
                        elf_cals = 0
        except IOError as err:
            print(f"File does not exist:\t{self.file_in}")

        return cal_list

    def sort_desc(self):
        desc_cals = sorted(self.elves, reverse=True)
        # print(desc_cals)
        return desc_cals

    def add_top(self, num: int):
        return sum(self.elves_sorted[:num])


def pull_HTML(url: str):
    # https://stackoverflow.com/a/33566923/10474024
    req = requests.get(day1_url)
    print(req)
    return req.text


# This section wil allow python file to be run from command line
if __name__ == "__main__":
    # html = pull_HTML(day1_url)
    # print(html)

    elf_obj = Elves(file_str, 3)
    print(elf_obj.top)
