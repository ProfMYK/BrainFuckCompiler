#!/bin/env python3

import sys
import subprocess

iota_counter = -1
def iota():
    global iota_counter
    iota_counter += 1
    return iota_counter

PLUS=iota()
MINUS=iota()
RIGHT=iota()
LEFT=iota()
START_LOOP=iota()
END_LOOP=iota()
PRINT=iota()
INPUT=iota()

def plus():
    return PLUS
def minus():
    return MINUS
def right():
    return RIGHT
def left():
    return LEFT
def startLoop():
    return START_LOOP
def endLoop():
    return END_LOOP
def printt():
    return PRINT
def inputt():
    return INPUT

def compileProgram(program, fileLoc):
    with open("temp.c", "w") as f:
        f.write("#include <stdio.h>\n")
        f.write("#include <unistd.h>\n")
        f.write("int main(char argc, char **argv) {\n")
        f.write("char arr[30000]={0};\n")
        f.write("char *ptr=arr;\n")
        for op in program:
            if op == PLUS:
                f.write("++*ptr;\n")
            elif op == MINUS:
                f.write("--*ptr;\n")
            elif op == RIGHT:
                f.write("++ptr;\n")
            elif op == LEFT:
                f.write("--ptr;\n")
            elif op == START_LOOP:
                f.write("while(*ptr){\n")
            elif op == END_LOOP:
                f.write("}\n");
            elif op == PRINT:
                f.write("putchar(*ptr);\n")
            elif op == INPUT:
                f.write("*ptr=getchar();\n")
        f.write("return 0;\n")
        f.write("}\n")
    subprocess.call(["gcc", "-o", fileLoc, "temp.c"])
    subprocess.call(["rm", "temp.c"])
            
def simulateProgram(program):
    arr = [0]
    p = 0
    arr_index = 0
    while_loop = []

    while p < len(program):
        if program[p] == PLUS:
            arr[arr_index] += 1
            if arr[arr_index] == 256:
                arr[arr_index] = 0
        elif program[p] == MINUS:
            arr[arr_index] -= 1
            if arr[arr_index] == -1:
                arr[arr_index] = 255
        elif program[p] == RIGHT:
            arr_index += 1
            if arr_index == len(arr):
                arr.append(0)
        elif program[p] == LEFT:
            arr_index -= 1
            if arr_index < 0:
                arr.insert(0, 0)
                arr_index += 1
        elif program[p] == PRINT:
            print(chr(arr[arr_index]), end="")
        elif program[p] == INPUT:
            arr[arr_index] = int(input())
        elif program[p] == START_LOOP:
            while_loop.append(p)
        elif program[p] == END_LOOP:
            if arr[arr_index] != 0:
                p = while_loop[-1]
            else:
                del while_loop[-1]
        p += 1

def turnFileIntoProgram(fileLoc):
    program = []
    with open(fileLoc, 'r') as f:
        code = f.read()

        for l in code:
            if l == '+':
                program.append(plus())
            if l == '-':
                program.append(minus())
            if l == '.':
                program.append(printt())
            if l == ',':
                program.append(inputt())
            if l == '>':
                program.append(right())
            if l == '<':
                program.append(left())
            if l == '[':
                program.append(startLoop())
            if l == ']':
                program.append(endLoop())
    
    return program

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        assert False, "No arguments provided."
    elif args[0] == "sim":
        if len(args) == 1:
            assert False, "No file provided."
        simulateProgram(turnFileIntoProgram(args[1]))
    elif args[0] == "com":
        if len(args) == 1:
            assert False, "No file provided."
        compileProgram(turnFileIntoProgram(args[1]), args[2])
    else:
        assert False, "Argument unknown."
