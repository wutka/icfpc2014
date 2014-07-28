import sys

with open(sys.argv[1], 'r') as f:
    data = [l.strip() for l in f.readlines()]
    addr=0
    for line in data:
        if (line[0] != ';'):
            print addr,'\t',line
            addr += 1
        else:
            print line
