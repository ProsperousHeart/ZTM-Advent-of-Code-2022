# Day 1 Requirements

Advent of Code Day 1 is [here](https://adventofcode.com/2022/day/1).
- puzzle input [here](https://adventofcode.com/2022/day/1/input)

## Part 1
Need to take the input (a web page with numbers on it) and:
1. each grouping of numbers is what a single elf has
2. find a way to determine the total calories carried
3. provide the total calories the elf with the most has

## Part 2

Need to show top 3 elves' calories combined total.

# Day 2 Requirements - Rock Paper Scissors

The information in [the encrypted file](Day-02/Files/StrategyGuide.txt) has 2 columns:
1. what opponent will play
2. what you should play in response

## Expectations

Winner with the highest score, where:
- total score:  sum of your scores per round
- your choice:  Rock (1), Paper (2), Scissors (3)
- round outcome:  lost (0), draw (3), won (16)

### Opponent
- Rock - A
- Paper - B
- Scissors - C

### Response
- Rock - X
- Paper - Y
- Scissors - Z

# Day 3 - Rucksack Reorganization

## Part 1

You have a "sack" with 2 compartments. Certain objects go in a specific section.

An elf messed up 1 item. Need to find errors.
Every type is ID'd by a single lower or upper case letter (a and A are different)
lowercase are 1-26 in priority, upper are 27-52

First half of string is one side, the rest is the other. Which item appears in both?
There could be duplicates

what is the sum of priorities shared?

## Part 2

Need to read in a file of lines that have characters. But this time, every set of 3 belongs to a group. And 1 character matches among them.

Take that character and provide it a number same as before. Add those numbers up.

# Day 4

TBD
