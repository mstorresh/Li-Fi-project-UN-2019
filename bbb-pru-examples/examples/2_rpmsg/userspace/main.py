import struct

f=open("/dev/rpmsg_pru30","rb+",buffering=0)


format="ii"
b=struct.pack(format,3,4) 
sb=struct.calcsize(format) #= len(b)
f.write(b)
rb=f.read(sb)
a,b=struct.unpack(format,rb)
print(a,b)
f.close()

