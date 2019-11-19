i = [1,2,3]
i[1] = 'x'
i[1] = str(i[1])
print(i)
s = i*3
print(s[0])
print(s[1])
print(s[2])
print(s[3])
r = input('numeros')
r.replace(' ', '')
a  = [int(i) for i in str(r)]
#print(len(r))
#r.split(',')
print(r)
print(a)