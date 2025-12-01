
IType = list[int]
"""The "full" input-data. One input.txt file should parse into one IType"""

def parse_input(input_content:str) -> IType:
    # format per line is [LR]\d\d?
    # Treat turns right as positive, turns left as negative.
    retval = list()
    for line in input_content.strip().splitlines():
        if line.strip() == "":
            continue
        distance = int(line.strip()[1:])
        if line[0] == "L":
            distance = -distance
        retval.append(distance)
    return retval

def star_one(data:IType) -> str:
    zero_count = 0
    pointing_at = 50
    for turn in data:
        pointing_at += turn
        pointing_at %= 100
        if not pointing_at:
            zero_count += 1
    return str(zero_count)

def star_two(data:IType) -> str:
    pass

if __name__ == "__main__":
    from pathlib import Path
    source = input("Path to input data? (leave blank for 'input/day_01.txt')")
    if source == "" :
        source = Path(__file__).parent.parent / "input" / "day_01.txt"
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
