import requests
from bs4 import BeautifulSoup

# day1_url = "https://adventofcode.com/2022/day/1/input"
file_str = r"Files/Day1.txt"

def pull_HTML(url: str):
    # https://stackoverflow.com/a/33566923/10474024
    req = requests.get(day1_url)
    print(req)
    return req.text

def read2parse(file: str):
    high_num = 0
    try:
        with open(file, 'r') as file_in:
            elf_cals = 0
            for line in file_in:
                line = line.strip()
                # print(f"line:\t{line} ({len(line)} + {line.isdigit()})")
                if len(line) > 0 and line.isdigit():
                    elf_cals += int(line)
                    print(f"New cals:\t{elf_cals}")
                else:
                    if elf_cals > high_num:
                        high_num = elf_cals
                    print("resetting cals ...\n")
                    elf_cals = 0
    except IOError as err:
        return (True, "File does not exist.")
    return (False, str(high_num))

# This section wil allow python file to be run from command line
if __name__ == "__main__":
    # html = pull_HTML(day1_url)
    # print(html)

    fail_bool, cals = read2parse(file_str)
    if fail_bool:
        print(cals)
    else:
        print(f"Highest amount of calories:\t{cals}")
