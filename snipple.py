import struct


f=open(input('Enter filename 1: '), 'rb')
a = f.read(); f.close()
c = open(input('Enter outuput file: '), 'wb')

print("DATA BYTE LENGTH (minus header):", len(a) - 44)

q1 = int(input("enter start byte: ")) + 44
q2 = int(input("enter end byte  : ")) + 44
diff = q2 - q1
print(diff)

c.write(a[0:44])
c.write(a[q1:q2])

c.seek(4)
c.write(struct.pack('<l', 44 + diff - 8))

c.seek(40)
c.write(struct.pack('<l', diff ))

c.close()

print("[+] Successful stitch.")





 
