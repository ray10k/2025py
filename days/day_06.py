import re



IType = tuple[list[list[int]],list[list[int]],list[bool]]
"""The "full" input-data. One input.txt file should parse into one IType. The contents
are the grid of horizontal numbers, the grid of vertical numbers and a list of operations; 
True means add, False means multiply."""

def parse_input(input_content:str) -> IType:
    grid = list()
    operations = list()
    number_pt = re.compile(r"\d+")
    
    lines = input_content.strip().splitlines()
    column_len = max(len(line) for line in lines)
    
    for num_line in lines[:-1]:
        numbers = list(int(num) for num in number_pt.findall(num_line))
        grid.append(numbers)
    
    #Well, that's a first for me. Turns out that star 2 is a *parsing* challenge.
    grid_2 = list()
    
    for x in range(column_len):
        v_num = "".join(lines[y][x] for y in range(len(lines)-1))
        
    
    for operation in lines[-1].strip():
        if operation not in "*+":
            continue
        operations.append(operation == "+")
    
    return grid, grid_2, operations

def star_one(data:IType) -> str:
    grid, _, operations = data
    results:list[int] = list(int(not op) for op in operations) #Multiply columns need to start at 1, add columns at 0.

    for row in grid:
        for x, column in enumerate(row):
            if operations[x]:
                results[x] += column
            else:
                results[x] *= column
    return str(sum(results))

def star_two(data:IType) -> str:
    _, grid, operations = data
    return star_one((grid, None, operations))

if __name__ == "__main__":
    from pathlib import Path
    source = input("Path to input data? (leave blank for 'input/day_06.txt')")
    if source == "" :
        source = Path(__file__).parent.parent / "input" / "day_06.txt"
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
