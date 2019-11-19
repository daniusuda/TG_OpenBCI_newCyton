stringxX = ['X','1','2']
stringxX = ['x', 0, 0, 0, 0, 0, 0, 0, 'X']
print(stringxX)
for i in range(0,8):
    stringxX[i] = str(stringxX[i])
print(stringxX)
stringJoin = ''.join(stringxX)
print(stringJoin, 'stringjoin')
stringSer = ''.join(['b',stringJoin])
print(stringSer)
for i in range(0,7):
            stringB = ['a','b','c','d','e','f','g','h']
            stringB[i+1] = stringJoin[i]
            stringB[0] = 'b'
print(stringB)