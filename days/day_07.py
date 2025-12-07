from dataclasses import dataclass;

@dataclass(frozen=True, slots=True)
class Splitter:
    """One splitter's position."""
    row:int
    column:int
    
    def down(self) -> "Splitter":
        return Splitter(self.row + 1, self.column)
    
    def sides(self) -> tuple["Splitter","Splitter"]:
        return Splitter(self.row,self.column-1),Splitter(self.row,self.column+1)
    
    def __str__(self) -> str:
        return f"({self.column},{self.row})"

IType = tuple[int,set[Splitter],int]
"""All the relevant data from the input file. In order of appearance: column
of the starting point (always on row 0), collection of all splitter-positions, height of the map."""

def parse_input(input_content:str) -> IType:
    lines = input_content.splitlines()
    starting_column = lines[0].index("S")
    splitters = set()
    for y, row in enumerate(lines):
        for x, char in enumerate(row):
            if char == "^":
                splitters.add(Splitter(y,x))
    return starting_column, splitters, len(lines)


def star_one(data:IType) -> str:
    beams = set()
    beams.add(Splitter(0,data[0]))
    splitters = data[1]
    retval = set()
    
    for y in range(data[2]-1):
        # Changing the collection while filtering is an error, so pre-filter
        # and save the result.
        relevant_beams = list(filter(lambda b: b.row == y, beams))
        for current_beam in relevant_beams:
            next_beam = current_beam.down()
            if next_beam in splitters:
                beams.update(next_beam.sides())
                retval.add(next_beam)
            else:
                beams.add(next_beam)
    return str(len(retval))

def star_two(data:IType) -> str:
    start_col, splitters, height = data
    
    # Approach: let the numbers "trickle down."
    beam_path:dict[Splitter,int] = dict()
    beam_path[Splitter(0,start_col)] = 1
    for y in range(height-1):
        to_check = list(filter(lambda b:b.row == y,beam_path.keys()))
        for beam in to_check:
            next_beam = beam.down()
            if next_beam in splitters:
                left, right = next_beam.sides()
                beam_path[left] = beam_path.get(left,0) + beam_path[beam]
                beam_path[right] = beam_path.get(right,0) + beam_path[beam]
            else:
                beam_path[next_beam] = beam_path.get(next_beam,0) + beam_path[beam]
    return str(sum(beam_path[beam] for beam in beam_path.keys() if beam.row == height-1))
            

if __name__ == "__main__":
    from pathlib import Path
    source = input("Path to input data? (leave blank for 'input/day_07.txt')")
    if source == "" :
        source = Path(__file__).parent.parent / "input" / "day_07.txt"
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
