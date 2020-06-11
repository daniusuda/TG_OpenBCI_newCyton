import newCyton as nCyton
import time 

x=nCyton.newCyton()
x.sdTime14s()
x.ser.write(b'x1060100X')
x.ser.write(b'x2060100X')

x.ser.write(b'x3060100X')

x.ser.write(b'x4060100X')

x.ser.write(b'x5160100X')

x.ser.write(b'x6160100X')

x.ser.write(b'x7160100X')

x.ser.write(b'x8160100X')
