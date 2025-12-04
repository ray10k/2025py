from dataclasses import dataclass;

@dataclass(frozen=True,slots=True)
class InputItem:
    """Representation of one 'unit' of input-data. May represent as little
    as a single character from input, as much as the entire file, or anywhere
    inbetween."""
    x:int
    y:int
    
    def __add__(self,other):
        return InputItem(self.x + other.x, self.y+other.y)

IType = tuple[set[InputItem],int,int]
"""The "full" input-data. One input.txt file should parse into one IType"""

NEIGHBOURS = [InputItem(-1,-1),InputItem(-1,0),InputItem(-1,1),
              InputItem(0,-1),               InputItem(0,1),
              InputItem(1,-1),InputItem(1,0),InputItem(1,1)]

def show_map(data:IType):
    map_data, width, height = data
    
    print(f"{width=}; {height=}")
    for y in range(height):
        for x in range(width):
            if InputItem(x,y) in map_data:
                print("@",end="")
            else:
                print(" ",end="")
        print("")

def parse_input(input_content:str) -> IType:
    retval = set()
    
    width = 0
    height = 0
    
    for y,row in enumerate(input_content.splitlines()):
        for x,column in enumerate(row):
            if column == "@":
                retval.add(InputItem(x,y))
        width = max(width,len(row))
        height += 1
    
    return retval, width, height

def star_one(data:IType) -> str:
    map_data = data[0]
    
    show_map(data)
    found = set()
    
    retval = 0
    
    for here in map_data:
        free_spaces = 0
        for neighbour in NEIGHBOURS:
            offset = here + neighbour
            if offset not in map_data:
                free_spaces += 1
                
        if free_spaces > 4:
            found.add(here)
            retval += 1
                
    return str(retval)

def star_two(data:IType) -> str:
    map_data = data[0]
    
    found = set()
    
    retval = 0
    
    while True:
        found.clear()
        for here in map_data:
            free_spaces = 0
            for neighbour in NEIGHBOURS:
                offset = here + neighbour
                if offset not in map_data:
                    free_spaces += 1
                    
            if free_spaces > 4:
                found.add(here)
                retval += 1
        map_data.difference_update(found)
        if not found:
            break
                
    return str(retval)

if __name__ == "__main__":
    from pathlib import Path
    source = input("Path to input data? (leave blank for 'input/day_04.txt')")
    if source == "" :
        source = Path(__file__).parent.parent / "input" / "day_04.txt"
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
