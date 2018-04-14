#! /usr/bin/python3

import sys
from collections import Counter

# A possible mine
class Qnode:
    def __init__(self,name,state=None):
        self.name = name
        self.state = state
        self.nnodes = []

    def set(self, state):
        #print("setting qnode ", self.name, state)
        self.state = state
        if self.state == True:
            for n in self.nnodes:
                if n.numleft() > 0:
                    n.set(self)
        else:
            for n in self.nnodes:
                n.unset(self)

# A clear cell with a number
class Nnode:
    def __init__(self,name,number,possibles,qnodes):
        self.name = name
        self.number = number
        self.possibles = [q for q in qnodes.values() if q.name in possibles]
        self.mines = []
        self.safes = []
        for q in self.possibles:
            q.nnodes.append(self)

    def numleft(self):
        return self.number - len(self.mines)

    def possct(self):
        return len(self.possibles)
    
    def set(self, q):
        self.possibles.remove(q)
        self.mines.append(q)
        if self.numleft() == 0:
            while self.possct() > 0:
                qq = self.possibles[0]
                qq.set(False)
    
    def unset(self, q):
        if q in self.possibles:
            self.possibles.remove(q)
            self.safes.append(q)

# given a qnode's name, set it as a mine, then loop through its nnodes
# if a contradiction is found, return None
# if any nnode is found which has only one possible qnode, return it
# otherwise return an nnode with the minimal number of qnodes to check
def step(qname):
    for n in nnodes.values():
        if n.numleft() > 0 and n .possct() == 0:
            print("contradiction")
            return None

    minval = sys.maxsize
    maxval = -1
    for n in nnodes.values():
        if n.possct() == 1:
            #print(n.possibles[0].name)
            return n
        if n.possct() != 0 and n.possct() < minval:
            minval = n.possct()
            minnode = n
        if n.numleft() > maxval:
            maxval = n.numleft()
    if maxval == 0:
        return True
    return minnode


# given a list of qnode names, pop the last, then try to compute a solution
# add it to the set and append it to the output file.  
# If we arrive at a branch point.  Pop the next 
def solve(qname):
    global solutions
    done = False
    while not done:
        qnodes[qname].set(True)
        n = step(qname)
        if n == None:
            print("found contradiction, quitting")
            done = True
        else:
            if n == True:
                mines = [q.name for q in qnodes.values() if q.state == True]
                print("found solution: {}".format(mines))
                solutions.add(tuple(sorted(mines)))
                done = True
            elif n != None:
                #print("found node {0} with numleft = {1:d} and possct = {2:d}" \
                #    .format(n.name, n.numleft(), n.possct()))
                if n.possct() == 1:
                    qname = n.possibles[0].name
                else:
                    possqs = [q.name for q in n.possibles]
                    print("step returned node {0} with possibles:".format(n.name))
                    print(possqs)
                    valid = False
                    while not valid:
                        print("enter one to try or 0 to quit")
                        qname = input(">>> ")
                        if qname == '0':
                            exit(0)
                        if qname in possqs:
                            valid = True

def write_out():
    text = "\n".join([str(sol) for sol in sorted(list(solutions))]) + "\n"
    with open("output.txt",'w') as f:
        f.write("{0:d} solution(s) found.\n".format(len(solutions)))
        f.write(text)
        l = [item for sublist in solutions for item in sublist]
        c = Counter(l)
        f.write("\nNumber of mines in cell summed over all solutions:\n")
        for k in sorted(c.keys()):
            f.write("{0}: {1:d}\n".format(k, c[k]))

def reset():
    global qnodes, nnodes
    nnodes = {}
    lines = text.strip().split("\n")
    qnodes = {name: Qnode(name) for name in lines[0].split(",")}
    for i in range(1,len(lines)):
        name, count, possibles = lines[i].split(",")
        nnodes[name] = Nnode(name,int(count),possibles,qnodes)

if len(sys.argv) != 2:
    print("usage: python3 mines.py <input file name>")
    exit(2)

with open(sys.argv[1],'r') as f:
    text = f.read()

solutions = set()
qnodes = {}
nnodes = {}
reset()
qname = '1'
while qname != '0':
    print("{0:d} solution(s) found.\n".format(len(solutions)))
    valid = False
    while not valid:
        print("qnodes are: {0}".format(", ".join(list(qnodes.keys()))))
        print("enter one to try or 0 to quit")
        qname = input(">>> ")
        if qname == '0':
            write_out()
            exit(0)
        if qname in qnodes.keys():
            valid = True
    write_out()
    reset()
    solve(qname)

# input1.txt represents the following state
# where cells a-h are nnodes (cells with number values)
# and cells i-x are qnodes (cells which may be mines)
######################
#
#  x   i   j   k   l
#  w  1a  1b  2c   m
#  v  1h   0  2d   n
#  u  1g  1f  3c   o
#  t   s   r   q   p
#
######################


