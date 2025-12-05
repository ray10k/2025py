from collections import deque
from dataclasses import dataclass
from itertools import islice;

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
    
    def overlaps(self,other:"IdRange") -> bool:
        return self.end + 1 == other.start or other.end + 1 == self. start or not (self.end < other.start or self.start > other.end)
        
    def merge(self,other:"IdRange"):
        self.start = min(self.start,other.start)
        self.end = max(self.end,other.end)
    
    def __len__(self) -> int:
        return (self.end - self.start) + 1
    
    def __str__(self) -> str:
        return f"<{self.start}-{self.end}>"
    
    def __lt__(self,other:"IdRange"):
        return self.start < other.start

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
    ranges, ingredients = data
    retval = 0
    for ingredient in ingredients:
        for id_range in ranges:
            if id_range.check_id(ingredient):
                retval += 1
                break
    return str(retval)

def check_or_merge(base:IdRange, other:IdRange) -> bool:
    if not base.overlaps(other):
        return True
    base.merge(other)
    return False

def sliding_window(iterable, n):
    "Collect data into overlapping fixed-length chunks or blocks."
    # sliding_window('ABCDEFG', 4) → ABCD BCDE CDEF DEFG
    iterator = iter(iterable)
    window = deque(islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)

def star_two(data:IType) -> str:
    # *far* too many IDs to manually count them.
    # So, dedupe/merge overlapping ranges, then calculate the sum-of-lengths of the
    # resulting ranges.
    ranges = sorted(data[0],reverse=True)
    reduced_ranges:list[IdRange] = list()
        
    while ranges:
        base_range = ranges.pop()
        while True:
            #Find all overlapping ranges.
            overlaps = list(filter(lambda x: x[1].overlaps(base_range), enumerate(ranges)))
            #Apply in reverse, removing overlapped ranges from the list.
            for index, id_range in overlaps[::-1]:
                ranges.pop(index)
                base_range.merge(id_range)
            #Keep doing this, until *no* overlapping ranges have been found.
            if len(overlaps) == 0:
                break
        reduced_ranges.append(base_range)
    
    retval = sum(len(id_range) for id_range in reduced_ranges)
    return str(retval)
    

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
