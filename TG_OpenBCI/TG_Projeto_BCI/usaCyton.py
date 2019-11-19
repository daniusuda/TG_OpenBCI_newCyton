"""
usaCyton.py
==================
Módulo final, com interface para controle da placa.
"""
#arquivo de exemplo para se utilizar a placa com os novos comandos de newCyton
import newCyton as nCyton

#This is about big_func1.
"""  
:param abra: abra number. 
:param cadabra: cadabra number.
:param sesame: sesame information.
:return ret_val: result information.
:rtype: int.
"""

x=nCyton.newCyton()

x.sdTime14s()

x.test1xAmpSlow()
x.sdTime14s()
x.test1xAmpFast()
x.sdTime14s()


#x.sample4k()
#x.startText()
#x.adslisRelatorio()
#x.test1xAmpSlow()
#x.print_bytes_in()
#x.readSample()
#x.streamStart()
#x.start_streaming(3000,-1)
#x.read_serial_binary(3000)
#x.streamStart()

#x.test2xAmpFast()
#x.ligar_Canal(2, liga=0)
#x.ligar_Canal(3, liga=1)
#x.sdTime5m()
#x.sdStop()
#x.configCanal(2,0,3,1,1,0,1)
#x.configCanal(3,0,4,0,0,1,1)
#x.escolher_Ganho(1, 12)
#x.escolher_Input(2, 'normal')
#x.ativar_BIAS(3, False)
#x.testGND()
#x.padraoRelatorio()
#
#x.myStopStreaming()