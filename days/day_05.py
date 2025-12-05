from dataclasses import dataclass;

@dataclass
class IdRange:
    """Representation of one 'unit' of input-data. May represent as little
    as a single character from input, as much as the entire file, or anywhere
    inbetween."""
    start:int
    end:int
    
    def into_range(self):
        return range(self.start,self.end+1)
    
    def check_id(self,id:int) -> bool:
        return id >= self.start and id <= self.end

IType = tuple[list[IdRange],list[int]]
"""The "full" input-data. One input.txt file should parse into one IType"""

def parse_input(input_content:str) -> IType:
    lines = iter(input_content.splitlines())
    ranges = list()
    while (curr_line := next(lines)) != "":
        left,right = curr_line.strip().split("-")
        ranges.append(IdRange(int(left),int(right)))
    ingredients = list(int(line) for line in lines)
    return ranges, ingredients

def star_one(data:IType) -> str:
    print(len(data[0]),len(data[1]))
    ranges, ingredients = data
    retval = 0
    for ingredient in ingredients:
        for id_range in ranges:
            if id_range.check_id(ingredient):
                retval += 1
                break
    return str(retval)

def star_two(data:IType) -> str:
    pass

if __name__ == "__main__":
    from pathlib import Path
    source = input("Path to input data? (leave blank for 'input/day_05.txt')")
    if source == "" :
        source = Path(__file__).parent.parent / "input" / "day_05.txt"
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
