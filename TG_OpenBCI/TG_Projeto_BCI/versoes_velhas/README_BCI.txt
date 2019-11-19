Iniciar o arquivo novouser.py
pré-requisitos: Python 2.7, Numpy 1.7(para uso de funções matemticas), pySerial(para mandar serial)

Do arquivo novouser.py:

Funções:

"-p" para se obter a porta serial, é feita tentativa de obtê-la
"--no-filtering" desativa o filtro rejeita-faixa
"-d" força o modo Daisy de 16 canais
"-x" ativa a entrada AUX(auxiliar)
"--log" para criar um log do próprio programa ao ser executado

Comunicação com a placa:

x0000000X:

"x0000000X" a principal função, que envia uma string que inclui as seguintes configurações,
dependendo da posição na string, versão mais completa de alguns dos comandos abaixo na lista:
-x e X são os bytes de início e final da string para se comunicar com a placa

Canais(CHANNEL):

-a primeira posição é um int(desconsiderando a placa Daisy, que torna utiliza caracteres como Q e R)
nos valores de 1-8 correspondentes aos canais da placa, por exemplo: "x2000000X" seleciona
o canal 2 para que este seja configurado com os outros 6 valores, que são int. Sem valor padrão pois
trata-se da seleção do canal.
Desligar(POWER_DOWN):

-a segunda posição é referente a ligar ou não o canal, um valor de "1" significa ter o canal desligado   
, exemplo: "x1100000X" seleciona o canal 1 o desativa pelo valor "1" na segunda posição.Valor "0" é o padrão.

Ganho(GAIN_SET):

-a terceira posição é para determinação do ganho a ser aplicado ao sinal, os valores 0-4 correspondem a
 2*n de ganho para n ser o valor escolhido, exceto 5 e 6, respectivamente são ganho 12 e 24, exemplo: "x0040000X" 
torna o ganho 8, valor 6, de ganho 24 é o padrão.

Tipo de input(INPUT_TYPE_SET):

-a quarta posição é para determinar o tipo de input para o canal conversor de analógico para digital,são 8 os tipos:
"0" é o normal, "1" é em curto, "2" é para realizar medição da voltagem de BIAS, "3" é MVDD, medição de 
VDD("drain"/supply voltage, é a voltagem da fonte de alimentação) com o ADC(analog-to-digital converter),
"4" para medição de temperatura, "5" para avaliar o sinal de teste, "6" para o Drain BIAS positivo, e "7" para o 
Drain BIAS negativo.

Gerador de BIAS(BIAS_SET):

-a quinta posição determina para "0" incluir no sinal o gerador de BIAS, uma corrente DC sobre o sinal
, para "1" é incluído esse sinal, exemplo: "x0000100X" desativa o BIAS."1" é o padrão. 

Pino positivo SRB2(SRB2_SET):

-a sexta posição é para determinar a conexão dos canais P, positivos do canal especificado com o pino SRB2, 
une as voltagens do input."0" desconecta o input do pino, "1" o conecta; exemplo: "x0000000X" tem SRB2 ativo
. "1" é o padrão.

Pino negativo SRB1(SRB1_SET):

-a sétima posição é para determinar a conexão dos canais N, negativos do canal especificado com o pino SRB1, 
une as voltagens do input."0" desconecta o input do pino, "1" o conecta.exemplo: "x0000001X" tem SRB2 inativo
. "1" é o padrão.

Tabela de inputs possíveis para o x0000000X(nas posições dos zeros):
 x
 1º0 Canais 1/2/3/4/5/6/7/8
 2º0 Desligado 1/0 (Ligado(padrão)/desligado)
 3º0 Ganho 0/1/2/3/4/5/6 (1,2,3,4,6,12,24)
 4º0 Tipo de Input 0/1/2/3/4/5/6/7 (normal(padrão), curto, BIAS, fonte de alimentação, temperatura, sinal de teste, BIAS positivo, BIAS negativo)
 5º0 BIAS 1/0 (Desligado/Ligado(padrão))
 6º0 SRB2 1/0 (Desligado/Ligado(padrão))
 7º0 SRB1 1/0 (Desligado(padrão)/Ligado)
 X

Do arquivo cyton.py, os comandos originais e descrição básica:

Geral:

"v" inicializa a board Cyton 32-bits
"V" retorna a versão do firmware da placa em questão
"b" é o comando padrão para iniciar o streaming, "start" pode ser utilizado também
"s" é o comando padrão para parar o streaming, "stop" pode ser utilizado também
"?" é o comando que imprime as configurações atuais da placa

Filtro: 

"f" habilita um filtro rejeita-faixa de 60Hz embutido
"g" desabilita o filtro 

Sinais pré-configurados de teste:

"0" todos os pinos conectados ao terra
"p" todos os pinos conectados ao Vcc
"-" todos os pinos conectados ao sinal com amplitude 1x, baixa frequência
"=" todos os pinos conectados ao sinal com amplitude 1x, alta frequência
"[" todos os pinos conectados ao sinal com amplitude 2x, baixa frequência
"]" todos os pinos conectados ao sinal com amplitude 2x, alta frequência

Habilitar/desabilitar sinais:

"!,@,#,$,%,^,&,*" correspondem a habilitar os canais 1-8
"1,2,3,4,5,6,7,8" correspondem a desabilitar os canais 1-8
"d" volta as configurações para os padrões
"D" retorna o estado das configurações-padrão

Cartão SD:

"A,S,D,F,G,H,J,K,L" correspondem a 5,15,30,60,120,240,720,1440(minutos)
						1,2,4,12,24(horas)

Para a Daisy:

"Q,W,E,R,T,Y,U,I" correspondem a habilitar os canais 9-16, respectivamente
"q,w,e,r,t,y,u,i" correspondem a desabilitar os canais 9-16, respectivamente
 
Algumas Notas:

Há comandos para a impedância inicial, com respostas da placa, porém não implementado para Cyton com o código atual, algo que pode ser expandido.

Também estão presentes na documentação e nos códigos para firmwares mais avançados que o Cyton, portanto não foram adicionados, mas estes podem ser
consultados em "https://docs.openbci.com/OpenBCI%20Software/04-OpenBCI_Cyton_SDK" na seção "Firmware v2.0.0 New Commands" em diante.

Várias das funções utilizam também combinações destes comandos mandados por serial,
por exemplo o "reconnect", que utiliza um comando de stop, seguido de "v" e "b" para
realizar automaticamente o reinício do streaming