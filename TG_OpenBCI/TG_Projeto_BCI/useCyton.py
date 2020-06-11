"""
useCyton.py
==================
Módulo final, com interface para controle da placa.

newCyton é importado para ter suas funções utilizadas; sendo simplificado para x.

Para usar as funções, seguir/observar os exemplos com as funções comentadas abaixo.

Notas:

* O comando sdStop() finaliza a coleta de dados, portanto deve ser usado um timer se desejar usar esta função.
* O cartão não necessita ficar o tempo estipulado integralmente, o SD pode ser removido antes de atingir o tempo "correto"; os registros serão mantidos retirando-se o cartão com a placa ligada ou desligando a placa.
* Se estiver utilizando o Dongle USB, ao invés da placa WiFi, a taxa de aquisição ficará restrita a 250Hz. os comandos para alterar esta taxa estão definidos em newCyton.py, porém não foram testados devido à placa não estar disponível.
* Após aquisição dos dados, é recomendado a utilização de filtro rejeita-faixa de 50 ou 60Hz, dependendo da rede elétrica; também é recomendado um filtro passa-faixa, entre 0.5 e 45Hz, é a faixa em que normalmente está o EEG.
* Os dados estarão em hexadecimal, com a primeira coluna sendo o número da amostra; as 8 colunas seguintes são os valores obtidos dos canais de 1-8 de ADS1299; além destes haverão 3 colunas seguintes, estas correspondem ás acelerações em x,y e z do LIS3DH, fixo em 50Hz.
* No rodapé estarão disponíveis outras informações como o tempo de aquisição.
* O dado em hexadecimal corresponde a valores de 24 bits.
* O ganho deve ser considerado na fórmula: Fator de Escala (Volts/amostra) = 4.5 Volts / gain / (2^23 - 1); isto deve ser aplicado aos valores
convertidos de 32-bits signed, após ser feita a conversão dos 24-bits signed fornecido pela placa. Esta conversão está incluída no arquivo que processa
 a os arquivos de texto.
* Caracteres não utilizados: 9 ( ) _ o O f g h k l ‘ “ n N M , . (space)
"""

import newCyton as nCyton
import time

x=nCyton.newCyton()


#x.sample16k()
#x.test2xAmpSlow()

x.sdTime15m()

x.configCanal(canal = 1,liga = 1,ganho = 24,tipo = 'normal',BIAS = 1,SRB2 = 0,SRB1 = 0)
time.sleep(2)
x.configCanal(canal = 2,liga = 1,ganho = 24,tipo = 'normal',BIAS = 1,SRB2 = 0,SRB1 = 0)
time.sleep(2)
x.configCanal(canal = 3,liga = 1,ganho = 24,tipo = 'normal',BIAS = 1,SRB2 = 0,SRB1 = 0)
time.sleep(2)
x.configCanal(canal = 4,liga = 1,ganho = 24,tipo = 'normal',BIAS = 1,SRB2 = 0,SRB1 = 0)
time.sleep(2)
x.configCanal(canal = 5,liga = 0,ganho = 24,tipo = 'normal',BIAS = 1,SRB2 = 0,SRB1 = 0)
time.sleep(2)
x.configCanal(canal = 6,liga = 0,ganho = 24,tipo = 'normal',BIAS = 1,SRB2 = 0,SRB1 = 0)
time.sleep(2)
x.configCanal(canal = 7,liga = 0,ganho = 24,tipo = 'normal',BIAS = 1,SRB2 = 0,SRB1 = 0)
time.sleep(2)
x.configCanal(canal = 8,liga = 0,ganho = 24,tipo = 'normal',BIAS = 1,SRB2 = 0,SRB1 = 0)

#x.sdTime14s() #Tempo para coleta de dados do cartão SD de 14 segundos
#x.sdTime5m() #Tempo para coleta de dados do cartão SD de 5 minutos

#x.sdStop()
#x.getSampleRate()
#x.sdTime14s()


#x.sample4k()
#x.startText()
#x.adslisRelatorio()
#x.test1xAmpSlow()
#x.sdStop()
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
#x.sdTime14s()
#x.test2xAmpSlow()
#x.sdTime14s()
#x.test2xAmpFast()

#x.configCanal(2,0,3,1,1,0,1)
#x.configCanal(3,0,4,0,0,1,1)

#x.escolher_Ganho(1, 12)
#x.escolher_Input(2, 'normal')
#x.ativar_BIAS(3, False)
#x.testGND()
#x.padraoRelatorio()
#
#x.myStopStreaming()