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
#-------------------------------
#!/usr/bin/env python2.7

#imports nativos do python a partir do 2.7 com excecao do yapsy para plugins, que nao e necessario para
#a utilizaçao da placa, portanto foi removido "from yapsy.PluginManager import PluginManager"
#from __future__ ajuda na compatibilidade entre versões do python, neste caso os diferentes modos da função print

import argparse  # new in Python2.7

#import atexit removido pois faz parte dos plugins
#import logging removido pois nao sera utilziado
#a porta foi encontrada pelo AUTO: /dev/ttyUSB0, pode variar para as demais placas
import logging
import string
import sys
import threading
import time

print("Board type: OpenBCI Cyton (v3 API)")

#removido "logging.basicConfig(level=logging.ERROR)"


# Load the plugins from the plugin directory.
#sem necessidade de plugins, porem ha algumas opçoes importantes para inicializar
#removido manager = PluginManager()

if __name__ == '__main__':
    # como estes comandos são esperados logo no começo, pode ser incluido um readme para iniciar com
    #algumas das configurações ja desejadas  

    print("------------user.py-------------")
    
    import openbci.cyton as bci
    parser = argparse.ArgumentParser(description="OpenBCI 'user'")
    #removidas algumas das opcoes para o parser, nao vai precisar de '--board', vai ser somente com cyton
    #'--list' tambem removido por nao necessitar da lista de plugins ja que nao vai utilizar
    #'--info' nao vai ser utlizado pois fornece mais informaçoes sobre certo plugin
    
    parser.add_argument('-p', '--port',
                        help="For Cyton, port to connect to OpenBCI Dongle " +
                             "( ex /dev/ttyUSB0 or /dev/tty.usbserial-* ). ")
                        #removido parte do print relacionado a board ganglion                            
    parser.set_defaults(port="AUTO")
    # baud rate is not currently used
    #parser.add_argument('-b', '--baud', default=115200, type=int,
                        #help="Baud rate (not currently used)")
    parser.add_argument('--no-filtering', dest='filtering',
                        action='store_false',
                        help="Disable notch filtering")
    parser.set_defaults(filtering=True)
    parser.add_argument('-d', '--daisy', dest='daisy',
                        action='store_true',
                        help="Force daisy mode (cyton board)")
    parser.add_argument('-x', '--aux', dest='aux',
                        action='store_true',
                        help="Enable accelerometer/AUX data (ganglion board)")
    parser.add_argument('--log', dest='log', action='store_true',
                        help="Log program")
    # first argument: plugin name, then parameters for plugin
    #opcoes  '--add', '--log', ''plugins-path' removidos, relacionados a opcoes de plugin
   
    #finaliza o parser com args
    args = parser.parse_args()
    
    #no caso de não serem adicionados nennhum dos plugins acima, aparece o de baixo
    #alterar o texto para nao mencionar os plugins ou o ganglion
    #if not args.add: removido
    
        #codigo para seleção de placa, como vai ser somente o cyton, pode deixar fixo,
        #importa o outro arquivo openbci.cyton como bci, é o que interessa
        #"import openbci.cyton as bci" pode ser determinado logo no inicio ja que vai ser o unico tipo
        #removido codigo de seleçao entre o cyton e o ganglion (args.board == cyton ou ganglion, etc), import de cyton movido junto dos outros imports
   

    # Check AUTO port selection, a "None" parameter for the board API
    if "AUTO" == args.port.upper():
        #talvez alterar o comando '--port' para algo mais intuitivo
        print("Will try do auto-detect board's port. Set it manually with '--port' if it goes wrong.")
        args.port = None
    else:
        print("Port: ", args.port)
        
    #removido parte do codigo de "plugins_paths = ["openbci/plugins"]" e o "manager" de plugins   

    # Print list of available plugins and exit
    #opcao removida

    # User wants more info about a plugin...
    #info removido
    
    #notch filtering é filtro rejeita-faixa
    print("\n------------SETTINGS-------------")
    print("Notch filtering:" + str(args.filtering))

    # Logging
    #logging para registro das atividades, mas esta relacionado com o uso do yapsy, portanto não sera utilizado
    #esse modulo
   
    if args.log:
        print("Logging Enabled: " + str(args.log))
        logging.basicConfig(filename="OBCI.log", format='%(asctime)s - %(levelname)s : %(message)s',
                            level=logging.DEBUG)
        logging.getLogger('yapsy').setLevel(logging.DEBUG)
        logging.info('---------LOG START-------------')
        logging.info(args)
    #codigo do logging removido
    

    print("\n-------INSTANTIATING BOARD-------")
    #args.board foi removido, o codigo fica sem sentido no if args.board, entao "board =" para as opcoes de cyton apenas
    #args.port foi determinado anteriormente com o AUTO ou manualmente com o '--port'
    #baud nao eh uma opcao de acordo com os comentarios, fixado em 115200 sample rate
    #daisy determinado com as opções iniciais com '--daisy'
    #args.filtering escolhido com '--no-filtering'
    #
    #logging utilizado no cyton.py
    
    board = bci.OpenBCICyton(port=args.port,
                                
                                 daisy=args.daisy,
                                 filter_data=args.filtering,
                                 scaled_output=True,
                                 log=args.log)
        
    #opcao de "args.board" e "board =" removidos
        
    #  Info about effective number of channels and sampling rate
    if board.daisy:
        print("Force daisy mode:")
    else:
        print("No daisy:")
        print(board.getNbEEGChannels(), "EEG channels and", board.getNbAUXChannels(), "AUX channels at",
              board.getSampleRate(), "Hz.")

    #secao de PLUGINS abaixo removida 

    # Fetch plugins, try to activate them, add to the list if OK
    #nao vai precisar de nada relacionado com os plugins, removido o codigo abaixo até a secao "INFO"

    #comandos convertidos para mais intuitivos
    print("--------------INFO---------------")
    print("User serial interface enabled...\n\/start to run, /stop \n\
before issuing new commands afterwards.\n\Type /exit to exit. \n\
Board outputs are automatically printed as: \n\
%  <tab>  message\n\
$$$ signals end of message")
    
    print("\n-------------BEGIN---------------")
    # Init board state
    # s: stop board streaming; v: soft reset of the 32-bit board (no effect with 8bit board)
    #com isso o inicio de s ja reinicia a placa e causa um soft reset
    s = 'sv'
    # Tell the board to enable or not daisy module
    #em vez disso colocar uma opcao y/n para uso da daisy, ou algo como daisy_enable
    if board.daisy:
        s = s + 'C'
    else:
        s = s + 'c'
    # d: Channels settings back to default
    s = s + 'd'
    #fazer algum comando como end, para finalizar a string s que é mandada
    while s != "/exit":
        # Send char and wait for registers to set
        if not s:
            pass
        elif "help" in s:
            print("View command map at: \
http://docs.openbci.com/software/01-OpenBCI_SDK.\n\
For user interface: read README or view \
https://github.com/OpenBCI/OpenBCI_Python")

        elif board.streaming and s != "/stop":
            print("Error: the board is currently streaming data, please type '/stop' before issuing new commands.")
        else:
            # read silently incoming packet if set (used when stream is stopped)
            flush = False

            if '/' == s[0]:
                s = s[1:]
                rec = False  # current command is recognized or fot

                if "T:" in s:
                    lapse = int(s[string.find(s, "T:") + 2:])
                    rec = True  
                elif "t:" in s:
                    lapse = int(s[string.find(s, "t:") + 2:])
                    rec = True
                else:
                    lapse = -1
                
                #cyton nao suporta impedance checking então parte if 'startimp' do codigo foi removida
                                   
                if "start" in s:
                    print("started streaming")
                    board.setImpedance(False)
                    #fun nao fara parte deste projeto pois fun é de relacionado aos plugins
                    #codigo relacionado ao 'fun' removido
                   
                    rec = True

                elif 'test' in s:
                    test = int(s[s.find("test") + 4:])
                    board.test_signal(test)
                    rec = True
                elif 'stop' in s:
                    board.stop()
                    rec = True
                    flush = True
                if rec == False:
                    print("Command not recognized...")

            elif s:
                for c in s:
                    if sys.hexversion > 0x03000000:
                        board.ser_write(bytes(c, 'utf-8'))
                    else:
                        board.ser_write(bytes(c))
                    time.sleep(0.100)

            line = ''
            time.sleep(0.1)  # Wait to see if the board has anything to report
            
            # The Cyton nicely return incoming packets -- here supposedly messages
            # whereas the Ganglion prints incoming ASCII message by itself
            if board.getBoardType() == "cyton":
                while board.ser_inWaiting():
                    # we're supposed to get UTF8 text, but the board might behave otherwise
                    c = board.ser_read().decode('utf-8', errors='replace')
                    line += c
                    time.sleep(0.001)
                    if (c == '\n') and not flush:
                        print('%\t' + line[:-1])
                        line = ''
            #secao de ganglion removida
                        
            if not flush:
                print(line)

      
#------------------------------------------------------------------------------   
        


#class myclass:
#    name = ''
#   def __init__(self):
#        self.name = 'name'

#manter o cyton na mesma pasta para que consiga encontrar
#string inicial para montar o comando desejado
#variaveis globais
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
n = 0

class myCyton(cyton.OpenBCICyton):
    
    
    def __init__(self, id=0,port=None, filter_data=True,timeout=None):
        cyton.OpenBCICyton.__init__(self,port=port, baud=115200, filter_data=filter_data, scaled_output=True, daisy=False, aux=False, impedance=False, log=False, timeout=timeout)
        self.log = log  # print_incoming_text needs log
        self.streaming = False
        self.baudrate = baud
        self.timeout = timeout
        if not port:
            port = self.find_port()
        self.port = port
        # might be handy to know API
        self.board_type = "cyton"
        print("Connecting to V3 at port %s" % (port))
        if port == "loop://":
            # For testing purposes
            self.ser = serial.serial_for_url(port, baudrate=baud, timeout=timeout)
        else:
            self.ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)

        print("Serial established...")

        time.sleep(2)
        # Initialize 32-bit board, doesn't affect 8bit board
        self.ser.write(b'v')

        # wait for device to be ready
        time.sleep(1)
        if port != "loop://":
            self.print_incoming_text()

        self.streaming = False
        self.filtering_data = filter_data
        self.scaling_output = scaled_output
        # number of EEG channels per sample *from the board*
        self.eeg_channels_per_sample = 8
        # number of AUX channels per sample *from the board*
        self.aux_channels_per_sample = 3
        self.imp_channels_per_sample = 0  # impedance check not supported at the moment
        self.read_state = 0
        self.daisy = daisy
        self.last_odd_sample = OpenBCISample(-1, [], [])  # used for daisy
        self.log_packet_count = 0
        self.attempt_reconnect = False
        self.last_reconnect = 0
        self.reconnect_freq = 5
        self.packets_dropped = 0

        # Disconnects from board when terminated
        atexit.register(self.disconnect)
        #self.nChannels=8
        #nao pareceu ter correspondencia com outros arquivos
        self = OpenBCICyton
        self.sample=[0]*8
        self.log = log
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
    
    def stringTest(self, s):
        self.s = s
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
    def test1(self):
            self.ser.write(b'0')
    def test2(self):
            self.ser.write(b'-')
    def test3(self):
            self.ser.write(b'=')
    def test4(self):
            self.ser.write(b'p')
    def test5(self):
            self.ser.write(b'[')
    def test6(self):
            self.ser.write(b']')
    
        #Configuração de Canais (Channel Setting Commands): x (CHANNEL, POWER_DOWN, GAIN_SET, INPUT_TYPE_SET, BIAS_SET, SRB2_SET, SRB1_SET) X 
        
        
        #Configuração de Canal Padrão(Default Channel Settings): d
        #Relatório de Configuração Padrão: D
    def padrao(self):
            self.ser.write(b'd')
    def padraoRel(self):
            self.ser.write(b'D')
    
        #Impedância do Canal (LeadOff Impedance Commands): z (CHANNEL, PCHAN, NCHAN) Z
    def ZdoCh(self):
            self.ser.write(b'z 1 1 1 Z')     
    
        #Comandos do Cartão SD (SD card Commands):
        #A S F G H J K L a:cada letra destas corresponde ao tempo de aquisição de dados, que corresponde ao vetor:
        #Em minutos 5 15 30 60 120 240 720 1440 (a = 14 segundos, pra teste)
        #Parar o logging e fechar o arquivo SD: j
    def sdTime(self):
            self.ser.write(b'A')
    def sdStop(self):
            self.ser.write(b'j')
    
        #Comandos de Stream de Dados (Stream Data Commands): 
        #b :começa o streaming de dados
        #s :interrompe o streaming de dados
    def stream(self):
            self.ser.write(b'b')
    def stop(self):
            self.ser.write(b's')
    
        #Comandos Sortidos:
        #? :lê e faz relatório sobre todas as configurações do ADS1299 e o LIS3DH
        #ADS1299 é um conversor AD especializado para medidas de biopotencial
        #LIS3DH é um acelerômetro linear de três eixos
    def ADSLIS(self):
            self.ser.write(b'?')
        #v :"soft reset" da placa Cyton
    def reset(self):
            self.ser.write(b'v')
    
    #Comandos Daisy/16 Canais
        #Desligar Canais (Turn Channels OFF):
        #q w e r t y u i :desligam respectivamente os canais de 9 a 16, na ordem
        #Ligar Canais (Turn Channels ON):
        #Q W E R T Y U I :ligam respectivamente os canais de 9 a 16, na ordem
    def daisyChoff(self):
            self.ser.write(b'q')
    def daisyChon(self):
            self.ser.write(b'Q')
    
        #Número de Canais(Select maximum channel number):
        #c :Habilita somente os canais 1 a 8
        #C :Habilita todos os canais de 1 a 16
    def maxCh8(self):
            self.ser.write(b'c')
    def maxCh16(self):
            self.ser.write(b'C')
    
    #Comandos Firmware 2.0.0
        # Marcação do Tempo (Time Stamping):
        #< :Inicia o time stamping, sincronizando o Driver e o Host.
        #> :Para o time stamping.
    def timeStamp(self):
            self.ser.write(b'<')
    def timeStop(self):
            self.ser.write(b'>')
            
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
     