#!/usr/bin/env python
# coding: utf-8

# In[66]:


#Importando as bibliotecas numéricas e de plotagem
import numpy as np
import matplotlib.pyplot as plt
import struct


# In[67]:


#Gerando a matriz com os dados, á partir do arquivo de texto da placa Cyton
#dtype = string para ser posteriormente traduzido de hexadecimal para float
#delimiter para remover as vírgulas do arquivo de texto
#usecols para selecionar somente as 8 colunas que correspondem aos 8 canais
#skipfooter para pular o rodapé, com informações além dos canais, o que interfere na utilização da função;
#algumas das últimas linhas podem acabar com menos elementos que 8, portanto foram removidas algumas linhas além do rodapé
#pode ser alterado o usecols se quiser obter os dados do acelerômetro, são os últimos 3 valores(x,y,z)
#para as colunas [10,11,12] os valores do acelerômetro, a 50Hz.
datahex = np.genfromtxt("OBCI_AF.txt", dtype=str,delimiter=',',usecols=np.arange(1,9), skip_footer = 13, filling_values = '8000000')
#datahex = np.genfromtxt("OBCI_AF.txt", dtype=str,delimiter=',',usecols=np.arange(1,9), skip_footer = 13)


# In[68]:


#.shape para obter as dimensões de data, para então ser utilizado para uma varredura abaixo
#irá transformar os valores de hexadecimal para decimal, float
len(datahex)
a = datahex.shape
#a[0]
# print(a[0])
print(datahex)


# In[69]:


#data2 é inicialmente um vetor de zeros, com as mesmas dimensões e número de elementos que a matriz data
#então realiza a conversão utilizando a função .fromhex()
data2 = np.zeros(len(datahex)*8,dtype=np.dtype('>i4')).reshape(a[0],a[1])
dat32 = np.zeros(len(datahex)*8,dtype=np.dtype('>i4')).reshape(a[0],a[1])
for i in range(0,a[0]):
    for j in range(0,a[1]):
        
                #OS DADOS SÃO BIG ENDIAN/MSB NA ESQUERDA, 24 BITS SIGNED
        #CADA DADO SERÁ PROCESSADO DE 24-BITS PARA 32-BITS PARA ESTAR CONDIZENTE COM O FATOR DE ESCALA FORNECIDO
        #E OBTIDO EXPERIMENTALMENTE


        bytetext =  bytearray.fromhex(datahex[i,j])
        unpacked = struct.unpack('3B',bytetext)
        print(unpacked)
        #Determinando o sinal, analisando o primeiro byte á esquerda da sequência de 3 bytes (24 bits), incluindo um prefixo
        #para determinar o prefixo a ser adicionado ao converter para 32 bits.
        if(unpacked[0]>127):
            pre_fix = bytes(bytearray.fromhex('FF'))
        else:
            pre_fix = bytes(bytearray.fromhex('00'))
#         print(bytetext)
#         print('bytetext s prefixo^^')
        bytetext = pre_fix + bytetext
#         print(bytetext)
#         print('bytetext com prefixo^^')
#         print(pre_fix)
#         print('pre_fix^^')
#         print(ab)
#         print('ab^^')


        myInt = struct.unpack('>i', bytetext)[0]
#         print(myInt)
#         print('myint^^')

#Scale Factor (Volts/count) = 4.5 Volts / gain / (2^23 - 1);
#Obtido experimentalmente, o cálculo é fornecido pelo site da OpenBCI.
#Deve alterar o ganho dependendo de qual for utilizado na placa.

        gain = 24
        scaleF = ((4.5/gain)/(2**23-1))
        #Valor em volts do dado após ser convertido com a escala

        bytetextInt = int.from_bytes(bytetext,byteorder='big',signed = True)
        data2[i,j] = bytetextInt*scaleF
        data444 = myInt*scaleF
#         print(data333)
#         print('data333')
#         print(data444)
#         print('data444')


# In[70]:


dt = 1/250
t = np.arange(0,len(data2)*dt,dt)


# In[71]:



plt.figure(figsize = (30,12))

plt.plot(t,data4[:,0],'red')
plt.plot(t,data4[:,1],'darkorange')
plt.plot(t,data4[:,2],'yellow')
plt.plot(t,data4[:,3],'chartreuse')
plt.plot(t,data4[:,4],'aqua')
plt.plot(t,data4[:,5],'royalblue')
plt.plot(t,data4[:,6],'darkviolet')
plt.plot(t,data4[:,7],'fuchsia')
plt.show()

