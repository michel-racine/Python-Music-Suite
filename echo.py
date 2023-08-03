# Name:		echo.py
# Purpose:	Applies echo effect to input .wav file using magical formula.
#		This version is much improved over previous versions, maintains stereo integrity
# Author:	Michael Root
# Date:		2023.08.02

import struct

def clip(b):
	"""
	Primitive clipping function, brutal.
	"""
	if b > 32767:
		b = 32767
	elif b < -32767:
		b = -32767
	return b


f=open(input('Enter filename: '), 'rb')
a = f.read(); f.close()
c = open(input('Enter output file: '), 'wb')
c.write(a[0:44])  ### output will be same size as input file, we will just reuse a's header.

# Left and right channel arrays
Bl = []
Br = []

# Unpack bytes from file and place them in respective arrays for easy processing.
for i in range(44, len(a), 4):
	Bl.append(struct.unpack('<hh', a[i:i+4])[0])
	Br.append(struct.unpack('<hh', a[i:i+4])[1])

# Magic number reverb happens here. Just sounds cool.
for b in range(len(Bl)):
	for i in range(1,19,7):
		if b + i * 4000 < len(Bl):
			Bl[b + i * 4000] += Bl[b] / (i * 5.7)

# and here for right channel
for b in range(len(Br)):
	for i in range(1,19,7):
		if b + i * 4000 < len(Br):
			Br[b + i * 4000] += Br[b] / (i * 5.7)

# Pack all the bytes into the file. Working, but can improvel
for i in range(len(Bl)):
	bl = clip(Bl[i])
	br = clip(Br[i])
	c.write(struct.pack('<hh', int(bl), int(br)))

c.close()

print("[+] Successful echo echo.")


