# ICFP Contest 2014

## O Caml, My Caml team

Team Members:
Mark Wutka, Nashville TN, USA


## Overview

This solution consists of a compiler that compiles a Lisp program into a GCC
machine binary, a python program to display addresses next to each GCC
instruction, and the source code for the lambdaman program. 

To build the compiler, you need the Jane Street core package installed.
If you have opam installed, you should be able to do "opam install core"

Then, to build the compiler, you can just type:
corebuild -use-menhir compiler.byte

The -use-menhir flag refers to the menhir package that replaces ocamlyacc.

To run the compiler, just do:
compiler.byte lambdaman.glisp

It should generate lambdaman.gcc in the same directory as the source file.


The compiler uses comments in the generated instructions to go back and
fill in symbol references, and it is handy to have them there when analyzing
why the program failed. I wrote show\_addresses.py to take the GCC file and
annotate it with the addresses of each instruction, skipping any comment
lines. To run it, just do:
python show\_addresses.py lambdaman.gcc


## Lambdaman Program

The lambdaman program isn't particularly smart, it is basically just a greedy
algorithm that tries to avoid ghosts. At the beginning of each turn, it
computes the distances from the lambdaman to each non-wall location on the
board. This is done by the get-distance-map-for-loc-avoid-ghosts function.
It creates a map similar to the game map containing a distance and an initial
direction for each non-wall. The lambdaman location has a distance and dir of
0. For the squares directly adjacent to the lambdaman, it excludes computing
paths through any that are occupied by a ghost, or will be occupied by
a ghost on the next turn. For these adjacent squares, it stores a distance
of 1 and the direction taken to get to that square. From there, the program
computes all the squares that are n+1 squares away from the lambdaman by
looking at the squares adjacent to those that are n squares away, and any that
don't have an assigned distance are given a distance of n+1, and the direction
stores in the n-distance square the it was adjacent to (that is, the direction
is always the direction the lambdaman has to head in this turn to get there).

If the ghosts are frightened and will be for at least another turn, they
aren't considered when planning out the paths.

Once the distances are computed, the lambdaman looks for the closest square
that has something to eat. The fruit is included in the calculation if the time
for it to remain is greater than the distance away it is.

It turns out that the fruit calculation had a bug where the Lambdaman could get
stuck on the fruit square. I also think the logic for avoiding ghosts could have
been better by anticipating direction changes.


## Glisp Compiler

The compiler code consists of 4 files:
compiler.ml - The driver that opens the input and output files and then
              starts the parser
lexer.mll   - The ocamllex lexer
parser.mly  - The menhir (ocamlyacc) parser
glisp.ml    - Takes the parse tree generated by the parser and spits out
              GCC instructions. It generates the initial list of instructions,
              then when they have all been written, goes back through and
              fills in addresses for function symbols

There is some support for tail-recursion in the compiler, but I'm not sure
it will always generate correct code. Specifically, I have to explicitly
declare that a function is tail-recursive (with defun-tail) and any SEL
instructions in a tail-recursive function are converted to TSEL. It really
needs to be smart enough to only use TSEL when there should be no return.

The compiler does support LET, but not LET*. I occasionally wished for LET*,
but not badly enough to implement it. Having LAMBDA was a huge help. I didn't
implement COND, but did implement IF (IF test true-statement false-statement).
I also included BEGIN so you could do multiple statements in an IF when needed
(I ended up not using it. It was also handy to implement QUOTE (') and LIST
to generate lists on-the-fly. The lambdaman code has a number of these
commented out that were used for testing in the CPU simulator.

I wish I had implemented a stricter compiler, it would have saved me a lot
of headaches, but I'm not sure I could have done it within the timeframe.
It would have also been helpful to have the compiler do arity checking on
function calls - that was my biggest source of errors. Every time I thought
about implementing it, I realized I wanted it to spit out line numbers and
I didn't feel like I had the time to go back and propagate that information.
In hindsight, the amount of time I spent tracking down these types of errors
was longer than it would have taken to implement that simple check.
