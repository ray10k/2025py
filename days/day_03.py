from dataclasses import dataclass;

@dataclass
class InputItem:
    """Representation of one 'unit' of input-data. May represent as little
    as a single character from input, as much as the entire file, or anywhere
    inbetween."""
    batteries:tuple[int,...]

IType = list[InputItem]
"""The "full" input-data. One input.txt file should parse into one IType"""

def parse_input(input_content:str) -> IType:
    retval = list()
    for bank in input_content.splitlines():
        batteries = tuple(int(x) for x in bank.strip())
        retval.append(InputItem(batteries))
    return retval

def star_one(data:IType) -> str:
    retval = 0
    for battery_bank in data:
        #step 1: find the highest number on the left of the bank.
        left_highest = max(battery_bank.batteries[0:-1])
        #step 2: find the index of that number.
        splitpoint = battery_bank.batteries.index(left_highest) + 1
        #step 3: find the highest number on the right of the bank.
        right_highest = max(battery_bank.batteries[splitpoint:])
        #step 4: combine and add.
        retval += (left_highest*10) + right_highest
    return str(retval)

def star_two(data:IType) -> str:
    pass

if __name__ == "__main__":
    from pathlib import Path
    source = input("Path to input data? (leave blank for 'input/day_03.txt')")
    if source == "" :
        source = Path(__file__).parent.parent / "input" / "day_03.txt"
    else:
        source = Path(source).absolute()
    
    raw_data:str = ""
    with open(source) as ifile:
        raw_data = ifile.read()
    
    parsed_data = parse_input(raw_data)
    result_one = star_one(parsed_data)
    
    print(f"Result 1: {result_one}")
    
    parsed_data = parse_input(raw_data)
    result_two = star_two(parsed_data)
    
    print(f"Result 2: {result_two}")
