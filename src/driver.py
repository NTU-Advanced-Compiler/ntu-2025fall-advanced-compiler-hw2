import sys
from bril import parse_bril, serialize_bril, Program
from ssa_construct import construct_ssa

def main():
    import argparse

    parser = argparse.ArgumentParser(description='SSA Construction for Bril Programs')
    parser.add_argument('--input', type=str, help='Input Bril JSON file', default=None)
    parser.add_argument('--output', type=str, help='Output Bril JSON file', default=None)
    args = parser.parse_args()

    if args.input:
        with open(args.input, 'r') as f:
            json_input = f.read()
    else:
        json_input = sys.stdin.read()

    program = parse_bril(json_input)

    for function in program.functions:
        construct_ssa(function)

    json_output = serialize_bril(program)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(json_output)
    else:
        print(json_output)

if __name__ == '__main__':
    main()