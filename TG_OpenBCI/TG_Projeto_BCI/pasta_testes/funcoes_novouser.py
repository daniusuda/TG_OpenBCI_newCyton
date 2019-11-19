#string inicial para montar o comando desejado
stringxX = ['x', 0, 0, 0 , 0, 0, 0, 0, 'X']

def selec_Canal(n):
    n = int(input('Digite o canal que deseja configurar\n'))

    if (n > 0 and n < 9):
         stringxX[1] = [n]
         print (stringxX)
    else:
         print ('número não possível de canal')
    return

def ligar_Canal(c):
        c = int(input('ligar ou não? 0/1\n'))
        stringxX[2] = [c]
        print('Canal configurado', c)
        return
    
def escolher_Ganho(b):
        b = int(input('Digite o ganho do canal:bias=0/1/2/3/4/5/6 (G=1/2/3/4/6/12/24)\n'))
        ganho = [1,2,3,4,6,12,24]
        stringxX[3] = ganho[b]
        #bias = [0,1,2,3,4,5,6]
        print('Ganho de', b) 
        return
        
def escolher_Input(i):
        i = str(input('Digite o tipo de input:normal,curto,BIAS,fonte,temperatura,sinalteste,BIASpos,BIASneg\n'))
        inp = ['normal','curto','BIAS','fonte','temperatura','sinalteste','BIASpos','BIASneg']
        pos = inp.find[i]
        stringxX[4] = pos  
        print('Tipo de input escolhido', i)
        return

def ativar_BIAS(bi):
        bi = int(input('ligar ou não(BIAS)? 0/1\n'))
        stringxX[5] = [bi]
        print('BIAS configurado', bi)
        return
    
def ativar_SRB2(s1):
        s1 = int(input('ligar ou não(SRB2)? 0/1\n'))
        stringxX[6] = [s1]
        print('BIAS configurado', s1)
        return
    
def ativar_SRB1(s2):
        bi = int(input('ligar ou não(SRB1)? 0/1\n'))
        stringxX[7] = [s2]
        print('BIAS configurado', s2)
        return

    
def add_fila()
    #adiciona à fila em string do tipo: x0000000Xx0000000Xx0000000X...
    #laço em for para tornar todos os elementos da lista em string
    # sem a conversão não é possível utilizar o .join que é aplicável somente a strings
    #o .join torna, por exemplo, ['x', '0', '0', '0', '0', '0', '0', '0','X'] em x0000000X
    for i in range(0, n*8):
         nConfigCanais[i] = str(nConfigCanais[i])
         stringJunta = ''.join(nConfigCanais)
    #junta todas os valores da lista em uma única string, é o formato aceito pela placa
    #sem espaços entre as configurações
    stringTemp= stringTemp+stringJunta
    stringxX = ['x', 0, 0, 0, 0, 0, 0, 0, 'X']
    return

def enviar()
    s = stringTemp
    stringTemp = ''
    print (s)
    print ('Novas configurações dos canais:\n', n, c, b)
    print ('Canais escolhidos: ')
    return
