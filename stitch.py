import struct

f=open(input('Enter filename 1: '), 'rb')
a = f.read(); f.close()

f=open(input('Enter filename 2: '), 'rb')
b = f.read()[40:]; f.close()

c = open(input('Enter outuput file: '), 'wb')

c.write( a )
c.write( b )

c.seek(4)
c.write( struct.pack( '<l', len(a) + len(b) - 8 ) )

c.seek(40)
c.write( struct.pack( '<l', len(a) + len(b) -44 ) )

c.close()

print("[+] Successful stitch.")
