import copy
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
    global ValidData,Sudoku
    i,j = 0,0
    while i != 9 or j!= 0:
        if Sudoku[i][j] == 0:
            Columns = range(1,10)
            Rows = range(1,10)
            Block = range(1,10)
            CheckColum = range(0,9)
            CheckColum.remove(j)
            CheckRow = range(0,9)
            CheckRow.remove(i)
            for cj in CheckColum:
                if Sudoku[i][cj] != 0:
                    Columns.remove(Sudoku[i][cj])
            for ci in CheckRow:
                if Sudoku[ci][j] != 0:
                    Rows.remove(Sudoku[ci][j])
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
                        Block.remove(Sudoku[i+xi][j+yi])
            ValidData[(i,j)] = list(set(Columns).intersection(set(Rows)).intersection(set(Block)))
                        #print i,j,Columns,Rows,Block
        j += 1
        if j == 9:
            i += 1
            j = 0
def GetZeroPos():
    i,j = 0,0
    for i in range(0,9):
        for j in range(0,9):
            if Sudoku[i][j] == 0:ZeroPos.append((i,j))

def Cut(pos,i):
    x,y = pos
    lx,ly = range(0,9),range(0,9)
    lx.remove(x)
    ly.remove(y)
    for cy in ly:
        if Sudoku[x][cy] == 0:
            if i in ValidData[(x,cy)]:
                if len(ValidData[(x,cy)]) == 1:
                    return False
                else:
                    ValidData[(x,cy)].remove(i)
    for cx in lx:
        if Sudoku[cx][y] == 0:
            if i in ValidData[(cx,y)]:
                if len(ValidData[(cx,y)]) == 1:
                    return False
                else:
                    ValidData[(cx,y)].remove(i)
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
                if i in ValidData[(x+xi,y+yi)]:
                   if len(ValidData[(x+xi,y+yi)]) == 1:
                       return False
                   else:
                        ValidData[(x+xi,y+yi)].remove(i)
    return True
def CalcuSolved(n):
    global ValidData,Sudoku,Solved
    if n == len(ZeroPos) - 1:
        Solved = copy.deepcopy(Sudoku)
        return
    else:
        ValidDataList = copy.copy(ValidData[ZeroPos[n]])
        for i in ValidDataList:
            Sudoku[ZeroPos[n][0]][ZeroPos[n][1]] = i
            TmpValidData = copy.deepcopy(ValidData)
            if Cut(ZeroPos[n],i):
               CalcuSolved(n + 1)
            Sudoku[ZeroPos[n][0]][ZeroPos[n][1]] = 0
            ValidData = copy.deepcopy(TmpValidData)
        #return Sudoku
initSudoku(Test)
CalcuValiData()
GetZeroPos()
CalcuSolved(0)
for i in range(0,9):
    for j in range(0,9):
        print Solved[i][j],
    print 
