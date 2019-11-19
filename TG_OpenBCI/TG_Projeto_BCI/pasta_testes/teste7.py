import numpy as np
import cyton
import time

#manter o cyton na mesma pasta para que consiga encontrar
#string inicial para montar o comando desejado
#variaveis globais
stringxX = ['x', 0, 0, 0 , 0, 0, 0, 0, 'X']
stringTemp = ''

def selec_Canal():
    n = int(input('Digite o canal que deseja configurar\n'))

    if (n > 0 and n < 9):
         stringxX[1] = [n]
         print (stringxX)