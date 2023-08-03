# Name:		meld.py
# Purpose:	Combines or mixes two .wav files together. The length of the output
#		should default to the length of the smaller file

import struct


with open(input('Enter filename 1: '), 'rb') as f:
	a = f.read()
with open(input('Enter filename 2: '), 'rb') as f:
	b = f.read()
c = open(input('Enter outuput file: '), 'wb')

c.write(a[0:44])

for i in range(44, len(a), 4):
	a_tup = struct.unpack('<hh', a[i:i+4])
	b_tup = struct.unpack('<hh', b[i:i+4])

	aL = a_tup[0]
	aR = a_tup[1]
	bL = b_tup[0]
	bR = b_tup[1]

	# Our melding process lol
	if (aL >= 0 and bL <= 0) or (aL <= 0 and bL >= 0):
		cL = (aL + bL)
	elif aL > 0:
		cL = aL + (bL / 32768) * (32768 - aL)
	elif bL < 0:
		cL = aL + (-bL / 32768) * (-32768 - aL)

	if (aR >= 0 and bR <= 0) or (aR <= 0 and bR >= 0):
		cR = (aR + bR)
	elif aR > 0:
		cR = aR + (bR / 32768) * (32768 - aR)
	elif bL < 0:
		cR = aR + (-bR / 32768) * (-32768 - aR)


	c.write(struct.pack('<hh', int(cL), int(cR)))

c.close()

print("[+] Successful meldage.")





 
