import struct

f=open(input('Enter filename: '), 'rb')
a = f.read(); f.close()
c = open(input('Enter outuput file: '), 'wb')
c.write(a[0:44])  ### output will be same size as input file, we will just reuse a's header.

B = []

for i in range(44, len(a), 4):
    B.append(struct.unpack('<hh', a[i:i+4])[0])

for b in range(len(B)):
  for i in range(1,19,7):
    if b + i * 4000 < len(B):
      B[b + i * 4000] += B[b] / (i * 5.7)

for b in B:
  if b > 32767:
    b = 32767
  elif b < -32767:
    b = -32767

  c.write(struct.pack('<hh', int(b), int(b)))

c.close()


print("[+] Successful echo echo.")


