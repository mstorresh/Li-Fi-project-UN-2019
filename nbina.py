def toBinary(string):
    return "".join([format(ord(char),'#010b')[2:] for char in string])
    
def toString(binaryString):
    return "".join([chr(int(binaryString[i:i+8],2)) for i in range(0,len(binaryString),8)])
	
def binarizar(decimal):
    binario = ''
    while decimal // 2 != 0:
        binario = str(decimal % 2) + binario
        decimal = decimal // 2
    if len(binario)!=8:
		if len(binario)==6:
			return str(0) + str(decimal) + binario
		elif len(binario)==7:
			return str(decimal) + binario
    else:
		return str(decimal) + binario	
s=500
h=binarizar(s)
print(h)
for i in range(len(h)):
	if h[i]=="1":
		print(1)
cantidad = str(raw_input("escriba su nombre: "))
print (cantidad)
if cantidad == "gris":
	print("hhhh")
if cantidad == "color":
	print("lol")
#print(binarizar(s))
#print(int(binarizar(s),2))
#h=bin(64)
#i="2"
#print(h[0])
#l=toString(h)
#print(dec_to(64,2))
#r="".join([s,i])
#print(r)
#print(bin(6464))
