"""
newCyton.py
===========

Novo módulo baseado no arquivo cyton.py original do projeto OpenBCI.
 
"""
import cyton
import time
import serial
import struct
import numpy as np
#import matplotlib.pyplot as plt
import time
import timeit
import atexit
import logging
import threading
import sys
import pdb
import glob
#-------------------------------
#copia novouser.py

import argparse  # new in Python2.7
import string
import sys

print("OpenBCI Cyton")

#------------------------------------------------------------------------------   
#sample rate de 250 SPS é fixo para placa Cyton com dongle

SAMPLE_RATE = 250.0  # Hz
START_BYTE = 0xA0  # start of data packet
END_BYTE = 0xC0  # end of data packet
ADS1299_Vref = 4.5  # reference voltage for ADC in ADS1299.  set by its hardware
ADS1299_gain = 24.0  # assumed gain setting for ADS1299.  set by its Arduino code
scale_fac_uVolts_per_count = ADS1299_Vref / \
    float((pow(2, 23) - 1)) / ADS1299_gain * 1000000.
scale_fac_accel_G_per_count = 0.002 / \
    (pow(2, 4))  # assume set to +/4G, so 2 mG

stringxX = ['x', 0, 0, 0 , 0, 0, 0, 0, 'X']
stringxXmaster = [['x',1,0,0,0,0,0,0,'X'],['x',2,0,0,0,0,0,0,'X'],['x',3,0,0,0,0,0,0,'X'],['x',4,0,0,0,0,0,0,'X'],['x',5,0,0,0,0,0,0,'X'],['x',6,0,0,0,0,0,0,'X'],['x',7,0,0,0,0,0,0,'X'],['x',8,0,0,0,0,0,0,'X']]
stringJoin = 'teste'
n = 0

class newCyton(cyton.OpenBCICyton):
        
    def __init__(self, id=0,port=None, filter_data=True,timeout=None):
        
        cyton.OpenBCICyton.__init__(self,port=port, baud=115200,
                                    filter_data=filter_data,
                                    scaled_output=True,
                                    daisy=False,
                                    aux=False,
                                    impedance=False,
                                    log=False,
                                    timeout=timeout)
        
        
        self.streaming = False
        #self.baudrate = baud
        self.timeout = timeout
        if not port:
            port = self.find_port
            self.port = port
      # might be handy to know API
        self.board_type = "cyton"
       
       # if port == "loop://":
            # For testing purposes
            #self.ser = serial.serial_for_url(port, baudrate=baud, timeout=timeout)
       # else:
            #self.ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)
#        sstringxX = ['x', 0, 0, 0 , 0, 0, 0, 0, 'X']
#        stringJoin = 'x0000000X'
#        n = 0
        print("myCytonSerial established...")

        time.sleep(0.5)
        # Initialize 32-bit board, doesn't affect 8bit board
        #realiza soft reset
        #mostra
        self.ser.write(b'v')
        time.sleep(1)
        #colocando a sequência abaixo ele vai comendo caracteres
        #por algum motivo na mensagem, mas parece funcionar.
        #x2000000Xx3000000Xx4000000Xx5000000Xx6000000Xx7000000Xx1000000X')
        
#        print('Inicialização dos 8/16 canais...')
#        
#        time.sleep(1)
#        self.warn('teste_de_warn')      
#        
#        self.ser.write(b'x1000000X')
#        self.print_incoming_text()
#        taime.sleep(0.5)
#        self.ser.write(b'x2000000X')
#        self.print_incoming_text()
#        time.sleep(0.5)
#        self.ser.write(b'x3000000X')
#        self.print_incoming_text()
#        time.sleep(0.5)
#        self.ser.write(b'x4000000X')
#        self.print_incoming_text()
#        time.sleep(0.5)
#        self.ser.write(b'x5000000X')
#        self.print_incoming_text()
#        time.sleep(0.5)
#        self.ser.write(b'x6000000X')
#        self.print_incoming_text()
#        time.sleep(0.5)
#        self.ser.write(b'x7000000X')
#        self.print_incoming_text()
#        time.sleep(0.5)
#        self.ser.write(b'x8000000X')
#        self.print_incoming_text()
#        time.sleep(0.5)
#       
#        self.ser.write(b'?')
        
        #self.print_incoming_text()
        time.sleep(1.0)
        print('Fim da configuração de canais')
        #self.ser.write(b'?')
        #self.print_incoming_text()
        print("Serial write ? mostra as configurações")
        #self.print_incoming_text()
                # wait for device to be ready
        time.sleep(1)
        if port != "loop://":
            self.print_incoming_text()

        self.streaming = False
        self.filtering_data = filter_data
        #self.scaling_output = scaled_output
        # number of EEG channels per sample *from the board*
        self.eeg_channels_per_sample = 8
        # number of AUX channels per sample *from the board*
        self.aux_channels_per_sample = 3
        self.imp_channels_per_sample = 0  # impedance check not supported at the moment
        self.read_state = 0
        #self.daisy = daisy
        #self.last_odd_sample = OpenBCISample(-1, [], [])  # used for daisy
        self.log_packet_count = 0
        self.attempt_reconnect = False
        self.last_reconnect = 0
        self.reconnect_freq = 5
        self.packets_dropped = 0

        # Disconnects from board when terminated
        atexit.register(self.disconnect)
        
        self.sample=[0]*8
        #self.log = log
        self.ser.write(b'b')
        self.streaming = True
        time.sleep(0.5)
        
        #Initialize check connection
        self.check_connection()
     
#    def readSample(self):
#        
#        """
#        This is about readSample. 
#        :param abra: abra number. 
#        :param cadabra: cadabra number.
#        :param sesame: sesame information.
#        :return ret_val: result information.
#        :rtype: int.
#        """
#        # read current sample
#        self.streamStart()
#        #time.sleep(1)
#        sample = self._read_serial_binary()
#        if sample.channel_data[0]!=0.0:
#            self.sample = sample.channel_data
#        #self.print_incoming_text()
##        time.sleep(5)
##        self.myStopStreaming()
#        return self.sample
    def getSampleRate(self):
        if self.daisy:
            return SAMPLE_RATE / 2
        else:
            return SAMPLE_RATE
    
    def printBytes(self):
        if not self.streaming:
            self.ser.write(b'b')
            self.streaming = True
        while self.streaming:
            print(struct.unpack('B', self.ser.read())[0])   
           
            
    def myStopStreaming(self):
        self.stop()
        self.streaming = False
        return
    

#       Esta função é utilizada em outras para reiniciar a string que é enviada para a placa após certos comandos
    def resetStringxX(self):
        """
        Sobre resetStringxX
        
        Função utilizada internamente para reiniciar a string.
        """
        
        global stringxX
        global stringxXmaster
        stringxX = ['x', 0, 0, 0, 0, 0, 0, 0, 'X']
        return
    
#       laço que torna todos os elementos da lista em string
#       sem a conversão não é possível utilizar o .join que é aplicável somente a strings
#       o .join torna, por exemplo, ['x', '0', '0', '0', '0', '0', '0', '0','X'] em x0000000X
    def transforma_String(self):
        
        #for i in range(0, 7):
        global stringxX
        global stringJoin
        for i in range(0,8):
            stringxX[i] = str(stringxX[i])
            
        stringJoin = ''.join(stringxX)
        # O b que aparece é a conversão do unicode de python 3 para bytes como é o utlizaod em seirlad
#        for i in range(0,):
#            stringB = ['a','b','c','d','e','f','g','h']
#            stringB[i+1] = stringJoin[i]
#            stringB[0] = 'b'
#       convertebyte = b
        stringSer = str.encode(stringJoin)
        print(stringSer)
        self.ser.write(stringSer)
        #time.sleep(1)
        self.resetStringxX()
        return

#       A função ligar_Canal aceita valores em "canal" de 1 a 8, dos 8 canais da placa Cyton; para os valores de ligado ou desligado
 #       Para liga = 1 o canal está ligado, liga = 0 está desligado
    def ligar_Canal(self, canal, liga=1):
        """
        Sobre ligar_Canal
        
        :param canal: este parâmetro determina qual canal será ligado(1 a 8). 
        :param liga: o valor padrão é 1(ligado), mas pode ser 0(desligado).
        
        Retorna qual é o canal que foi ligado/desligado.
         
        """
        
        global stringJoin
        global stringxX
        stringxX[1] = canal
        if(liga == 1):
            stringxX[2] = 0
        if(liga == 0):
            stringxX[2] = 1
        self.transforma_String()
#        self.print_incoming_text()
#        print('passo1')
#        time.sleep(2)
#        print('passo2')
#        self.print_incoming_text()
        print('Canal configurado', canal)
        print(stringJoin)
       # print('passo3')
        #time.sleep(2)
       # self.print_incoming_text()
        self.resetStringxX()
        return
    
#       Os canais são de 1-8; as opções de ganho são os valores 1, 2, 3, 4, 6, 12 e 24
#       O ganho padrão é de 24
    def escolher_Ganho(self, canal, ganho=24):
        """
        Sobre ligar_Canal
        
        :param canal: este parâmetro determina qual canal será ligado(1 a 8). 
        :param ganho: as opções de ganho são os valores 1, 2, 3, 4, 6, 12 e 24; o valor padrão é 24.
        
        Imprime qual é o valor do ganho e de qual canal.
        
        """
        global stringxX
        gain = [1,2,3,4,6,12,24]
        stringxX[1] = canal
        stringxX[3] = gain.index(ganho)
        self.transforma_String()
        print('Ganho de', ganho, 'do', canal)
        #self.print_incoming_text()
        self.resetStringxX()
        return

#       Escolha o tipo de input: normal, curto, BIAS, fonte, temperatura, sinalteste, BIASpos, BIASneg
#       Escreva o tipo entre aspas ''
    def escolher_Input(self, canal, tipo='normal'):
        """
        Sobre escolher_Input
        
        :param canal: este parâmetro determina qual canal será definido o tipo de input(1 a 8). 
        :param tipo: normal, curto, BIAS, fonte, temperatura, sinalteste, BIASpos, BIASneg; o tipo deve estar entre aspas ex:'BIASpos'.
        
        Imprime qual é o tipo de input e qual canal.
        
        """
        global stringxX
        inp = ['normal','curto','BIAS','fonte','temperatura','sinalteste','BIASpos','BIASneg']
        stringxX[1] = canal
        stringxX[4] = inp.index(tipo)
        self.transforma_String()
        print('Tipo de input escolhido', 'do', canal)
        #self.print_incoming_text()
        self.resetStringxX()
        return
 
#       Determina se liga ou não o BIAS, aceita True ou False como valores de "BIAS"  
    def ativar_BIAS(self,canal,BIAS=True):
        """
        Sobre ativar_BIAS
        
        :param canal: este parâmetro determina qual canal terá o BIAS ligado ou não(1 a 8). 
        :param BIAS: parâmetro True para ligar, False para desligar; valor padrão é True.
        
        Imprime qual é o estado do BIAS e de qual canal é.
        
        """
        global stringxX
        stringxX[1] = canal
        stringxX[5] = int(BIAS)
        self.transforma_String()
        print('BIAS configurado', BIAS, 'do', canal)
        #self.print_incoming_text()
        self.resetStringxX()
        return
    
#       Determina se liga ou não o SRB2, aceita True ou False como valores de "SRB2"    
    def ativar_SRB2(self,canal,SRB2=True):
        """
        Sobre ativar_SRB2
        
        :param canal: este parâmetro determina qual canal terá o BIAS ligado ou não(1 a 8). 
        :param SRB2: parâmetro True para ligar, False para desligar; valor padrão é True.
        
        Imprime qual é o estado do SRB2 e de qual canal é.
        
        """
        global stringxX
        stringxX[1] = canal
        stringxX[6] = SRB2
        self.transforma_String()
        print('BIAS configurado', SRB2)
        #self.print_incoming_text()
        self.resetStringxX()
        return
    
#       Determina se liga ou não o SRB1, aceita True ou False como valores de "SRB1"    
    def ativar_SRB1(self,canal,SRB1=True):
        """
        Sobre ativar_SRB1
        
        :param canal: este parâmetro determina qual canal terá o BIAS ligado ou não(1 a 8). 
        :param SRB1: parâmetro True para ligar, False para desligar; valor padrão é True.
        
        Imprime qual é o estado do SRB1 e de qual canal é.
        
        """
        global stringxX
        stringxX[1] = canal
        stringxX[7] = SRB1
        self.transforma_String()
        print('BIAS configurado', SRB1)
        #self.print_incoming_text()
        self.resetStringxX()
        return
    
#       stringxX pode ser alterado manualmente com o comando abaixo, mas necessita da conversões abaixo:
#       "canal" aceita valores de 1 a 8, para selecionar os canais
#       "liga" aceita valores de 0 ou 1, 0 significa canal ligado, e 1 canal desligado
#       "ganho" aceita valores de 0 a 6, considera-se a tabela de conversão: 0/1/2/3/4/5/6(serial) <=> 1/2/4/6/8/12/24 (ganho)
#       "inp" aceita valores de 0 a 7, para selecionar o tipo de input: 0/1/2/3/4/5/6/7 <=> normal/curto/BIAS/fonte/temperatura/sinalteste/BIASpos/BIASneg (tipo)
#       "bias" aceita valores de 0 ou 1, 0 significa bias ligado, 1 bias desligado
#       "srb2" aceita valores de 0 ou 1, 0 significa srb2 ligado, 1 srb2 desligado
#       "srb1" aceita valores de 0 ou 1, 0 significa srb1 ligado, 1 srb1 desligado
#       Configuração de Canais (Channel Setting Commands): x (CHANNEL, POWER_DOWN, GAIN_SET, INPUT_TYPE_SET, BIAS_SET, SRB2_SET, SRB1_SET) X 
    def configCanal(self,canal=1,liga=0,ganho=1,inp=1,bias='normal',srb2=0,srb1=0):
        """
        Sobre ativar_SRB1
        
        Esta função pode ser utilizada ao invés das funções anteriores, para configurar múltiplos parâmetros de um canal de uma vez.
        
        :param canal: este parâmetro determina qual canal terá o BIAS ligado ou não(1 a 8). 
        :param liga: parâmetro ligado(liga = 1) ou desligado(liga = 0).
        :param ganho: parâmetro do ganho, valores 1/2/3/4/6/12/24.
        :param inp: parâmetro de input, tipos: 'normal','curto','BIAS','fonte','temperatura','sinalteste','BIASpos','BIASneg'.
        :param bias: parâmetro do bias; True para ligar, False para desligar; valor padrão é True.
        :param srb2: parâmetro  do srb2; True para ligar, False para desligar; valor padrão é True.
        :param srb1: parâmetro do srb1; True para ligar, False para desligar; valor padrão é True.
        
        Imprime qual é o estado do SRB1 e de qual canal é.
        
        """
        global stringxX
        stringxX[1] = canal
        stringxX[2] = liga
        stringxX[3] = ganho
        stringxX[4] = inp
        stringxX[5] = bias
        stringxX[6] = srb2
        stringxX[7] = srb1
        self.transforma_String()
        ##self.print_incoming_text()
        self.resetStringxX()
        print('Canal Configurado',canal,liga,ganho,inp,bias,srb2,srb1)
        return

    #Comandos Firmware 1.0.0
    
        #Desligar Canais (Turn Channels OFF): 1 2 3 4 5 6 7 8
        #Ligar Canais (Turn Channels ON): ! @ # $ % ^ & *
        #Podem ser incluídos, mas devido à redundância com os comandos de canal não foram adicionados
        #Sinais de Teste (Test Signal Control Commands): 0 - = p [ ]
        #Liga todos os canais, e os conecta ao teste de sinal interno, útil para calibração e teste dos canais, para checar o funcionamento destes
        #São dos tipos ground; sinal com 1x amplitude (devagar ou veloz); sinal corrente contínua; sinal com 2x de amplitude (devagar ou veloz)
    def testGND(self):
        self.ser.write(b'0')
        #self.print_incoming_text()
        print('sinal de teste GND')
        return
    def test1xAmpSlow(self):
        self.ser.write(b'-')
        #self.print_incoming_text()
        print('sinal de teste ganho 1, devagar')
        return
    def test1xAmpFast(self):
        self.ser.write(b'=')
        #self.print_incoming_text()
        
        print('sinal de teste ganho 1, rápido')
        return
    def testDC(self):
        self.ser.write(b'p')
        
        #self.print_incoming_text
        print('sinal de teste CC')
        return
    def test2xAmpSlow(self):
        self.ser.write(b'[')
        #self.print_incoming_text
        print('sinal de teste ganho 1, devagar')
        return
    def test2xAmpFast(self):
        self.ser.write(b']')
        #self.print_incoming_text()
        print('sinal de teste ganho 1, rápido')
        return
         
        #Configuração de Canal Padrão(Default Channel Settings): d
        #Altera as configurações de canais para o padrão
        #Relatório de Configuração Padrão: D
        #Gera um relatório sobre o status da configuração padrão
    def padrao(self):
        self.ser.write(b'd')
        #self.print_incoming_text()
        print('Configurações padrões')
        return
    def padraoRelatorio(self):
        
        self.ser.write(b'D')
        print('Relatório padronizado')
        #self.print_incoming_text()
        return
    
        #Impedância do Canal (LeadOff Impedance Commands): z (CHANNEL, PCHAN, NCHAN) Z
        #O comando enviado é similar à configuração de canais, z e Z são start e end bits respectivamente
        #Canal configura o canal específico, aceita valores de 1 a 8, pchan e nchan aceitam valores de 0 e 1, 0 não é aplicado o sinal de teste, 1 é aplicado
        #O comando é utilizado para se determinar se a impedância nos polos dos canais está correta, envia um sinal de AC de 31.5Hz
        #Espera-se que o canal seja atenuado, caso esteja adequada a conexão, sem atenuação do sinal pode indicar uma má conexão
    def zDoCh(self,canal=1,pchan=0,nchan=0):
        stringZ = ['z',canal,pchan,nchan,'Z']
        for i in range(0, 4):
            stringZ[i] = str(stringZ[i])
            stringZJunta = ''.join(stringZ[i])
        stringSerial = ''.join(['b',stringZJunta])
        self.ser.write(stringSerial)
        print('Teste de impedância')
        #self.print_incoming_text()
        stringZ = ['z',1,0,0,'Z']
        return
        
        #Comandos do Cartão SD (SD card Commands):
        #O comando é utilizado para realizar registro por certo período de tempo das leituras feitas pela placa
        #A S F G H J K L a: cada letra destas corresponde ao tempo de aquisição de dados, que corresponde ao vetor:
        #Em minutos? 5 15 30 60 120 240 720 1440 (a = 14 segundos, pra teste)
        #A/S/F/G/H/J/K/L/a <=> 5 min./15 min./30 min./60 min./120 min./240 min./720 min./1440 min./14 segs.
        #Parar o logging e fechar o arquivo SD: j
    def sdTime5m(self):
        """
        O arquivo de texto gerado tem nome inicial: OBCI_01.txt, com incrementos conforme são gravados outros arquivos.
        Os dados obtidos pela aquisição têm o formato: Número da amostra / 8 valores dos canais / 3 valores dos acelerômetros
        Os dados estão em hexadecimal.
        
        Comandos do Cartão SD (SD card Commands):
        
        O comando é utilizado para realizar registro por certo período de tempo das leituras feitas pela placa, fazendo data logging no cartão SD.    
        sdTime5m/15m/30m/60m/120m/240m/720m/1440m/14s <=> 5 min./15 min./30 min./60 min./120 min./240 min./720 min./1440 min./14 segs. de registro
        
        
        Para parar o logging e fechar o arquivo SD: sdStop; a função deve ser utilizada no final para gerar o arquivo de texto.
        
        """
        print('Registro no cartão SD por 5 minutos')
        self.ser.write(b'A')
        return
    def sdTime15m(self):
        '''
        Ver sdTime 5m.
        '''
        print('Registro no cartão SD por 15 minutos')
        self.ser.write(b'S')
        return
    def sdTime30m(self):
        '''
        Ver sdTime 5m.
        '''
        print('Registro no cartão SD por 30 minutos')
        self.ser.write(b'F')
        return
    def sdTime60m(self):
        '''
        Ver sdTime 5m.
        '''
        print('Registro no cartão SD por 60 minutos')
        self.ser.write(b'G')
        return
    def sdTime120m(self):
        '''
        Ver sdTime 5m.
        '''
        print('Registro no cartão SD por 120 minutos')
        self.ser.write(b'H')
        return
    def sdTime240m(self):
        '''
        Ver sdTime 5m.
        '''
        print('Registro no cartão SD 240 minutos')
        self.ser.write(b'J')
        return
    def sdTime720m(self):
        '''
        Ver sdTime 5m.
        '''
        print('Registro no cartão SD por 720 minutos')
        self.ser.write(b'K')
        return
    def sdTime1440m(self):
        '''
        Ver sdTime 5m.
        '''
        print('Registro no cartão SD por 1440 minutos')
        self.ser.write(b'L')
        return
    def sdTime14s(self):
        '''
        Ver sdTime 5m.
        '''
        print('Registro no cartão SD por 14 segundos')
        self.ser.write(b'a')
        return
    def sdStop(self):
        '''
        Ver sdTime 5m.
        '''
        self.ser.write(b'j')
        print('Comando para finalização da aquisição no cartão SD')
        return
    
        #Comandos de Stream de Dados (Stream Data Commands): 
        #b :começa o streaming de dados
        #s :interrompe o streaming de dados
    
    def streamStart(self):
        ident = 1
        data = 1
        aaux_data = 1
        imp_data = 1
        self.ser.write(b'b')
        self.streaming = True
        t = 1
        while True:
            sample = self._read_serial_binary()
#            ident = packet_id
#            data = channel_data
#            aaaux_data = aux_data
#            imp_data = []
#            print(sample)
#            print(ident)
#            print(data)
#            print(aaaux_data)
#            print(imp_data)
        return
    
   
            
    def streamStop(self):
        self.ser.write(b's')
        print('Finalizando o streaming')
        return
    
        #Comandos Sortidos:
        #? :lê e gera um relatório sobre todas as configurações do ADS1299 e o LIS3DH
        #ADS1299 é um conversor AD especializado para medidas de biopotencial
        #LIS3DH é um acelerômetro linear de três eixos
    def adslisRelatorio(self):
        
        print('Relatório das configurações atuais')
        time.sleep(0.5)
#        
        self.ser.write(b'?')
        self.print_incoming_text()
        
        return 
        #v :"soft reset" da placa Cyton
    def softReset(self):
        print('Soft reset da placa')
        self.ser.write(b'v')
        return
    
    #Comandos Daisy/16 Canais
        #Desligar Canais (Turn Channels OFF):
        #q w e r t y u i :desligam respectivamente os canais de 9 a 16, na ordem
        #Ligar Canais (Turn Channels ON):
        #Q W E R T Y U I :ligam respectivamente os canais de 9 a 16, na ordem
        # As funções aceitam valores de 9 a 16
    def daisyChOff(self, canal):
        daisyOff = ['q','w','e','r','t','y','u','i']
        canalOff = daisyOff[canal-9]
        serialOff = ''.join(['b',canalOff])
        self.ser.write(serialOff)  
        #self.print_incoming_text()
        print('Desligando canal da Daisy:', canal)
        return
        
    def daisyChOn(self,canal):
        daisyOn = ['Q','W','E','R','T','Y','U','I']
        canalOn = daisyOn[canal-9]
        serialOn = ''.join(['b',canalOn])
        self.ser.write(serialOn)  
        #self.print_incoming_text()
        print('Ligando canal da Daisy:', canal)
        return
            
        #Número de Canais(Select maximum channel number):
        #c :Habilita somente os canais 1 a 8
        #C :Habilita todos os canais de 1 a 16
    def maxCh8(self):
        self.ser.write(b'c')
        print('Limite de canais de 1 a 8')
        return
    def maxCh16(self):
        self.ser.write(b'C')
        print('Limite de canais de 1 a 16')
        return
    
    #Comandos Firmware 2.0.0
        # Marcação do Tempo (Time Stamping):
        #< :Inicia o time stamping, sincronizando o Driver e o Host.
        #> :Para o time stamping.
    def timeStamp(self):
        self.ser.write(b'<')
        print('Início do Time Stamping')
        
        return
    def timeStop(self):
        self.ser.write(b'>')
        print('Fim do Time Stamping')
        return
            
        #Número de Rádio do Canal (Get Radio Channel Number):
        #0xF0 0x00: retorna a falha ou sucesso, e o valor do host, mais o do aparelho no caso de sucesso.
        #Configurar Número do Canal de Rádio (Set Radio System Channel Number):
        #0xF0 0x01 0x07: retorna a falha ou sucesso, sucesso se o host e o aparelho estiverem com o mesmo valor; também retorna em HEX o valor do canal.
        #O 0x07 é opcional, para determinar o canal, de 1 a 25 em HEX. De 0x01 a 0x19
        #Configurar Sobreposição do Canal de Rádio (Set Host Radio Channel Override):
        #0xF0 0x02 0x01: retorna falha ou sucesso, força a troca de canal do Host para o canal(opcional). De 0x01 a 0x19
    def radioGet(self):
        self.ser.write(b'0xF0 0x00')
        return
          
    def radioSet(self,radSet):
        radioSet = ' '.join(['b','0x01',radSet])
        self.ser.write(radioSet)
        return
            
    def radioOver(self):
        radioOver = ' '.join(['b','0x02',radOver])
        self.ser.write(radioOver)
        return
            
        #Obter Poll Time de Rádio(Radio Get Poll Time):
        #0xF0 0x03: retorno de pool time, pode significar erros e está associado com as capacidades do sistema. Retornado em HEX o poll time.
        #Configurar Poll Time de Rádio(Radio Get Poll Time):
        #0xF0 0x04 0x40:a terceira opção determina o poll time em HEX, são aceitos valores de 0 a 255, em ms. Padrão é de 80ms.
    def radioPoll(self):
        self.ser.write(b'0xF0 0x03')
        return
    def radioPollSet(self,pollSet=80):
        radioPoll = ' '.join(['b','0x04',pollSet])
        self.ser.write(radioPoll)
        return
                             
        #Configurar o Baud Rate para o Padrão do Rádio do Host (Radio Set HOST to Driver Baud Rate to Default):
        #0xF0 0x05: configura o Baud Rate para 115200Hz.
        #Configurar o Baud Rate para Modo de Alta-Velocidade (Radio Set HOST to Driver Baud Rate to High-Speed mode):
        #0xF0 0x06: configura o Baud Rate pra 230400Hz.
        #Configurar o Baud Rate para Modo de Hiperalta-Velocidade (Radio Set HOST to Driver Baud Rate to Hyper-Speed mode):
        #0xF0 0x0A: configura o Baud Rate pra 921600Hz.
    def radio1152kHz(self):
        self.ser.write(b'0xF0 0x05')
        return
    def radio2304kHz(self):
        self.ser.write(b'0xF0 0x06')
        return
    def radio9216kHz(self):
        self.ser.write(b'0xF0 0x0A')
        return
        
        #Relatório do Sistema de Rádio:
        #0xF0 0x07: checa o status do sistema de rádio, confirma ou nega se está operante.
    def radioRelat(self):
        self.ser.write(b'0xF0 0x07')
        return
    
    #Comandos Firmware 3.0.0
        
        #Taxa de Aquisição (Sample Rate):
        #~0 : configura a taxa de aquisição, o 0 no comando pode ser alterado para os valores 0/1/2/3/4/5/6/~
        #Os valores correspondem às taxas: 16000Hz / 8000Hz / 4000Hz / 2000Hz / 1000Hz / 500Hz / 250Hz / Obter a taxa de aquisição atual
    def sample16k(self):
        self.ser.write(b'~0')
        print('Sample Rate: 16000Hz')
        return
    def sample8k(self):
        self.ser.write(b'~1')
        print('Sample Rate: 8000Hz')
        return
    def sample4k(self):
        self.ser.write(b'~2')
        print('Sample Rate: 4000Hz')
        return
    def sample2k(self):
        self.ser.write(b'~3')
        print('Sample Rate: 2000Hz')
        return
    def sample1k(self):
        self.ser.write(b'~4')
        print('Sample Rate: 1000Hz')
        return
    def sample500(self):
        self.ser.write(b'~5')
        print('Sample Rate: 500Hz')
        return
    def sample250(self):
        self.ser.write(b'~6')
        print('Sample Rate: 250Hz')
        return
    def sampleStatus(self):
        self.ser.write(b'~~')
        print('Sample Rate Atual')
        return
        
        #Modo da Placa (Board Mode):
        #/0 : configura o modo da placa, o 0 no comando pode ser alterado para os valores 0/1/2/3/4//
        #Os valores correspondem as modos: Padrão / Modo Debug / Modo Analógico / Modo Digital / Modo Marcador / Obter o modo de aquisição atual
    def boardModeDef(self):
        self.ser.write(b'/0')
        print('Modo: Padrão')
        return
    def boardModeDebug(self):
        self.ser.write(b'/1')
        print('Modo: Debug')
        
        return
    def boardModeAnalog(self):
        self.ser.write(b'/2')
        print('Modo: Analógico')
        return
    def boardModeDigital(self):
        self.ser.write(b'/3')
        print('Modo: Digital')
        return
    def boardModeMarker(self):
        self.ser.write(b'/4')
        print('Modo: Marcador')
        return
    def boardModeStatus (self):
        self.ser.write(b'/X')
        print('Modo Atual')
        return
        
    def startText(self):
        self.ser.write(b'x')
        return
        
        #Comandos do Shield de Wifi (Wifi Shield Commands):
        #{ : Faz uma tentativa de se sincronizar com shield de Wifi, retorna o sucesso ou falha.
        #} : Tenta remover o shield de Wifi, retorna sucesso ou falha da operação.
        #: : Obtém o status do shield de Wifi, se está presente ou não.
    def WifiShieldSync(self):
        print('Tentativa de sincronização de Wifi')
        self.ser.write(b'{')
        
        return 
    def WifiShieldDesync(self):
        print('Tentativa de desincronização de Wifi')
        self.ser.write(b'}')
        return                     
    def WifiShieldStatus(self):
        print('Status do Wifi')
        self.ser.write(b':') 
        return
        
         #Obter Versão (Get Version):
         #V : Retorna a versão do Firmware.
    def firmware(self):
        self.ser.write(b'V')
        #time.sleep(0.5)
        self.print_incoming_text()
        print('Versão do Firmware:')
        
        return
                             
    #Adendo
        
        #Caracteres não utilizados: 9 ( ) _ o O f g h k l ‘ “ n N M , . (space)
class OpenBCISample(object):
    

    def __init__(self, packet_id, channel_data, aux_data):
        self.id = packet_id
        self.channel_data = channel_data
        self.aux_data = aux_data
        self.imp_data = []

     