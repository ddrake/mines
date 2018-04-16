#! /usr/bin/python3
import sys
from collections import Counter

# A possible mine
class Qnode:
    def __init__(self,name,state=None):
        self.name = name
        self.state = state
        self.nnodes = []

    # set the state of a qnode to True (a mine) or False (not a mine)
    # then call the set (or unset) method for all connected Nnodes.
    def set(self, state):
        self.state = state
        if self.state == True:
            for n in self.nnodes:
                if n.numleft() > 0:
                    n.set(self)
        else:
            for n in self.nnodes:
                n.unset(self)

# A clear cell with a number.  Initially, all it's neighbors are 
# "possibles" i.e. possible mines.  As mines are set or unset, 
# possibles are moved to the "mines" or "safes" bins.
class Nnode:
    def __init__(self,name,number,possibles,qnodes):
        self.name = name
        self.number = number
        self.possibles = [q for q in qnodes.values() if q.name in possibles]
        self.mines = []
        self.safes = []
        for q in self.possibles:
            q.nnodes.append(self)

    # the number of remaining mines to identify
    def numleft(self):
        return self.number - len(self.mines)

    def possct(self):
        return len(self.possibles)
    
    # Set a neighboring qnode to a mine by moving it to the
    # "mines" bin.  If our known number of mines equals the
    # the count in our "mines" bin, unset any remaining qnodes.
    # This will have the side effect 
    # of moving them to our "safes" bin.
    def set(self, q):
        self.possibles.remove(q)
        self.mines.append(q)
        if self.numleft() == 0:
            while self.possct() > 0:
                qq = self.possibles[0]
                qq.set(False)
    
    # Set a neighboring qnode to be safe by moving it to the 
    # "safes" bin.
    def unset(self, q):
        if q in self.possibles:
            self.possibles.remove(q)
            self.safes.append(q)

# Given a qnode's name, set it as a mine, then loop through its nnodes
# If a contradiction is found (i.e. all possibles sorted, but the known
# number of mines doesn't match the count of the mines bin) return None.
# If any nnode is found which has only one possible qnode, return it.
# Otherwise return an nnode with the minimal number of qnodes to check.
def step(qname):
    for n in nnodes.values():
        if n.numleft() > 0 and n.possct() == 0:
            return None

    minval = sys.maxsize
    maxval = -1
    for n in nnodes.values():
        if n.possct() == 1:
            return n
        if n.possct() != 0 and n.possct() < minval:
            minval = n.possct()
            minnode = n
        if n.numleft() > maxval:
            maxval = n.numleft()
    if maxval == 0:
        return True
    return minnode

# Initially, each list in the sequence queue will contain exactly one
# element, a qnode that we are going to assume to be a mine.
# Pop a list from the sequence queue, and test if it gives a solution by 
# first stepping through all its elements, then following the trail
# indicated by the step function.  
# If we reach a solution, add the current list to the solution set.  
# If we reach a contradiction, return.  
# If step returns a node with n qnodes to check, create n copies of the
# current list, add them all to the sequence queue, then pop one back off
# as the new current list.
def solve():
    global solutions
    global seq_queue
    curlist = seq_queue.pop()
    print("{0:d} in Queue. Current list is: {1:s}" \
            .format(len(seq_queue), str(curlist)))
    curidx = 0
    done = False
    while not done:
        qname = curlist[curidx]
        curidx += 1
        qnodes[qname].set(True)
        # take a step
        n = step(qname)
        if n == None:
            if debug: 
                print("found contradiction with {}, quitting".format(qname))
                print(curlist)
            done = True
        else:
            if n == True:
                mines = [q.name for q in qnodes.values() if q.state == True]
                if debug: 
                    print("found solution: {}".format(mines))
                    print(curlist)
                solutions.add(tuple(sorted(mines)))
                done = True
            elif curidx >= len(curlist) and n != None:
                if n.possct() == 1:
                    qname = n.possibles[0].name
                    if debug: 
                        print("only one possible cell to check: {}".format(qname))
                        print(curlist)
                    curlist.append(qname)
                else:
                    if debug: 
                        print("several possible cells to check")
                    for q in n.possibles:
                        newlist = curlist[:]
                        newlist.append(q.name)
                        if debug: 
                            print("appending new list to queue", newlist)
                        seq_queue.append(newlist)
                    curlist = seq_queue.pop()
            else:
                if debug: 
                    print("testing the next in the current list")
                    print(curlist)

# Generate an output file, 'output.txt', with all possible solutions and
# the number of solutions in which each given qnode appears as a mine.
def write_out():
    text = "\n".join([str(sol) for sol in sorted(list(solutions))]) + "\n"
    with open("output.txt",'w') as f:
        f.write("{0:d} solution(s) found.\n".format(len(solutions)))
        f.write(text)
        l = [item for sublist in solutions for item in sublist]
        c = Counter(l)
        for q in qnodes.keys():
            if q not in c: c[q]=0
        f.write("\nNumber of mines in cell summed over all solutions:\n")
        for k in sorted(c.keys()):
            f.write("{0}: {1:d}\n".format(k, c[k]))

# Re-read the input file, populating the nnodes and qnodes global lists.
def reset():
    global qnodes, nnodes
    nnodes = {}
    lines = text.strip().split("\n")
    qnodes = {name: Qnode(name) for name in lines[0].split(",")}
    for i in range(1,len(lines)):
        name, count, possibles = lines[i].split(",")
        possibles = possibles[1:-1].split()
        nnodes[name] = Nnode(name,int(count),possibles,qnodes)

# Start Main Program
if len(sys.argv) != 2:
    print("usage: python3 mines.py <input file name>")
    exit(2)

with open(sys.argv[1],'r') as f:
    text = f.read()

# Debug flag enables print statements
debug = False
solutions = set()
qnodes = {}
nnodes = {}
reset()

# Initialize the sequence queue (one qnode in each list)
seq_queue = [[q] for q in qnodes.keys()]

# Loop until the queue becomes empty (todo: estimate max number of passes).
# In each pass, call solve and overwrite the output file.
i = 1
while len(seq_queue) > 0:
    solve()
    print("{0:d} solution(s) found after {1:d} steps.\n" \
            .format(len(solutions),i))
    write_out()
    reset()
    i+=1

# input1.txt represents the following state
# where cells a-h are nnodes (cells with number values)
# and cells A-P are qnodes (cells which may be mines)
# The cell in the middle, an nnode with 0 value, is not relevant.
######################
#
#  P   A   B   C   D
#  O  1a  1b  2c   E
#  N  1h   0  2d   F
#  M  1g  1f  3c   G
#  L   K   J   I   H
#
######################


