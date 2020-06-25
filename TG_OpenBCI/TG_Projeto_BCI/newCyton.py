"""
newCyton.py
===========

New module based on the original cyton.py file from the OpenBCI project.

"""
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
#copia novouser.py

import argparse  # new in Python2.7
import string
import sys

print("***OpenBCI newCyton***")

#------------------------------------------------------------------------------
#sample rate de 250 SPS é fixo para placa Cyton com dongle

SAMPLE_RATE = 250.0  
START_BYTE = 0xA0  
END_BYTE = 0xC0  
ADS1299_Vref = 4.5  
ADS1299_gain = 24.0  
scale_fac_uVolts_per_count = ADS1299_Vref / \
    float((pow(2, 23) - 1)) / ADS1299_gain * 1000000.
scale_fac_accel_G_per_count = 0.002 / \
    (pow(2, 4))  

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
        
        self.timeout = timeout
        if not port:
            port = self.find_port
            self.port = port
    
        self.board_type = "cyton"

        print("Conexão serial estabelecida...")

        time.sleep(0.5)
    
        print("Soft Reset da placa")


        self.ser.write(b'v')
        time.sleep(1)

        print('IDs do ADS1299 e do LIS3DH, versão do Firmware:\n')

        if port != "loop://":
            self.print_incoming_text()

        self.streaming = False
        self.filtering_data = filter_data
        
        self.eeg_channels_per_sample = 8
        
        self.aux_channels_per_sample = 3
        self.imp_channels_per_sample = 0  # impedance check not supported at the moment
        self.read_state = 0
        
        self.log_packet_count = 0
        self.attempt_reconnect = False
        self.last_reconnect = 0
        self.reconnect_freq = 5
        self.packets_dropped = 0

        
        atexit.register(self.disconnect)

        self.sample=[0]*8
        
        self.ser.write(b'b')
        self.streaming = True
        time.sleep(0.5)

        
        self.check_connection()

    #################################################Funções#########################################


#       Esta função é utilizada em outras para reiniciar a string que é enviada para a placa após certos comandos
    def internal_resetting_configuration_channel_String_of_values(self):
        """
        Internal function for resetting the string of the channel configuration process. This function, and the others related to the channel configuration are based on one of the original commands for the Cyton, with the format: x0000000X, x being the start bit, and X being the end bit; the remaining 7 values meaning a different parameter within the channels. Dividing this command type into more functions was a way to turn it into a more intuitive way of using it.
        """

        global stringxX
        global stringxXmaster
        stringxX = ['x', 0, 0, 0, 0, 0, 0, 0, 'X']
        return

#       laço que torna todos os elementos da lista em string
#       sem a conversão não é possível utilizar o .join que é aplicável somente a strings
#       o .join torna, por exemplo, ['x', '0', '0', '0', '0', '0', '0', '0','X'] em x0000000X
    def transform_the_vector_to_it_through_serial(self):
        """
        Internal function that executes the necessary transformations of the channel configuration String, that looks like this: ['x', '0', '0', '0', '0', '0', '0', '0','X']; so this can be properly formatted so it can be interpreted by the Cyton; it merges all elements in a single String, then converts this into its value in bits.
        """
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

#        if self.ser.inWaiting():
#            c = self.ser.read()
#            print(c)
        #self.print_incoming_text()
        #time.sleep(1)
        self.internal_resetting_configuration_channel_String_of_values()
        return

    def resend_all_values_set_for_the_channel_configuration(self):
        """
        Function for converting and sending through the serial port all the changes made in the channels. It's recommended to use this function if you're going to make multiple changes in the channels, this way you can gaurantee that all the changes have been made, ignoring the overwriting. So this function is to be utilized after all functions that have to do with the channel configuration.
        """
        global stringxXMaster
        global stringJoin
        for i in range(0,8):
            stringxXMaster[i] = str(stringxXMaster[i])
        stringJoin = ''.join(stringxXMaster)
        stringSer = str.encode(stringJoin)
        print(stringSer)
        self.ser.write(stringSer)

        return

#       A função onr_channel aceita valores em "channel" de 1 a 8, dos 8 canais da placa Cyton; para os valores de ondo ou desondo
 #       Para on = 1 o channel está ondo, on = 0 está desondo
    def set_channel_on_or_off(self, channel, on=1):
        """
        This turns the channel on or off, defined with 'channel' and 'on' parameters.

        :param channel: this parameter defines which channel is being turned on (values:1/2/3/4/5/6/7/8).
        :param on: the standard value is 1(ON), while it can also accept 0(OFF).

        Prints which channel was turned on/off.
        """
        global stringxXMaster
        global stringJoin
        global stringxX
        stringxX[1] = channel

        if(on == 1):
            stringxX[2] = 0
            stringxXMaster[channel-1][2] = 0
        if(on == 0):
            stringxX[2] = 1
            stringxXMaster[channel-1][2] = 1

        self.transform_the_vector_to_it_through_serial()
        print('channel set', channel,'to',on)
        print(stringJoin)

        return

#       Os canais são de 1-8; as opções de gain são os valores 1, 2, 3, 4, 6, 12 e 24
#       O gain padrão é de 24
    def set_channel_input_gain(self, channel, gain=24):
        """
        This function defines what's the gain of a certain channel, based on the 'channel' and 'gain' parameters. The gain set in this is relevant for the calculations to get the real value in Volts, from the .txt file or the streaming data.

        :param channel: this parameter defines which channel is having its gain set (values:1/2/3/4/5/6/7/8).
        :param gain: the accepted values for gain are: 1, 2, 3, 4, 6, 12 e 24; default is 24.

        Prints which channel was turned on or off.
        """
        global stringxX
        gain = [1,2,3,4,6,12,24]
        stringxX[1] = channel
        stringxX[3] = gain.index(gain)
        stringxXMaster[channel-1][3] = gain.index(gain)

        self.transform_the_vector_to_it_through_serial()
        print('gain of', gain, 'on channel', channel)
        #self.print_incoming_text()
        self.internal_resetting_configuration_channel_String_of_values()
        return

#       Escolha o type de input: normal, short, BIAS, VDD, temp, testsignal, BIASpos, BIASneg
#       Escreva o type entre aspas ''
    def set_channel_input_type(self, channel, type='normal'):
        """
        Function for defining the type of data that is being obtained. The parameters are 'channel' and 'type'. It's not made clear by the OpenBCI site what each type of input alters during the sampling, these were not tested for the differences in input.
        :param channel: this parameter defines which channel is having its input type defined (values:1/2/3/4/5/6/7/8).
        :param type: normal, short, BIAS, VDD, temp, testsignal, BIASpos, BIASneg; type must be in String format, that is between brackets; ex: 'BIAS'.

        Prints which type of input the defined channel has been set to.

        """
        global stringxX
        inp = ['normal','short','BIAS','VDD','temp','testsignal','BIASpos','BIASneg']
        stringxX[1] = channel
        stringxX[4] = inp.index(type)
        stringxXMaster[channel-1][4] = inp.index(type)
        self.transform_the_vector_to_it_through_serial()
        print('input type:',type, 'from channel', channel)
        #self.print_incoming_text()
        self.internal_resetting_configuration_channel_String_of_values()
        return

#       Determina se on ou não o BIAS, aceita True ou False como valores de "BIAS"
    def set_channel_BIAS_on_or_off(self,channel,BIAS=True):
        """
        Function for setting the BIAS of the defined channel on or off.

        :param channel: this parameter defines which channel is having its BIAS turned on or off (values:1/2/3/4/5/6/7/8).
        :param BIAS: True for turning it on, False for turning it off; default value is True.

        Prints if the BIAS is on or not, and the channel set.

        """
        global stringxX
        stringxX[1] = channel
        stringxX[5] = int(BIAS)
        stringxXMaster[channel-1][5] = int(BIAS)
        self.transform_the_vector_to_it_through_serial()
        print('BIAS value', BIAS, 'from channel', channel)
        #self.print_incoming_text()
        self.internal_resetting_configuration_channel_String_of_values()
        return

#       Determina se on ou não o SRB2, aceita True ou False como valores de "SRB2"
    def set_channel_connection_to_SRB2_on_or_off(self,channel,SRB2=True):
        """
        This connects the positive input of the specified channel to the SRB2 pin, closing a circuit. Multiple inputs can be connected to this same pin.
        :param channel: this parameter defines which channel is having its SRB2 turned on or off (values:1/2/3/4/5/6/7/8).
        :param SRB2: True for turning it on, False for turning it off; default value is True.

        Prints the channel and if the channel is connected or not to SRB2.

        """
        global stringxX
        stringxX[1] = channel
        stringxX[6] = SRB2
        stringxXMaster[channel-1][6] = int(SRB2)

        self.transform_the_vector_to_it_through_serial()
        print('SRB2 value', SRB2, 'from channel', channel)
        #self.print_incoming_text()
        self.internal_resetting_configuration_channel_String_of_values()
        return

#       Determina se on ou não o SRB1, aceita True ou False como valores de "SRB1"
    def set_channel_connection_to_SRB1_on_or_off(self,channel,SRB1=True):
        """
        This connects the negative input of the specified channel to the SRB2 pin, closing a circuit. Multiple inputs can be connected to this same pin.
        :param channel: this parameter defines which channel is having its SRB1 turned on or off (values:1/2/3/4/5/6/7/8).
        :param SRB1: True for turning it on, False for turning it off; default value is True.

        Prints the channel, and if the channel is connected or not to SRB1.

        """
        global stringxX
        stringxX[1] = channel
        stringxX[7] = SRB1
        stringxXMaster[channel-1][6] = int(SRB1)

        self.transform_the_vector_to_it_through_serial()
        print('SRB1 value', SRB1, 'from channel', channel)
        #self.print_incoming_text()
        self.internal_resetting_configuration_channel_String_of_values()
        return

#       stringxX pode ser alterado manualmente com o comando abaixo, mas necessita da conversões abaixo:
#       "channel" aceita valores de 1 a 8, para selecionar os canais
#       "on" aceita valores de 0 ou 1, 0 significa channel ondo, e 1 channel desondo
#       "gain" aceita valores de 0 a 6, considera-se a tabela de conversão: 0/1/2/3/4/5/6(serial) <=> 1/2/4/6/8/12/24 (gain)
#       "inp" aceita valores de 0 a 7, para selecionar o type de input: 0/1/2/3/4/5/6/7 <=> normal/short/BIAS/VDD/temp/testsignal/BIASpos/BIASneg (type)
#       "bias" aceita valores de 0 ou 1, 0 significa bias ondo, 1 bias desondo
#       "srb2" aceita valores de 0 ou 1, 0 significa srb2 ondo, 1 srb2 desondo
#       "srb1" aceita valores de 0 ou 1, 0 significa srb1 ondo, 1 srb1 desondo
#       Configuração de Canais (Channel Setting Commands): x (CHANNEL, POWER_DOWN, GAIN_SET, INPUT_TYPE_SET, BIAS_SET, SRB2_SET, SRB1_SET) X

    def set_all_available_parameters_for_a_channel(self,channel=1,on=1,gain=1,type='normal',BIAS=True,SRB2=True,SRB1=True):
        """
        This function can be utilized in place of the previous functions, so as to configure multiple parameters of a channel in a single command. The parameters and their value restrictions are the same as the previous functions. The separate functions may better explain how its respective parameter works. Set by the parameters 'channel', 'on', 'gain', 'type', 'bias', 'srb2', 'srb1'.

        :param channel: this sets the channel to be customized.
        :param on: 1 for turning the channel on, 0 for turning it off.
        :param gain: gain parameter, available values: 1/2/3/4/6/12/24; default is 24.
        :param type: input type, accepted values: 'normal','short','BIAS','VDD','temp','testsignal','BIASpos','BIASneg'; default is 'normal'.
        :param bias: bias setting; True to turn it on, False to turn it off; default is True.
        :param srb2: srb2 setting; True to turn it on, False to turn it off; default is True.
        :param srb1: srb1 setting; True to turn it on, False to turn it off; default is True.

        Prints the channel, and its setting values.

        """
        global stringxX
        stringxX[1] = channel
        if(on == 1):
            stringxX[2] = 0
        if(on == 0):
            stringxX[2] = 1

        gain = [1,2,3,4,6,12,24]
        stringxX[3] = gain.index(gain)

        inp = ['normal','short','BIAS','VDD','temp','testsignal','BIASpos','BIASneg']
        stringxX[1] = channel
        stringxX[4] = inp.index(type)

        stringxX[5] = int(BIAS)
        stringxX[6] = int(SRB2)
        stringxX[7] = int(SRB1)

        self.transform_the_vector_to_it_through_serial()

        self.internal_resetting_configuration_channel_String_of_values()
        print('channel set as',channel,on,gain,type,BIAS,SRB2,SRB1)
        return

    #Comandos Firmware 1.0.0

        #Desonr Canais (Turn Channels OFF): 1 2 3 4 5 6 7 8
        #onr Canais (Turn Channels ON): ! @ # $ % ^ & *
        #Podem ser incluídos, mas devido à redundância com os comandos de channel não foram adicionados
        #Sinais de Teste (Test Signal Control Commands): 0 - = p [ ]
        #on todos os canais, e os conecta ao teste de sinal interno, útil para calibração e teste dos canais, para checar o funcionamento destes
        #São dos types ground; sinal com 1x amplitude (devagar ou veloz); sinal corrente contínua; sinal com 2x de amplitude (devagar ou veloz)

    def begin_ground_test_signal_input_all_channels(self):
        """
        This function connects the signal to the GND for all the 8 channels of the Cyton, it can be used for testing out the channels. Prints the type of signal being started.
        """
        self.ser.write(b'0')
        #self.print_incoming_text()
        print('ground test signal')
        return
    def begin_square_wave_test_signal_with_50mV_amplitude_1Hz_frequency_all_channels(self):
        """
        This function makes the Cyton send out a test square wave and collect it on all 8 channels, with approximately 50mV and 1Hz. Prints the type of signal being started.
        """
        self.ser.write(b'-')


        print('50mV 1Hz square wave signal')
        return
    def begin_square_wave_test_signal_with_50mV_amplitude_2Hz_frequency_all_channels(self):
        """
        This function makes the Cyton send out a test square wave and collect it on all 8 channels, with approximately 50mV and 2Hz. Prints the type of signal being started.
        """
        self.ser.write(b'=')
        #self.print_incoming_text()

        print('50mV 2Hz square wave signal')
        return
    def begin_continuous_current_test_signal_all_channels(self):
        """
        This function generates a DC test signal for all 8 channels, and collects their data.
        """
        self.ser.write(b'p')

        #self.print_incoming_text
        print('DC test signal')
        return
    def begin_square_wave_test_signal_with_100mV_amplitude_1Hz_frequency_all_channels(self):
        """
        This function makes the Cyton send out a test square wave and collect it on all 8 channels, with approximately 100mV and 1Hz(double the gain of the previous test functions). Prints the type of signal being started.
        """
        self.ser.write(b'[')
        #self.print_incoming_text
        print('100mV 1Hz square wave signal')
        return
    def begin_square_wave_test_signal_with_100mV_amplitude_2Hz_frequency_all_channels(self):
        """
        This function makes the Cyton send out a test square wave and collect it on all 8 channels, with approximately 100mV and 2Hz. Prints the type of signal being started.
        """
        self.ser.write(b']')
        #self.print_incoming_text()
        print('100mV 2Hz square wave signal')
        return

        #Configuração de channel Padrão(Default Channel Settings): d
        #Altera as configurações de canais para o padrão
        #Relatório de Configuração Padrão: D
        #Gera um relatório sobre o status da configuração padrão
    def set_all_channels_to_default_values_of_parameters_all_channels(self):
        """
        This sets up all channels, returning them to the default settings; that is the channel being on, a gain of 24, 'normal' type of input, , BIAS, SRB2 e SRB1 all set as True. These are the same settings as the combination ofthe default values of the channel config functions.

        """
        self.ser.write(b'd')
        #self.print_incoming_text()
        print('Default configs for all channels')
        return
    def get_report_for_default_settings(self):
        """
        This gives a report about what the default settings are.
        """
        self.ser.write(b'D')
        print('default report')
        self.print_incoming_text()
        return

        #Impedância do channel (LeadOff Impedance Commands): z (CHANNEL, PCHAN, NCHAN) Z
        #O comando enviado é similar à configuração de canais, z e Z são start e end bits respectivamente
        #channel configura o channel específico, aceita valores de 1 a 8, pchan e nchan aceitam valores de 0 e 1, 0 não é aplicado o sinal de teste, 1 é aplicado
        #O comando é utilizado para se determinar se a impedância nos polos dos canais está correta, envia um sinal de AC de 31.5Hz
        #Espera-se que o channel seja atenuado, caso esteja adequada a conexão, sem atenuação do sinal pode indicar uma má conexão
    def test_the_impedance_of_the_channel(self,channel=1,pchan=0,nchan=0):
        """
        This function is similar to the channel configuration, as it has z and Z as the start and end bits respectively. A similar approach was also made with this, to make it more intuitive. This function sends out an AC signal of 31.5Hz to a channel's poles, for checking it the impedance is correct. If the channel suffers dampening, this should indicate adequate impedance; otherwise it could be a bad connection problem. The parameters are 'channel', 'pchan' and 'nchan'.
        :param channel: this parameter defines the channel to be tested, values ranging from 1 to 8, same values as the channel configuration.
        :param pchan: 0 and 1 are the accepted value; with 0 the impedance is not applied to the positive input of the channel; with 1 as the value, it is applied.
        :param nchan: 0 and 1 are the accepted value; with 0 the impedance is not applied to the negative input of the channel; with 1 as the value, it is applied.
        """
        stringZ = ['z',channel,pchan,nchan,'Z']
        for i in range(0, 4):
            stringZ[i] = str(stringZ[i])
            stringZJunta = ''.join(stringZ[i])
        stringSerial = ''.join(['b',stringZJunta])
        self.ser.write(stringSerial)
        print('impedance test for channel', channel)
        #self.print_incoming_text()
        stringZ = ['z',1,0,0,'Z']
        return

        #Comandos do Cartão SD (SD card Commands):
        #O comando é utilizado para realizar registro por certo período de tempo das leituras feitas pela placa
        #A S F G H J K L a: cada letra destas corresponde ao tempo de aquisição de dados, que corresponde ao vetor:
        #Em minutes? 5 15 30 60 120 240 720 1440 (a = 14 segundos, pra teste)
        #A/S/F/G/H/J/K/L/a <=> 5 min./15 min./30 min./60 min./120 min./240 min./720 min./1440 min./14 segs.
        #Parar o logging e fechar o arquivo SD: j
    def generate_a_text_file_on_the_SD_card_every_5_minutes(self):
        """
        This function generates a text file with the name: OBCI_01.txt, that has its number portions increased as new text files are generated. The data has the format: Sample number / 8 values of the channels ADS1299 / 3 axis of the accelerometer LIS3DH; values are in 24-bit signed big endian for the channels, and 16-bit signed big endian for the accelerometer. This function has other variations with different, defined times for generating the text file.
        """
        print('Logging data to the SD card every 5 minutes')
        self.ser.write(b'A')
        return
    def generate_a_text_file_on_the_SD_card_every_15_minutes(self):
        '''
        This function logs data to the SD card, generating a text file every 15 minutes.
        '''
        print('Logging data to the SD card every 15 minutes')
        self.ser.write(b'S')
        return
    def generate_a_text_file_on_the_SD_card_every_30_minutes(self):
        '''
        This function logs data to the SD card, generating a text file every 30 minutes.
        '''
        print('Logging data to the SD card every 30 minutes')
        self.ser.write(b'F')
        return
    def generate_a_text_file_on_the_SD_card_every_60_minutes(self):
        '''
        This function logs data to the SD card, generating a text file every 60 minutes.
        '''
        print('Logging data to the SD card every 60 minutes')
        self.ser.write(b'G')
        return
    def generate_a_text_file_on_the_SD_card_every_120_minutes(self):
        '''
        This function logs data to the SD card, generating a text file every 120 minutes.
        '''
        print('Logging data to the SD card every 120 minutes')
        self.ser.write(b'H')
        return
    def generate_a_text_file_on_the_SD_card_every_240_minutes(self):
        '''
        This function logs data to the SD card, generating a text file every 240 minutes.
        '''
        print('Logging data to the SD card every 240 minutes')
        self.ser.write(b'J')
        return
    def generate_a_text_file_on_the_SD_card_every_720_minutes(self):
        '''
        This function logs data to the SD card, generating a text file every 720 minutes.
        '''
        print('Logging data to the SD card every 720 minutes')
        self.ser.write(b'K')
        return
    def generate_a_text_file_on_the_SD_card_every_1440_minutes(self):
        '''
        This function logs data to the SD card, generating a text file every 1440 minutes.
        '''
        print('Logging data to the SD card every 1440 minutes')
        self.ser.write(b'L')
        return
    def generate_a_text_file_on_the_SD_card_every_14_seconds(self):
        '''
        This function logs data to the SD card, generating a text file every 14 seconds.
        '''
        print('Logging data to the SD card every 14 seconds')
        self.ser.write(b'a')
        return
    def stop_logging_of_the_SD_text_file(self):
        '''
        This function interrupts the logging to the SD card by the Cyton.
        '''
        self.ser.write(b'j')
        print('ending SD card logging')
        return

        #Comandos de Stream de Dados (Stream Data Commands):
        #b :começa o streaming de dados
        #s :interrompe o streaming de dados
        #Comandos Sortidos:
        #? :lê e gera um relatório sobre todas as configurações do ADS1299 e o LIS3DH
        #ADS1299 é um conversor AD especializado para medidas de biopotencial
        #LIS3DH é um acelerômetro linear de três eixos


    #Comandos Daisy/16 Canais
        #Desonr Canais (Turn Channels OFF):
        #q w e r t y u i :desonm respectivamente os canais de 9 a 16, na ordem
        #onr Canais (Turn Channels ON):
        #Q W E R T Y U I :onm respectivamente os canais de 9 a 16, na ordem
        # As funções aceitam valores de 9 a 16
    def turn_this_daisy_channel_off(self, channel):
        '''
        This function is for turning off the channels on the Daisy module board.
        :param channel: This defines which daisy channel to turn off; the daisy channel values are: 9,10,11,12,13,14,15,16.

        '''
        daisyOff = ['q','w','e','r','t','y','u','i']
        channelOff = daisyOff[channel-9]
        serialOff = ''.join(['b',channelOff])
        self.ser.write(serialOff)
        #self.print_incoming_text()
        print('turning off Daisy channel', channel)
        return

    def turn_this_daisy_channel_on(self,channel):
        '''
        This function is for turning on the channels on the Daisy module board.
        :param channel: This defines which daisy channel to turn on; the daisy channel values are: 9,10,11,12,13,14,15,16.

        '''
        daisyOn = ['Q','W','E','R','T','Y','U','I']
        channelOn = daisyOn[channel-9]
        serialOn = ''.join(['b',channelOn])
        self.ser.write(serialOn)
        #self.print_incoming_text()
        print('turning on Daisy channel', channel)
        return

        #Número de Canais(Select maximum channel number):
        #c :Habilita somente os canais 1 a 8
        #C :Habilita todos os canais de 1 a 16
    def set_the_maximum_number_of_available_channels_as_8(self):
        '''
        This forces the use of the 8 original channels of the Cyton, preventing the connection between the Cyton and the Daisy boards.
        '''
        self.ser.write(b'c')
        print('Only original 8 channels are allowed')
        return

    def set_the_maximum_number_of_available_channels_as_16(self):
        '''
        This function allows for the use of the 16 channels, combining the Daisy board channels with the Cyton board channels.
        '''
        self.ser.write(b'C')
        print('All 16 channels are allowed')
        return

    #Comandos Firmware 2.0.0
        # Marcação do Tempo (Time Stamping):
        #< :Inicia o time stamping, sincronizando o Driver e o Host.
        #> :Para o time stamping.

    def start_time_stamping_of_data_stream(self):
        '''
        This function enables the time stamping of the data stream.

        '''
        self.ser.write(b'<')
        self.print_incoming_text()
        print('Starting Time Stamping')

        return
    def stop_time_stamping_of_data_stream(self):
        '''
        This function disables the time stamping of the data stream.

        '''
        self.ser.write(b'>')
        print('Stopping Time Stamping')
        return
    
        #Número de Rádio do channel (Get Radio Channel Number):
        #0xF0 0x00: retorna a falha ou sucesso, e o valor do host, mais o do aparelho no caso de sucesso.
        #Configurar Número do channel de Rádio (Set Radio System Channel Number):
        #0xF0 0x01 0x07: retorna a falha ou sucesso, sucesso se o host e o aparelho estiverem com o mesmo valor; também retorna em HEX o valor do channel.
        #O 0x07 é opcional, para determinar o channel, de 1 a 25 em HEX. De 0x01 a 0x19
        #Configurar Sobreposição do channel de Rádio (Set Host Radio Channel Override):
        #0xF0 0x02 0x01: retorna falha ou sucesso, força a troca de channel do Host para o channel(opcional). De 0x01 a 0x19
    def test_host_device_radio_connection(self):
        '''
        This tests if the radio connection is working between the host and the device, the Cyton board. Returns success or failure.

        '''
        self.ser.write(b'0xF0 0x00')
        return

    def test_host_device_radio_connection_and_switch_to_a_certain_channel_in_hex(self,radSet):
        '''
        This returns success or failure; success meaning the host and the board having the same channel set; failure if it doesn't. Also returns the channel's value in hex. It will change the radio to the defined channel.
        :param radSet: this parameter defines the new channel for the radio to change. Values range from 0x01 to 0x19, 25 different values.
        '''
        radioSet = ' '.join(['b','0x01',hex(radSet)])
        self.ser.write(radioSet)
        return

    def force_radio_channel_switch_to_a_certain_channel_in_hex(self,radOver):
        '''
        This function forces a channel switch, from the Host's channel to another channel. This change is optional.
        :param radOver: this parameter defines the new channel for the radio to change. Values range from 0x01 to 0x19.

        '''

        radioOver = ' '.join(['b','0x02',hex(radOver)])
        self.ser.write(radioOver)
        return

        #Obter Poll Time de Rádio(Radio Get Poll Time):
        #0xF0 0x03: retorno de pool time, pode significar erros e está associado com as capacidades do sistema. Retornado em HEX o poll time.
        #Configurar Poll Time de Rádio(Radio Get Poll Time):
        #0xF0 0x04 0x40:a terceira opção determina o poll time em HEX, são aceitos valores de 0 a 255, em ms. Padrão é de 80ms.
    def get_the_current_poll_time_in_milliseconds(self):
        '''
        returns the current pool time, it could indicate errors or dependant on the current system's capacities. It returns the value in hexadecimal.

        '''
        self.ser.write(b'0xF0 0x03')
        return
    def set_the_poll_time_in_milliseconds(self,pollSet):
        '''
        This function sets the pool time in milliseconds.
        :param pollSet: this parameter sets the poll time of data. The accepted range of values is from 0 to 255, in ms. Default value is at 80ms. Value is sent in hex.

        '''
        radioPoll = ' '.join(['b','0x04',hex(pollSet)])
        self.ser.write(radioPoll)
        return

        #Configurar o Baud Rate para o Padrão do Rádio do Host (Radio Set HOST to Driver Baud Rate to Default):
        #0xF0 0x05: configura o Baud Rate para 115200Hz.
        #Configurar o Baud Rate para Modo de Alta-Velocidade (Radio Set HOST to Driver Baud Rate to High-Speed mode):
        #0xF0 0x06: configura o Baud Rate pra 230400Hz.
        #Configurar o Baud Rate para Modo de Hiperalta-Velocidade (Radio Set HOST to Driver Baud Rate to Hyper-Speed mode):
        #0xF0 0x0A: configura o Baud Rate pra 921600Hz.
    def set_radio_baud_rate_to_115kHz(self):
        '''
        This sets the radio communications' baud rate to 230400Hz.

        '''
        self.ser.write(b'0xF0 0x05')
        return
    def set_radio_baud_rate_to_230kHz(self):
        '''
        This sets the radio communications' baud rate to 230400Hz.

        '''
        self.ser.write(b'0xF0 0x06')
        return
    def set_radio_baud_rate_to_921kHz(self):
        '''
        This sets the radio communications' baud rate to 921600Hz.

        '''
        self.ser.write(b'0xF0 0x0A')
        return

        #Relatório do Sistema de Rádio:
        #0xF0 0x07: checa o status do sistema de rádio, confirma ou nega se está operante.
    def get_radio_communication_status(self):
        '''
        This function checks the radio system's status, returning if it is operational or not.
        '''
        self.ser.write(b'0xF0 0x07')
        return

    #Comandos Firmware 3.0.0

        #Taxa de Aquisição (Sample Rate):
        #~0 : configura a taxa de aquisição, o 0 no comando pode ser alterado para os valores 0/1/2/3/4/5/6/~
        #Os valores correspondem às taxas: 16000Hz / 8000Hz / 4000Hz / 2000Hz / 1000Hz / 500Hz / 250Hz / Obter a taxa de aquisição atual
    def set_sample_rate_of_channels_to_16kHz(self):
        '''
        This sets the sample rate of the Cyton's voltage channels to 16000Hz. These sample rates can alter the sampling if you're using the SD card method; if it's through over-air data transfer, the sample rate is locked at 250Hz, unless the Wifi Shield hardware is used.

        '''

        self.ser.write(b'~0')
        print('Sample Rate: 16000Hz')
        return
    def set_sample_rate_of_channels_to_8kHz(self):
        '''
        This sets the sample rate of the Cyton's voltage channels to 8000Hz.

        '''
        self.ser.write(b'~1')
        print('Sample Rate: 8000Hz')
        return
    def set_sample_rate_of_channels_to_4kHz(self):
        '''
        This sets the sample rate of the Cyton's voltage channels to 4000Hz.

        '''
        self.ser.write(b'~2')
        print('Sample Rate: 4000Hz')
        return
    def set_sample_rate_of_channels_to_2kHz(self):
        '''
        This sets the sample rate of the Cyton's voltage channels to 2000Hz.

        '''
        self.ser.write(b'~3')
        print('Sample Rate: 2000Hz')
        return
    def set_sample_rate_of_channels_to_1kHz(self):
        '''
        This sets the sample rate of the Cyton's voltage channels to 1000Hz.

        '''
        self.ser.write(b'~4')
        print('Sample Rate: 1000Hz')
        return
    def set_sample_rate_of_channels_to_500Hz(self):
        '''
        This sets the sample rate of the Cyton's voltage channels to 500Hz.

        '''
        self.ser.write(b'~5')
        print('Sample Rate: 500Hz')
        return
    def set_sample_rate_of_channels_to_250Hz(self):
        '''
        This sets the sample rate of the Cyton's voltage channels to 250Hz.

        '''
        self.ser.write(b'~6')
        print('Sample Rate: 250Hz')
        return
    def get_current_sample_rate(self):
        '''
        This function returns the current sample rate set for the board.
        '''
        self.ser.write(b'~~')
        print('current sample rate')
        self.print_incoming_text()
        return

        #Modo da Placa (Board Mode):
        #/0 : configura o modo da placa, o 0 no comando pode ser alterado para os valores 0/1/2/3/4//
        #Os valores correspondem as modos: Padrão / Modo Debug / Modo Analógico / Modo Digital / Modo Marcador / Obter o modo de aquisição atual
    def set_the_cytons_board_mode_to_default_mode(self):
        '''
        This sets the Cyton's board mode to Default Mode. This makes it som that you can send accelerometer data to the auxiliary bytes on the stream or through the .txt file.
        '''
        self.ser.write(b'/0')
        self.print_incoming_text()
        print('Default mode')
        return
    def set_the_cytons_board_mode_to_debug_mode(self):
        '''
        This function sets the Cyton's board mode to Debug mode. This makes it so the board sends marked signals through its output, so it can be user for debugging purposes.
        '''
        self.ser.write(b'/1')
        self.print_incoming_text()
        print('Debug mode')

        return
    def set_the_cytons_board_mode_to_analog_mode(self):
        '''
        This sets the Cyton's board mode as Analog Mode. What this does is that it reads the analog pins A5 and A6; if the Wifi Shield is not present it will also read the A7 pin.

        '''
        self.ser.write(b'/2')
        self.print_incoming_text()
        print('Analog mode')
        return
    def set_the_cytons_board_mode_to_digital_mode(self):
        '''
        This sets the Cyton's board mode as Digital Mode. What this does is that it reads the inputs in the D11, D12 and D17 pins; if the Wifi Shield is not present it will also read the D13 and D18 pins. These pins can be seen on the spreadsheet of the Cyton Board.

        '''
        self.ser.write(b'/3')
        self.print_incoming_text()
        print('Digital mode')
        return
    def set_the_cytons_board_mode_to_marker_mode(self,x):
        '''
        This function sets the Cyton's board mode as Marker Mode. This will make it so that the accelerometer data is substituted with "_x_", this can be used for marking the position of the accelerometer data in the stream or on the generated text file.
        '''
        self.ser.write(b'/4')
        self.print_incoming_text()
        print('Marker mode')
        return
    def get_current_mode_of_the_cyton_board(self):
        '''
        For getting in which mode the  Cyton board is in, from the ones established before.
        '''
        print('the current board mode is:')
        self.ser.write(b'//')
        self.print_incoming_text()

        return


        #Comandos do Shield de Wifi (Wifi Shield Commands):
        #{ : Faz uma tentativa de se sincronizar com shield de Wifi, retorna o sucesso ou falha.
        #} : Tenta remover o shield de Wifi, retorna sucesso ou falha da operação.
        #: : Obtém o status do shield de Wifi, se está presente ou não.



    def try_to_sync_the_wifi_shield(self):
        '''
        Function for attempting to desync the Wifi Shield module.

        '''
        print('Tentativa de sincronização de Wifi Shield')
        self.ser.write(b'{')
        self.print_incoming_text()

        return
    def try_to_desync_the_wifi_shield(self):
        '''

        Function for attempting to desync the Wifi Shield module.

        '''
        print('desyncing Wifi Shield')
        self.ser.write(b'}')
        self.print_incoming_text()
        return
    def detect_if_the_wifi_shield_is_present(self):
        '''
        This returns with a status report on the WiFi Shield, if it's detected or not.
        '''
        print('detection of Wifi Shield')
        self.ser.write(b':')
        self.print_incoming_text()
        return
    def reset_the_wifi_shield_board(self):
        '''
        This function resets the Wifi Shield.
        '''
        print('resetting WiFi Shield')
        self.ser.write(b':')
        self.print_incoming_text()
        return
    def activate_60Hz_lowpass_filter(self):
        '''
        This activates the internal filter of the Cyton, it's a 60Hz low-pass filter, applied to the 8 channels.

        '''
        print('activating 60Hz low pass filter')
        self.ser.write(b'f')
        self.filtering_data = True

    def deactivate_60Hz_lowpass_filter(self):
        '''
        This deactivates the internal filter of the Cyton, it's a 60Hz low-pass filter, applied to the 8 channels.
        '''
        print('deactivating 60Hz low pass filter')
        self.ser.write(b'g')
        self.filtering_data = False

    def get_version_of_firmware_on_cyton(self):
        '''
        This function returns through the serial the version on the firmware that is on the OpenBCI Cyton Board.
        '''
        print('getting firware version')
        self.ser.write(b'V')

    def report_of_the_current_settings_ads_and_lis(self):
        '''
        This generates a report similar to the one present in newCyton.py's __init__ function, exposing things such as the version number of the firmware, and  the all the settings of the ADS1299 and the LIS3DH; which are the specialized AD converter for biopotential, and a 3-dimensional accelerometer, respectively.
        '''
        print('Current settings report')
        time.sleep(0.5)
        self.ser.write(b'?')
        self.print_incoming_text()

        return
        #v :"soft reset" da placa Cyton
    def do_a_soft_reset_of_the_cyton(self):
        '''
        This function does a soft reset of the Cyton board, resetting the streaming and reverting settings to default.
        '''
        print('Soft reset of the Cyton')
        self.ser.write(b'v')
        return
    def print_the_bytes_on_the_serial(self):
        '''
        Function for printing bytes of data, sent by the OpenBCI Cyton Board.
        '''
        if not self.streaming:
            self.ser.write(b'b')
            self.streaming = True
        while self.streaming:
            print(struct.unpack('B', self.ser.read())[0])


    def stop_the_streaming_sent_from_the_Cyton_Board(self):
        '''
        For stopping the stream of data sent by the OpenBCI Cyton Board.
        '''
        self.stop()
        self.streaming = False
        return
