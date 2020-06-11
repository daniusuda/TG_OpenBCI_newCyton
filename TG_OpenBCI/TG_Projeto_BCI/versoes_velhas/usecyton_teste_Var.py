import newCyton as nCyton


x=nCyton.newCyton()
#x.softReset()
x.sdTime14s()
x.configCanal(1,0,6,0,0,0,0) #canal 1, ligado, ganho = 12, tipo 'normal', BIAS desligado, SRB2 desligado, SRB1 desligado 
x.configCanal(2,0,6,0,0,0,0)
x.configCanal(3,1,6,0,0,0,0) #canal 3, ligado, ganho = 6, tipo 'normal', BIAS desligado, SRB2 desligado, SRB1 desligado  
x.configCanal(4,1,6,0,0,0,0)
x.configCanal(5,1,6,0,0,0,0) #canal 5, ligado, ganho = 3, tipo 'normal', BIAS desligado, SRB2 desligado, SRB1 desligado  
x.configCanal(6,1,6,0,0,0,0) #canal 6, ligado, ganho = 2, tipo 'normal', BIAS desligado, SRB2 desligado, SRB1 desligado  
x.configCanal(7,1,6,0,0,0,0)
x.configCanal(8,1,6,0,0,0,0)

#x.sdStop()
