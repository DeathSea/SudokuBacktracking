import copy
import math
Sudoku = [
[0,0,0,0,0,0,0,0,0],#0
[0,0,0,0,0,0,0,0,0],#1
[0,0,0,0,0,0,0,0,0],#2
[0,0,0,0,0,0,0,0,0],#3
[0,0,0,0,0,0,0,0,0],#4
[0,0,0,0,0,0,0,0,0],#5
[0,0,0,0,0,0,0,0,0],#6
[0,0,0,0,0,0,0,0,0],#7
[0,0,0,0,0,0,0,0,0],#8
]
Solved = []
ValidData = {
    #(0,0):[],
}
ZeroPos = []
Test = [
4,7,9, 0,0,0, 0,6,0,
0,1,0, 7,0,4, 0,0,0,
0,0,3, 9,0,0, 0,0,0,

0,0,0, 0,2,0, 0,5,0,
7,0,0, 3,0,1, 0,0,0,
0,0,0, 0,0,0, 4,0,2,

0,0,0, 0,5,0, 1,0,3,
1,0,0, 0,0,7, 8,2,0,
8,0,0, 0,0,6, 0,7,0
]
def initSudoku(Matrix):
    #globals Sudoku
    global Sudoku
    i,j = 0,0
    for item in Matrix:
        Sudoku[i][j] = item
        if j == 8:
            i += 1
            j = -1
        j += 1
def CalcuValiData():
    global ValidData,Sudoku,ZeroPos
    i,j = 0,0
    while i != 9 or j!= 0:
        if Sudoku[i][j] == 0:
            ZeroPos.append((i,j))
            ThisValidData = 0b001111111110
            CheckColum = [0,1,2,3,4,5,6,7,8]
            CheckColum.remove(j)
            CheckRow = [0,1,2,3,4,5,6,7,8]
            CheckRow.remove(i)
            for cj in CheckColum:
                if Sudoku[i][cj] != 0:
                    ThisValidData = ThisValidData & ~(1 << Sudoku[i][cj])
            for ci in CheckRow:
                if Sudoku[ci][j] != 0:
                    ThisValidData = ThisValidData & ~(1 << Sudoku[ci][j])
            #Block;
            if i%3 == 0:
                CheckBlockx = [+1,+2]
            elif i%3 == 1:
                CheckBlockx = [-1,+1]
            else:
                CheckBlockx = [-2,-1]
            if j%3 == 0:
                CheckBlocky = [+1,+2]
            elif j%3 == 1:
                CheckBlocky = [-1,+1]
            else:
                CheckBlocky = [-2,-1]
            for xi in CheckBlockx:
                for yi in CheckBlocky:
                    if Sudoku[i+xi][j+yi] != 0:
                        ThisValidData = ThisValidData & ~(1 << Sudoku[i+xi][j+yi])
            ValidData[(i,j)] = ThisValidData
                        #print i,j,Columns,Rows,Block
        j += 1
        if j == 9:
            i += 1
            j = 0
#def GetZeroPos():
#    i,j = 0,0
#    for i in range(0,9):
#        for j in range(0,9):
#            if Sudoku[i][j] == 0:ZeroPos.append((i,j))

def Cut(pos,i):
    ispow2 = lambda x:not (x & x - 1)
    x,y = pos
    lx,ly = range(0,9),range(0,9)
    lx.remove(x)
    ly.remove(y)
    for cy in ly:
        if Sudoku[x][cy] == 0:
            if 1 << i & ValidData[(x,cy)] != 0:
                if ispow2(ValidData[(x,cy)]):
                    return False
                else:
                    ValidData[(x,cy)] &= ~(1 << i)
    for cx in lx:
        if Sudoku[cx][y] == 0:
            if 1 << i & ValidData[(cx,y)] != 0:
                if ispow2(ValidData[(cx,y)]):
                    return False
                else:
                    ValidData[(cx,y)] &= ~(1 << i)
    if x%3 == 0:
        CheckBlockx = [+1,+2]
    elif x%3 == 1:
        CheckBlockx = [-1,+1]
    else:
        CheckBlockx = [-2,-1]
    if y%3 == 0:
        CheckBlocky = [+1,+2]
    elif y%3 == 1:
        CheckBlocky = [-1,+1]
    else:
        CheckBlocky = [-2,-1]
    for xi in CheckBlockx:
        for yi in CheckBlocky:
            if Sudoku[x+xi][y+yi] == 0:
                if 1 << i & ValidData[(x+xi,y+yi)] != 0:
                   if ispow2(ValidData[(x+xi,y+yi)]):
                       return False
                   else:
                        ValidData[(x+xi,y+yi)] &= ~(1 << i)
    
    return True
def CalcuSolved(n):
    global ValidData,Sudoku,Solved

    if n == len(ZeroPos):
        Solved .append( copy.deepcopy(Sudoku))
        return
    else:
        ThisValidData = ValidData[ZeroPos[n]]
        shift = 1
        while shift != 10:
            if ((ThisValidData >> shift & 1) == 0):
                shift += 1
                continue
            i = shift
            Sudoku[ZeroPos[n][0]][ZeroPos[n][1]] = i
            TmpValidData = copy.copy(ValidData)
            if Cut(ZeroPos[n],i):
                CalcuSolved(n + 1)
            Sudoku[ZeroPos[n][0]][ZeroPos[n][1]] = 0
            ValidData = copy.copy(TmpValidData)
            shift += 1
        #return Sudoku
initSudoku(Test)
CalcuValiData()

CalcuSolved(0)
print "there is {0} solve(s) total ,show like this:".format(len(Solved))
for solve in Solved:
    for i in range(len(solve)):
        for j in range(len(solve[i])):
            print solve[i][j],
        print 
    print "-"*48
#key = ValidData.keys()
#key.sort()
#print len(key)
#for i in key:
#    print i,bin(ValidData[i])[2:].zfill(10)
