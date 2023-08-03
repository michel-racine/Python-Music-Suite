# Name:		display.py
# Purpose:	Creates a graph of wave amplitudes for .wav sample
# Author:	Michael Root
# Date:		2023.08.03

import wave, struct, math, random
from PIL import Image

img = Image.new('RGB', (1800,400), "black")
pix = img.load()
a = b""

# Get file stripped of header
with open(input("Input file: "), "rb") as f:
	a = f.read()[44:]

total_samples = len(a) / 2
reduction_range = total_samples / 1800


# Important byte array
B=[]

for b in range(0, int(total_samples), 4):
  vals = struct.unpack("<hh", a[b: b + 4])
  for val in vals:
    B.append(val)

reduction_range = len(B)/1800

# Map wave amplitudes to image y values along x axis.
# It will make sense when you see the output.
for x in range(1800):
    val = B[x * int(reduction_range)]
    display_y = int((val / 170)) + 200
    if val > 0:
        for p in range(200, display_y):
            pix[x, p] = (255, 0, 0)
    if val < 0:
        for p in range(200, display_y, -1):
            pix[x, p] = (255, 0, 0)

img = img.save("display.png")

