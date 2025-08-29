import sys
import json
from form_blocks import form_blocks
from util import flatten


def trivial_dce_pass(func):
    """
    TODO:
    1. Remove instructions from `func` that are never used as arguments to any other instruction.
    2. Return a bool indicating whether anything changed.
    """
    return False



def drop_killed_pass(block):
    """
    TODO:
    1. Delete instructions in a single block whose result is unused before the next assignment. 
    2. Return a bool indicating whether anything changed.
    """
    return False


def trivial_dce_plus(func):
    while trivial_dce_pass(func) or drop_killed_pass(func):
        pass




def localopt():
    modify_func = trivial_dce_plus
    # Apply the change to all the functions in the input program.
    bril = json.load(sys.stdin)
    for func in bril['functions']:
        modify_func(func)
    json.dump(bril, sys.stdout, indent=2, sort_keys=True)


if __name__ == '__main__':
    localopt()
