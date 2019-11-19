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

        # Take user input
        # s = input('--> ')
        #sys.hexversion determina  a versao do python e entao seleciona-se o codigo correspondente para o input
        #A partir do python 3.0.0 utiliza-se o input() no lugar de raw_input() 0x03000000 se refere
        #a isso
        #o s neste caso vai diretamente para a string que é enviada e se comunica com a placa cyton
        #para melhorar a interface, fazer primeiro texto de explicação, em vez dos comandos diretos de s, obter
        #as strings fornecidas pelo usuario para então alterar o string "s" que é mandado
        print('Input desejado:')
        if sys.hexversion > 0x03000000:
            s = input('--> ')
        else:
            s = raw_input('--> ')
    
        
