import newCyton as nCyton
import time 

x=nCyton.newCyton()
x.sdTime14s()
x.self.ser.write(b'x1060100X')
x.configCanal(1,1,24,'normal',1,0,0)
time.sleep(0.5)
x.configCanal(2,1,24,'normal',1,0,0)
time.sleep(0.5)
x.configCanal(3,1,24,'normal',1,0,0)
time.sleep(0.5)
x.configCanal(4,1,24,'normal',1,0,0)
time.sleep(0.5)
x.configCanal(5,0,24,'normal',1,0,0)
time.sleep(0.5)
x.configCanal(6,0,24,'normal',1,0,0)
time.sleep(0.5)
x.configCanal(7,0,24,'normal',1,0,0)
time.sleep(0.5)
x.configCanal(8,0,24,'normal',1,0,0)
time.sleep(0.5)
#time.sleep(1)
#x.printPackets()
