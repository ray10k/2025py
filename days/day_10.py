from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Configuration:
    """One machine's target lights, wiring schematics and target joltages."""
    
    lightmask:tuple[bool,...]
    switches:tuple[tuple[int,...],...]
    joltages:tuple[int,...]

IType = list[Configuration]
"""The "full" input-data. One input.txt file should parse into one IType"""

def parse_input(input_content:str) -> IType:
    retval = list()
    segments = re.compile(r"^(?P<mask>\[.+\])(?P<switches>[ \(\)\,0-9]+)(?P<joltage> \{.+\})$")
    switch = re.compile(r"( \([0-9,]+\))")
    
    for config in input_content.splitlines():
        parts = segments.match(config)
        lights = parts.group("mask").strip("[]")
        joltages = parts.group("joltage").strip(" \{\}").split(",")
        switches = parts.group("switches")
        switches = list(sw.strip(" ()").split(",") for sw in switch.split(switches) if len(sw) > 0)
        # Ordering: 0 is the left-most switch. Frustrating.
        parsed_lights = list()
        for light in lights:
            parsed_lights.append(light == "#")
        parsed_switches = list()
        for switch_ in switches:
            wires = tuple(int(x) for x in switch_)
            parsed_switches.append(wires)
        retval.append(Configuration(tuple(parsed_lights),tuple(parsed_switches),tuple(int(jolt) for jolt in joltages)))
    return retval

def star_one(data:IType) -> str:
    retval = 0
    
    #Each button is a toggle-switch. So, pressing a button an even number of times
    # has the same effect as not pressing it at all, and pressing it an odd number
    # of times has the same effect as pressing it once.
    #So, the problem can be simplified to "which buttons need to be pressed?"
    #Total number of possibilities then is 2 ** number_of_buttons - 1 (since there 
    # are no inputs that expect all lights to be off.)
    
    print(max(len(config.switches) for config in data))
    
    #The largest number of switches in the actual data is 13, for a total of ~8k
    # possibilities. Don't overthink it, I guess.
    
    for current_config in data:
        option_count = 2 ** len(current_config.switches)
        best_option = len(current_config.switches)
        for option in range(1,option_count):
            #Treat option as a bit-field; position indicates if that switch should
            # be toggled.
            result = [False] * len(current_config.lightmask)
            pressed = 0
            for position,switch in enumerate(current_config.switches):
                if 1<<position & option:
                    pressed += 1
                    for wire in switch:
                        result[wire] = not result[wire]
            if all(res == goal for res, goal in zip(result,current_config.lightmask)):
                best_option = min(pressed,best_option)
        retval += best_option
            
    
    return str(retval)

def star_two(data:IType) -> str:
    pass

if __name__ == "__main__":
    from pathlib import Path
    source = input("Path to input data? (leave blank for 'input/day_10.txt')")
    if source == "" :
        source = Path(__file__).parent.parent / "input" / "day_10.txt"
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
