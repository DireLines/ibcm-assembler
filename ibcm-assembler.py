#remove comments
def remove_comments(line):
    return line.split("#")[0].strip()
#find labels
#find vars
def extract_labels(lines):
    labels = {}
    newlines = []
    for (i,line) in enumerate(lines):
        split_on_colon = line.split(":")
        if len(split_on_colon) > 1: #label declaration
            label_name = split_on_colon[0].split(" ")[-1]
            rest_of_line = split_on_colon[1]
            if rest_of_line == '':
                rest_of_line = 'nop'
            if label_name in labels:
                print(f"duplicate label detected: {label_name} at both {labels[label_name]} and {i}")
            labels[label_name] = i
            newlines.append(rest_of_line.strip())
            continue
        if line[:2] == "dw" or line[:3] == "var": #variable declaration
            tokens = line.split()[1:]
            label_name = tokens[0]
            init_val = 0
            if len(tokens) > 1:
                init_val = tokens[2]
            if label_name in labels:
                print(f"duplicate label detected: {label_name} at both {labels[label_name]} and {i}")
            labels[label_name] = i
            newlines.append(f"init {init_val}")
            continue
        newlines.append(line)
    return labels,newlines
#convert empty lines to nop
def nop_if_empty(line):
    if line == '':
        return 'nop'
    return line
#translate instructions
opcodes = {
    "halt":0,
    "readH":1,
    "readC":1,
    "printH":1,
    "printC":1,
    "shiftL":2,
    "shiftR":2,
    "rotL":2,
    "rotR":2,
    "load":3,
    "store":4,
    "add":5,
    "sub":6,
    "and":7,
    "or":8,
    "xor":9,
    "not":10,
    "nop":11,
    "jmp":12,
    "jmpe":13,
    "jmpl":14,
    "brl":15,
}
io_codes = {
    "readH":0,
    "readC":1,
    "printH":2,
    "printC":3,
}
shift_rotate_codes = {
    "shiftL":0,
    "shiftR":1,
    "rotL":2,
    "rotR":3,
}
def translate(labels):
    def translate(line):
        tokens = line.split()
        instr_name = tokens[0]
        if instr_name == "init":
            init_val = tokens[1]
            if init_val in labels:
                return f"{labels[init_val]:0>4X}"
            if init_val[:2] == '0x':
                return f"{int(init_val,16):0>4X}"
            return f"{int(init_val):0>4X}"
        if instr_name not in opcodes:
            print(f"unrecognized instruction: {instr_name}")
        opcode = opcodes[instr_name]
        if "read" in instr_name or "print" in instr_name:
            fun_code = io_codes[instr_name] << 6
            return f'{opcode:X}{fun_code:0<3X}'
        if "shift" in instr_name or "rot" in instr_name:
            fun_code = shift_rotate_codes[instr_name] << 6
            shift_amount = int(tokens[1])
            return f'{opcode:X}{fun_code:0<2X}{shift_amount:X}'
        if len(tokens) == 1:
            return f'{opcode:0<4X}'
        label_name = tokens[1]
        if label_name not in labels:
            print(f"unrecognized label in '{line}': {label_name}")
        addr = int(labels[label_name])
        return f'{opcode:0<2X}{addr:0>2X}'
    return translate

#create output file

#turn file into list of lines
import sys
input_filename = sys.argv[1]
input_file = open(input_filename,'r')
original_lines = input_file.readlines()
if len(original_lines) > 0x64:
    print("error: maximum program length exceeded")
    exit()
input_file.close()
#remove comments
lines = list(map(remove_comments, original_lines))
#find labels
#find vars
labels, lines = extract_labels(lines)
#convert empty lines to nop
lines = list(map(nop_if_empty,lines))
#translate instructions
lines = list(map(translate(labels),lines))
#create output
output = ''
for (i,line) in enumerate(lines):
    line_num = f'{i:0>3X}'
    output += f'{line} {line_num} {original_lines[i]}'
print(output)

