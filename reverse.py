import struct

f=open(input('Enter filename: '), 'rb')
a = f.read(); f.close()

c = open(input('Enter output file: '), 'wb')
c.write( a[0:44] )  ### output will be same size as input file, we will just reuse a's header.


for i in range(len(a), 44, -4):
  c.write( a[i-4:i] )

c.close()


print("[+] Successful reversion.")




