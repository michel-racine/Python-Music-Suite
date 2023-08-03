# Name:		phasor.py
# Purpose:	This program generates a phased copy of user input file. The right channel is shifted by a
# 		user specified amount
# Author:	Michael Root
# Date:		2023.07.26

import struct

f=open(input('Enter filename: '), 'rb')
a = f.read(); f.close()
c = open(input('Enter output file: '), 'wb')
c.write(a[0:44])  ### output will be same size as input file, we will just reuse a's header.
shift = int(input("Enter shift amount in samples: "))

B = []
for i in range(44, len(a), 4):
    B.append(struct.unpack('<hh', a[i:i+4])[0])
"""
for b in B:
  if b > 32767:
    b = 32767
  elif b < -32767:
    b = -32767
"""
### This is where phasor magic happens
B1 = []
for i in range(len(B)):
	if i < shift:
		B1.append(0)
	else:
		B1.append(B[i - shift]);

for i in range(len(B)):
	c.write(struct.pack('<hh', B[i], B1[i]))

c.close()


print("[+] Successful phasor actions.")
