from dataclasses import dataclass
from itertools import combinations

@dataclass(frozen=True,slots=True,order=True)
class Position:
    """3D coordinate."""
    x:int
    y:int
    z:int
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"
    
    def distance(self,other:"Position") -> float:
        delta_x = (self.x - other.x) ** 2
        delta_y = (self.y - other.y) ** 2
        delta_z = (self.z - other.z) ** 2
        return (delta_x + delta_y + delta_z) ** 0.5

IType = list[Position]
"""The "full" input-data. One input.txt file should parse into one IType"""

def parse_input(input_content:str) -> IType:
    retval = list()
    for line in input_content.splitlines():
        coords = list(int(c) for c in line.strip().split(","))
        retval.append(Position(*coords))
    return retval

def star_one(data:IType) -> str:
    distance_cache:dict[tuple[Position,Position],float] = dict()
    for first,second in combinations(data,2): # 499500 operations; should be OK?
        key = min(first,second),max(first,second)
        value = first.distance(second)
        distance_cache[key] = value
    nearest_pairs = sorted(distance_cache.keys(),key=lambda pair: distance_cache[pair])
    #Can't really test this easily; the example expects 10 connections, while the real run expects 1000
    #So, improvise.
    is_test = len(data) == 20
    
    circuits:list[set[Position]] = list()
    max_connections = 10 if is_test else 1000
    for left, right in nearest_pairs[0:max_connections]:
        l_circ = None
        r_circ = None
        for circuit in circuits:
            if left in circuit:
                l_circ = circuit
            if right in circuit:
                r_circ = circuit
        if l_circ is not None and r_circ is not None and l_circ != r_circ:
            #Merge the circuits. Both nodes are already included anyway.
            circuits.remove(l_circ)
            circuits.remove(r_circ)
            new_circuit = l_circ.union(r_circ)
            circuits.append(new_circuit)
        elif l_circ is not None:
            #Add the new node to the existing circuit.
            l_circ.add(right)
        elif r_circ is not None:
            r_circ.add(left)
        else:
            #Create a new circuit.
            circuits.append(set([left,right]))
    sizes = sorted((len(circuit) for circuit in circuits),reverse=True)
    retval = sizes[0] * sizes[1] * sizes[2]
    return str(retval)

def star_two(data:IType) -> str:
    pass

if __name__ == "__main__":
    from pathlib import Path
    source = input("Path to input data? (leave blank for 'input/day_08.txt')")
    if source == "" :
        source = Path(__file__).parent.parent / "input" / "day_08.txt"
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
