#de quiser fazer manualmente
#x0000000X
#'x' e 'X' correspondem ao início e ao fim das strings a serem enviadas
#a primeira posição numérica significa o canal a ser escolhido. Na placa estão numerados os 8 canais 
#como N1P, N2P, N3P, N4P, N5P, N6P, N7P, N8P
#
#a segunda posição numérica significa ligar ou não o canal. O canal será ligado para valor 0(padrão), 1 para não ligar.
#
#a terceira posição numérica significa escolha do ganho. Os valores entre número e ganho são: 0 -> ganho 1, 1 -> ganho 2, 2 -> ganho 3,
#3 -> ganho 4, 4 -> ganho 6, 5 -> ganho 12, 6 -> ganho 24.
#
#a quarta posição numérica significa o tipo de input selecionado para o canal.
#Tipos: normal, curto, BIAS, fonte, temperatura, sinalteste, BIASpos, BIASneg
#
#a quinta posição numérica significa ativar o BIAS para o canal selecionado.
#
#a sexta posição numérica significa ativar o SRB1 para o canal selecionado.
#
#a sétima posição numérica significa ativar o SRB2 para o canal selecionado.
#
#string de exemplo:
#a string acima será portando do canal para o ganho