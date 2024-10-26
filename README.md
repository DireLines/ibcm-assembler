# ibcm-assembler

Assembles a custom assembly language into IBCM, the University of Virginia CS department's own instructional machine language.

Just for fun!

IBCM in-class slides: https://uva-cs.github.io/pdr/slides/07-ibcm.html#/ibcmdesc

IBCM spec: https://github.com/aaronbloomfield/pdr/blob/master/book/ibcm-chapter.pdf

IBCM homepage: https://uva-cs.github.io/pdr/ibcm/index.html

(sadly it looks as though all the browser simulator pages are down)

## example usage:

```
> cat example/fib.ibasm
jmp start # skip around the variables
var i
var s
var N
var one = 1
var zero = 0
start:  readH # read N
        store   N
        load    one
        store   i
        load    zero
        store   s
loop:   load    N
        sub     i
        jmpl    exit
        load    s
        add     i
        store   s
        load    i
        add     one
        store   i
        jmp     loop
exit:   load    s
        printH
        halt
> python3 ibcm-assembler.py example/fib.ibasm
C006 000 jmp start # skip around the variables
0000 001 var i
0000 002 var s
0000 003 var N
0001 004 var one = 1
0000 005 var zero = 0
1000 006 start:  readH # read N
4003 007         store   N
3004 008         load    one
4001 009         store   i
3005 00A         load    zero
4002 00B         store   s
3003 00C loop:   load    N
6001 00D         sub     i
E016 00E         jmpl    exit
3002 00F         load    s
5001 010         add     i
4002 011         store   s
3001 012         load    i
5004 013         add     one
4001 014         store   i
C00C 015         jmp     loop
3002 016 exit:   load    s
1800 017         printH
0000 018         halt

>
```

note: only the first four characters of each line are the actual IBCM program, the rest is just a comment so you can see what line the instruction corresponded to in the original program, as well as the hex address of the line within program memory.

## ibasm

IBCM is a machine language and not an assembly language, so I had to come up with names for the assembly instructions which correspond to the machine instructions.

Most names come from the examples in IBCM slides:

- https://uva-cs.github.io/pdr/slides/07-ibcm.html#/4/10
- https://uva-cs.github.io/pdr/slides/07-ibcm.html#/5/3

I added the ability to declare and optionally initialize variables with the keyword `var`:

```
var i  #default to 0
var one = 1  #initial state of cell is 1
var sixteen = 0x10  #hexadecimal is also supported
load i  #now we can refer to the variable names instead of addresses
add sixteen
store i
halt
```

I also added labels:

```
var i
var one = 1
var sixteen = 16
loop: load i
      add one
      store i
      printH
      sub sixteen
      jmpl loop  #now "loop" refers to the label's address
halt
```
