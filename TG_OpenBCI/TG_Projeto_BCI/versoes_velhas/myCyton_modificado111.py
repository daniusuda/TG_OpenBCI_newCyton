import numpy as np
import cyton
import time
import serial
import struct
import numpy as np
import time
import timeit
import atexit
import logging
import threading
import sys
import pdb
import glob

#class myclass:
#    name = ''
#   def __init__(self):
#        self.name = 'name'

#manter o cyton na mesma pasta para que consiga encontrar
#string inicial para montar o comando desejado
#variaveis globais
stringxX = ['x', 0, 0, 0 , 0, 0, 0, 0, 'X']
n = 0

class myCyton(cyton.OpenBCICyton):
    
    
    def __init__(self,id=0,port=None, filter_data=True,timeout=None):
        cyton.OpenBCICyton.__init__(self,port=port, baud=115200, filter_data=filter_data, scaled_output=True, daisy=False, aux=False, impedance=False, log=False, timeout=timeout)
        #self.nChannels=8
        #nao pareceu ter correspondencia com outros arquivos
        self.sample=[0]*8
        self.ser.write(b'b')
        self.streaming = True
        time.sleep(0.5)
        
        #Initialize check connection
        self.check_connection()
     
    def readSample(self):
        # read current sample
        sample = self._read_serial_binary()
        if sample.channel_data[0]!=0.0:
            self.sample = sample.channel_data
        return self.sample
    
    def stringTest(self):
        s = x0000000X
        self.ser.write(b's')
        
            
    def myStopStreaming(self):
        self.stop()
        self.streaming = False
        

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
        for x in range(0, 1,len(s)):
            print ('O canal está configurado como:')
            print ('Novas configurações dos canais:\n', n, c, b)
            print ('Canais escolhidos: ')
        return

    #pode fazer um exibidor da configuração nova do canal, pode ser com o enviar ou algum complemento
    #dentro dele
    
    #Comandos disponíveis em: https://docs.openbci.com/OpenBCI%20Software/04-OpenBCI_Cyton_SDK#openbci-cyton-sdk-firmware-v300-new-commands-get-version
   
    #Comandos Firmware 1.0.0
        #Desligar Canais (Turn Channels OFF): 1 2 3 4 5 6 7 8
        #Ligar Canais (Turn Channels ON): ! @ # $ % ^ & *  
        #Sinais de Teste (Test Signal Control Commands): 0 - = p [ ]
        #Configuração de Canais (Channel Setting Commands): x (CHANNEL, POWER_DOWN, GAIN_SET, INPUT_TYPE_SET, BIAS_SET, SRB2_SET, SRB1_SET) X 
        #Configuração de Canal Padrão(Default Channel Settings): d
        #Relatório de Configuração Padrão: D
        #Impedância do Canal (LeadOff Impedance Commands): z (CHANNEL, PCHAN, NCHAN) Z
        #Comandos do Cartão SD (SD card Commands):
        #A S F G H J K L
        #Parar o logging e fechar o arquivo SD: j     
        #Comandos de Stream de Dados (Stream Data Commands): 
        #b :começa o streaming de dados
        #s :interrompe o streaming de dados    
        #Comandos Sortidos:
        #? :lê e faz relatório sobre todas as configurações do ADS1299 e o LIS3DH
        #ADS1299 é um conversor AD especializado para medidas de biopotencial
        #LIS3DH é um acelerômetro linear de três eixos
        #v :"soft reset" da placa Cyton
    
    #Comandos Daisy/16 Canais
        #Desligar Canais (Turn Channels OFF):
        #q w e r t y u i :desligam respectivamente os canais de 9 a 16, na ordem
    
        #Ligar Canais (Turn Channels ON):
        #Q W E R T Y U I :ligam respectivamente os canais de 9 a 16, na ordem
    
        #Número de Canais(Select maximum channel number):
        #c :Habilita somente os canais 1 a 8
        #C :Habilita todos os canais de 1 a 16
    
    #Comandos Firmware 2.0.0
        # Marcação do Tempo (Time Stamping):
        #< :Inicia o time stamping, sincronizando o Driver e o Host.
        #> :Para o time stamping.
        
        #Número de Rádio do Canal (Get Radio Channel Number):
        #0xF0 0x00: retorna a falha ou sucesso, e o valor do host, mais o do aparelho no caso de sucesso.
        #Configurar Número do Canal de Rádio (Set Radio System Channel Number):
        #0xF0 0x01 0x07: retorna a falha ou sucesso, sucesso se o host e o aparelho estiverem com o mesmo valor; também retorna em HEX o valor do canal.
        #O 0x07 é opcional, para determinar o canal, de 1 a 25 em HEX. De 0x01 a 0x19
        #Configurar Sobreposição do Canal de Rádio (Set Host Radio Channel Override):
        #0xF0 0x02 0x01: retorna falha ou sucesso, força a troca de canal do Host para o canal(opcional). De 0x01 a 0x19
        def radioGet(self):
            self.ser.write(b'0xF0 0x00')
        def radioSet(self):
            self.ser.write(b'0xF0 0x01 0x07') 
        def radioOver(self):
            self.ser.write(b'0xF0 0x02 0x01')
            
        #Obter Poll Time de Rádio(Radio Get Poll Time):
        #0xF0 0x03: retorno de pool time, pode significar erros e está associado com as capacidades do sistema. Retornado em HEX o poll time.
        #Configurar Poll Time de Rádio(Radio Get Poll Time):
        #0xF0 0x04 0x40:a terceira opção determina o poll time em HEX, são aceitos valores de 0 a 255, em ms. Padrão é de 80ms.
        def radioPoll(self):
            self.ser.write(b'0xF0 0x03')
        def radioPollSet(self):
            self.ser.write(b'0xF0 0x04')
               
        #Configurar o Baud Rate para o Padrão do Rádio do Host (Radio Set HOST to Driver Baud Rate to Default):
        #0xF0 0x05: configura o Baud Rate para 115200Hz.
        #Configurar o Baud Rate para Modo de Alta-Velocidade (Radio Set HOST to Driver Baud Rate to High-Speed mode):
        #0xF0 0x06: configura o Baud Rate pra 230400Hz.
        #Configurar o Baud Rate para Modo de Hiperalta-Velocidade (Radio Set HOST to Driver Baud Rate to Hyper-Speed mode):
        #0xF0 0x0A: configura o Baud Rate pra 921600Hz.
        def radio115k(self):
            self.ser.write(b'0xF0 0x05')
        def radio230k(self):
            self.ser.write(b'0xF0 0x06')
        def radio921k(self):
            self.ser.write(b'0xF0 0x0A')
        
        #Relatório do Sistema de Rádio:
        #0xF0 0x07: checa o status do sistema de rádio, confirma ou nega se está operante.
         def radioRelat(self):
            self.ser.write(b'0xF0 0x07')
    
    
    #Comandos Firmware 3.0.0
        
        #Taxa de Aquisição (Sample Rate):
        #~0 : configura a taxa de aquisição, o 0 no comando pode ser alterado para os valores 0/1/2/3/4/5/6/~
        #Os valores correspondem às taxas: 16000Hz / 8000Hz / 4000Hz / 2000Hz / 1000Hz / 500Hz / 250Hz / Obter a taxa de aquisição atual
         def sample16k(self):
            self.ser.write(b'~0')
         def sample8k(self):
            self.ser.write(b'~1')
         def sample4k(self):
            self.ser.write(b'~2')
         def sample2k(self):
            self.ser.write(b'~3')
         def sample1k(self):
            self.ser.write(b'~4')
         def sample500(self):
            self.ser.write(b'~5')
         def sample250(self):
            self.ser.write(b'~6')
         def samplestatus(self):
            self.ser.write(b'~~')
        
        #Modo da Placa (Board Mode):
        #/0 : configura o modo da placa, o 0 no comando pode ser alterado para os valores 0/1/2/3/4//
        #Os valores correspondem as modos: Padrão / Modo Debug / Modo Analógico / Modo Digital / Modo Marcador / Obter o modo de aquisição atual
         def boardModedef(self):
            self.ser.write(b'/0')
         def boardModedebug(self):
            self.ser.write(b'/1')
         def boardModeanalog(self):
            self.ser.write(b'/2')
         def boardModedigital(self):
            self.ser.write(b'/3')
         def boardModemarker(self):
            self.ser.write(b'/4')
         def boardModestatus (self):
            self.ser.write(b'/X') 
        
        
        #Comandos do Shield de Wifi (Wifi Shield Commands):
        #{ : Faz uma tentativa de se sincronizar com shield de Wifi, retorna o sucesso ou falha.
        #} : Tenta remover o shield de Wifi, retorna sucesso ou falha da operação.
        #: : Obtém o status do shield de Wifi, se está presente ou não.
         def WifiShieldAtt(self):
            self.ser.write(b'{')
         def WifiShieldDeatt(self):
            self.ser.write(b'}')
         def WifiShieldStatus(self):
            self.ser.write(b':') 
        
        
         #Obter Versão (Get Version):
         #V : Retorna a versão do Firmware.
        def firmware(self):
           self.ser.write(b'V')
        
    #Adendo
        
        #Caracteres não utilizados: 9 ( ) _ o O f g h k l ‘ “ n N M , . (space)
     