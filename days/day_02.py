from dataclasses import dataclass;

@dataclass
class InputItem:
    """Representation of one 'unit' of input-data. May represent as little
    as a single character from input, as much as the entire file, or anywhere
    inbetween."""
    start:str
    end:str
    
    def into_range(self) -> range:
        return range(int(self.start),int(self.end)+1)

IType = list[InputItem]
"""The "full" input-data. One input.txt file should parse into one IType"""

def is_repeated(value:int) -> bool:
    """Checks if the given number matches the conditions for star one.

    Args:
        value (int): A number that may be "invalid"

    Returns:
        bool: True if the number is "invalid", False otherwise.
    """
    str_value = str(value)
    #Easy case: only even-length numbers can be invalid.
    if len(str_value) % 2 != 0:
        return False
    halfway = len(str_value) // 2
    return str_value[0:halfway] == str_value[halfway:]

def parse_input(input_content:str) -> IType:
    retval = list()
    for input_range in input_content.split(","):
        start, end = input_range.split("-")
        retval.append(InputItem(start,end))
    return retval

def star_one(data:IType) -> str:
    retval = 0
    for data_range in data:
        for id_to_check in data_range.into_range():
            if is_repeated(id_to_check):
                retval += id_to_check
    return str(retval)

def star_two(data:IType) -> str:
    pass

if __name__ == "__main__":
    from pathlib import Path
    source = input("Path to input data? (leave blank for 'input/day_02.txt')")
    if source == "" :
        source = Path(__file__).parent.parent / "input" / "day_02.txt"
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
