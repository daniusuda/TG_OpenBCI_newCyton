import numpy as np
import cyton
import time

#manter o cyton na mesma pasta para que consiga encontrar
#string inicial para montar o comando desejado
#variaveis globais
stringxX = ['x', 0, 0, 0 , 0, 0, 0, 0, 'X']
n = 0

def selec_Canal():
    n = int(input('Digite o canal que deseja configurar\n'))

    if (n > 0 and n < 9):
         stringxX[1] = [n]
         print (stringxX)
    else:
        #o número máximo de canais é 8
         print ('número não possível de canal')
    return

def ligar_Canal():
        c = int(input('ligar ou não? 0/1\n'))
        stringxX[2] = [c]
        print('Canal configurado', c)
        print (stringxX)
        return
    
def escolher_Ganho():
        b = int(input('Digite o ganho do canal:bias=0/1/2/3/4/5/6 (G=1/2/3/4/6/12/24)\n'))
        ganho = [1,2,3,4,6,12,24]
        stringxX[3] = ganho[b]
        #bias = [0,1,2,3,4,5,6]
        print('Ganho de', b)
        print (stringxX)
        return
        
def escolher_Input():
        print('Escolha o tipo de input: normal,curto,BIAS,fonte,temperatura,sinalteste,BIASpos,BIASneg\n')
        i = int(input('1 a 8 tipos\n'))
        inp = [1,2,3,4,5,6,7,8]
        #i = str(input('Digite o tipo de input:normal,curto,BIAS,fonte,temperatura,sinalteste,BIASpos,BIASneg\n'))
        #inp = ['normal','curto','BIAS','fonte','temperatura','sinalteste','BIASpos','BIASneg']
        pos = inp[i]
        stringxX[4] = pos  
        print('Tipo de input escolhido', i)
        print (stringxX)
        return
    
def ativar_BIAS():
        bi = int(input('ligar ou não(BIAS)? 0/1\n'))
        stringxX[5] = bi
        print('BIAS configurado', bi)
        print (stringxX)
        return
    
def ativar_SRB2():
        s1 = int(input('ligar ou não(SRB2)? 0/1\n'))
        stringxX[6] = s1
        print('BIAS configurado', s1)
        print (stringxX)
        return
    
def ativar_SRB1():
        bi = int(input('ligar ou não(SRB1)? 0/1\n'))
        stringxX[7] = s2
        print('BIAS configurado', s2)
        print (stringxX)
        return

#stringxX pode ser alterado manualmente
  
def add_fila():
    #adiciona à fila em string do tipo: x0000000Xx0000000Xx0000000X...
    #laço em for para tornar todos os elementos da lista em string
    # sem a conversão não é possível utilizar o .join que é aplicável somente a strings
    #o .join torna, por exemplo, ['x', '0', '0', '0', '0', '0', '0', '0','X'] em x0000000X
    for i in range(0, n*8):
         nConfigCanais[i] = str(nConfigCanais[i])
         stringJunta = ''.join(nConfigCanais)
    #junta todas os valores da lista em uma única string, é o formato aceito pela placa
    #sem espaços entre as configurações
    stringTemp = ''
    stringTemp = stringTemp + stringJunta
    stringxX = ['x', 0, 0, 0, 0, 0, 0, 0, 'X']
    return

def enviar():
    s = stringTemp
    self.ser.write(b's')
    #self.ser.write(b'b') é para escrever para a placa
    #self.streaming = True é para iniciar o streaming
    print (s)
    for x in range(1, 1, len(s)):
        print ('O canal está configurado como:')
        print ('Novas configurações dos canais:\n', n, c, b)
        print ('Canais escolhidos: ')
    return

#pode fazer um exibidor da configuração nova do canal, pode ser com o enviar ou algum complemento
#dentro dele