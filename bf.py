#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Brainf*** interpreter.
Alejandro Santos, @alejolp
https://github.com/alejolp/bf
"""

import os, sys

def syntax_check(CODE):
    """
    Check if the [] are balanced.
    """
    stack = 0
    for i, c in enumerate(CODE):
        if c == '[':
            stack = stack + 1
        elif c == ']':
            stack = stack - 1
            if stack < 0:
                raise Exception("Syntax error: unbalanced [] at " + str(i))

    if stack != 0:
        raise Exception("Syntax error: unbalanced []")

def build_jump_table(CODE):
    """
    Builds the jump table for the []
    """
    JT = {}
    stack = []

    for i, c in enumerate(CODE):
        if c == '[':
            stack.append(i)
        elif c == ']':
            x = stack.pop(-1)
            JT[i] = x
            JT[x] = i

    return JT

def main():
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        f = open(file_name, 'r')
    else:
        f = sys.stdin

    # Memory
    M = [0] * (1 << 16)

    # Pointer to M
    P = 0

    # Instruction pointer to CODE
    ip = 0

    CODE = f.read()
    f.close()

    syntax_check(CODE)

    JT = build_jump_table(CODE)

    while ip < len(CODE):
        c = CODE[ip]
        ip = ip + 1

        if c == '>':
             P = P + 1
        elif c == '<':
            P = P - 1
        elif c == '+':
            M[P] = M[P] + 1
        elif c == '-':
            M[P] = M[P] - 1
        elif c == '[':
            if M[P] == 0:
                ip = JT[ip - 1] + 1
        elif c == ']':
            ip = JT[ip - 1]
        elif c == '.':
            sys.stdout.write(chr(M[P]))
        elif c == ',':
            M[P] = ord(sys.stdin.read(1))

if __name__ == '__main__':
    main()
