from dataclasses import dataclass;

@dataclass(frozen=True,slots=True)
class Coordinate:
    """Location of a single red tile."""
    column:int
    row:int

IType = list[Coordinate]
"""The "full" input-data. One input.txt file should parse into one IType"""

def parse_input(input_content:str) -> IType:
    retval = list()
    for red_tile in input_content.strip().splitlines():
        x,y = red_tile.split(",")
        retval.append(Coordinate(int(x),int(y)))
    return retval

def star_one(data:IType) -> str:
    top = min(data,key=lambda x: x.row).row
    bottom = max(data,key=lambda x: x.row).row
    left = min(data,key=lambda y: y.column).column
    right = max(data,key=lambda y:y.column).column
    hsplit = left + (right-left) // 2
    vsplit = top + (bottom-top) // 2

    quadrants:dict[tuple[bool,bool],list[Coordinate]] = {(True,True):list(),(True,False):list(),(False,True):list(),(False,False):list()}
    for tile in data:
        h = tile.column >= hsplit
        v = tile.row >= vsplit
        quadrants[(h,v)].append(tile)
    
    retval = 0
    #top-left / bottom-right first.
    for topleft in quadrants[(False,False)]:
        for bottomright in quadrants[(True,True)]:
            delta_x = (bottomright.column - topleft.column) +1
            delta_y = (bottomright.row - topleft.row) +1
            retval = max(retval,delta_x*delta_y)
    #top-right / bottom-left next.
    for topright in quadrants[(True,False)]:
        for bottomleft in quadrants[(False,True)]:
            delta_x = (topright.column - bottomleft.column) +1
            delta_y = (bottomleft.row - topright.row) +1
            retval = max(retval, delta_x * delta_y)
    return str(retval)

def star_two(data:IType) -> str:
    pass

if __name__ == "__main__":
    from pathlib import Path
    source = input("Path to input data? (leave blank for 'input/day_09.txt')")
    if source == "" :
        source = Path(__file__).parent.parent / "input" / "day_09.txt"
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
