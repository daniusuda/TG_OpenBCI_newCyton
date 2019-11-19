#string inicial para montar o comando desejado
stringxX = ['x', 0, 0, 0, 0, 0, 0, 0, 'X']
def selec_Canais:
    n = int(input('Digite o número de canais que deseja configurar\n'))

    if (n > 0 and n < 9):
         nConfigCanais = n*stringxX 
         print (nConfigCanais)
    else:
         print ('número não possível de canais')
    return

def string_para_list(string):     
    string = r
    r = r.replace(" ", "")
    #Transforma a string em lista
    transfEmLista  = [int(i) for i in str(r)]
    print(transfEmLista)
    return

def ligar_Canais(n):
     n = int(input('Digite os canais que deseja ligar\n'))
     string_para_list(n)
     for i in range(1, len(n)):
         nConfigCanais[1] = transfEmLista[0]
         nConfigCanais[2] = 0
         nConfigCanais[1+i*8] = transfEmLista[i]
         nConfigCanais[2+i*8] = 0
         print('Canais ligados em', transfEmLista)
     return
    
def desligar_Canais(n):
     n = int(input('Digite os canais que deseja desligar\n'))
     string_para_list(n)
     for i in range(1, len(n)):
         nConfigCanais[1] = transfEmLista[0]
         nConfigCanais[2] = 1
         nConfigCanais[1+i*8] = transfEmLista[i]
         nConfigCanais[2+i*8] = 1
         print('Canais desligados em', transfEmLista)
         return
  
def escolher_Ganho(bias):
    bias = int(input('Digite os canais que deseja desligar\n'))
    for i in range(1, len(n)):
         nConfigCanais[1] = transfEmLista[0]
         nConfigCanais[2] = 1
         nConfigCanais[1+i*8] = transfEmLista[i]
         nConfigCanais[2+i*8] = 1
         print('Canais desligados em', transfEmLista)
         return

def ativar_BIAS(bias):
    nConfigCanais[]
a1 = 2
 print(a1)
 return
     

#Para já manter ligadas as conexões
for i in range(1, n):
    nConfigCanais[1] = transfEmLista[0]
    nConfigCanais[2] = 0
    nConfigCanais[1+i*8] = transfEmLista[i]
    nConfigCanais[2+i*8] = 0
    parar = input('Parar configuração?')
if (parar = 'sim' or 's' or 'y'):
     print ('Digite os canais que deseja apicar o BIAS')

    
     
#laço em for para tornar todos os elementos da lista em string
# sem a conversão não é possível utilizar o .join que é aplicável somente a strings
#o .join torna, por exemplo, ['x', '0', '0', '0', '0', '0', '0', '0','X'] em x0000000X
for i in range(0, n*8):
     nConfigCanais[i] = str(nConfigCanais[i])
#junta todas os valores da lista em uma única string, é o formato aceito pela placa
#sem espaços entre as configurações
s = ''.join(nConfigCanais)
print (s)
print ('Novas configurações dos canais:\n')
print ('Canais escolhidos: ')