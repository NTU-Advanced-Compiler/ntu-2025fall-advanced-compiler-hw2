"""Local value numbering for Bril.
"""
import json
import sys
from collections import namedtuple

from form_blocks import form_blocks
from util import flatten

# A Value uniquely represents a computation in terms of sub-values.
Value = namedtuple('Value', ['op', 'args'])


class Numbering(dict):
    """A dict mapping anything to numbers that can generate new numbers
    for you when adding new values.
    """

    def __init__(self, init={}):
        super(Numbering, self).__init__(init)
        self._next_fresh = 0

    def _fresh(self):
        n = self._next_fresh
        self._next_fresh = n + 1
        return n

    def add(self, key):
        """Associate the key with a new, fresh number and return it. The
        value may already be in the map; if so, it is overwritten and
        the old number is forgotten.
        """
        n = self._fresh()
        self[key] = n
        return n


def last_writes(instrs):
    """Given a block of instructions, return a list of bools---one per
    instruction---that indicates whether that instruction is the last
    write for its variable.
    """
    out = [False] * len(instrs)
    seen = set()
    for idx, instr in reversed(list(enumerate(instrs))):
        if 'dest' in instr:
            dest = instr['dest']
            if dest not in seen:
                out[idx] = True
                seen.add(instr['dest'])
    return out


def read_first(instrs):
    """Given a block of instructions, return a set of variable names
    that are read before they are written.
    """
    read = set()
    written = set()
    for instr in instrs:
        read.update(set(instr.get('args', [])) - written)
        if 'dest' in instr:
            written.add(instr['dest'])
    return read


def lvn_block(block, lookup, canonicalize, fold):
    """
    TODO:
    Implement local value numbering that supports commutative operations and constant folding.
    The following helper functions may help you complete the job, directly calling them whenever needed. 

    - `lookup`.
        Arguments: a value-to-number map and a value. 
        Return the corresponding number (or None if it does not exist).
    - `canonicalize`. 
        Argument: a value. 
        Returns an equivalent value in a canonical form.
    - `fold`. 
        Arguments: a number-to-constant map  and a value. 
        Return a new constant if it can be computed directly (or None otherwise).
    """
    pass


def _lookup(value2num, value):
    """Value lookup function with propagation through `id` values.
    """
    if value.op == 'id':
        return value.args[0]  # Use the underlying value number.
    else:
        return value2num.get(value)


FOLDABLE_OPS = {
    'add': lambda a, b: a + b,
    'mul': lambda a, b: a * b,
    'sub': lambda a, b: a - b,
    'div': lambda a, b: a // b,
    'gt': lambda a, b: a > b,
    'lt': lambda a, b: a < b,
    'ge': lambda a, b: a >= b,
    'le': lambda a, b: a <= b,
    'ne': lambda a, b: a != b,
    'eq': lambda a, b: a == b,
    'or': lambda a, b: a or b,
    'and': lambda a, b: a and b,
    'not': lambda a: not a
}


def _fold(num2const, value):
    if value.op in FOLDABLE_OPS:
        try:
            const_args = [num2const[n] for n in value.args]
            return FOLDABLE_OPS[value.op](*const_args)
        except KeyError:  # At least one argument is not a constant.
            if value.op in {'eq', 'ne', 'le', 'ge'} and \
               value.args[0] == value.args[1]:
                # Equivalent arguments may be evaluated for equality.
                # E.g. `eq x x`, where `x` is not a constant evaluates
                # to `true`.
                return value.op != 'ne'

            if value.op in {'and', 'or'} and \
               any(v in num2const for v in value.args):
                # Short circuiting the logical operators `and` and `or`
                # for two cases: (1) `and x c0` -> false, where `c0` a
                # constant that evaluates to `false`. (2) `or x c1`  ->
                # true, where `c1` a constant that evaluates to `true`.
                const_val = num2const[value.args[0]
                                      if value.args[0] in num2const
                                      else value.args[1]]
                if (value.op == 'and' and not const_val) or \
                   (value.op == 'or' and const_val):
                    return const_val
            return None
        except ZeroDivisionError:  # If we hit a dynamic error, bail!
            return None
    else:
        return None


def _canonicalize(value):
    """Cannibalize values for commutative math operators.
    """
    if value.op in ('add', 'mul'):
        return Value(value.op, tuple(sorted(value.args)))
    else:
        return value


def lvn(bril):
    """Apply the local value numbering optimization to every basic block
    in every function.
    """
    for func in bril['functions']:
        blocks = list(form_blocks(func['instrs']))
        for block in blocks:
            lvn_block(
                block,
                lookup=_lookup,
                canonicalize=_canonicalize,
                fold=_fold,
            )
        func['instrs'] = flatten(blocks)


if __name__ == '__main__':
    bril = json.load(sys.stdin)
    lvn(bril)
    json.dump(bril, sys.stdout, indent=2, sort_keys=True)
