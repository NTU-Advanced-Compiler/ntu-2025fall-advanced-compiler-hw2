import sys
import json
from form_blocks import form_blocks
from util import flatten


def trivial_dce_pass(func):
    """Remove instructions from `func` that are never used as arguments
    to any other instruction. Return a bool indicating whether we deleted
    anything.
    """
    blocks = list(form_blocks(func['instrs']))

    # Find all the variables used as an argument to any instruction,
    # even once.
    used = set()
    for block in blocks:
        for instr in block:
            # Mark all the variable arguments as used.
            used.update(instr.get('args', []))

    # Delete the instructions that write to unused variables.
    changed = False
    for block in blocks:
        # Avoid deleting *effect instructions* that do not produce a
        # result. The `'dest' in i` predicate is true for all the *value
        # functions*, which are pure and can be eliminated if their
        # results are never used.
        new_block = [i for i in block
                     if 'dest' not in i or i['dest'] in used]

        # Record whether we deleted anything.
        changed |= len(new_block) != len(block)

        # Replace the block with the filtered one.
        block[:] = new_block

    # Reassemble the function.
    func['instrs'] = flatten(blocks)

    return changed


def trivial_dce(func):
    """Iteratively remove dead instructions, stopping when nothing
    remains to remove.
    """
    while trivial_dce_pass(func):
        pass


def drop_killed_local(block):
    # TODO: 
    # Delete instructions in a single basic block whose result is unused before the next assignment. 
    # Return a bool indicating whether anything changed.
    pass


def drop_killed_pass(func):
    """Drop killed functions from *all* blocks. Return a bool indicating
    whether anything changed.
    """
    blocks = list(form_blocks(func['instrs']))
    changed = False
    for block in blocks:
        changed |= drop_killed_local(block)
    func['instrs'] = flatten(blocks)
    return changed


def trivial_dce_plus(func):
    """Like `trivial_dce`, but also deletes locally killed instructions.
    """
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
