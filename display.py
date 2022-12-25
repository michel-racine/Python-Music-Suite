import wave, struct, math, random
from PIL import Image # might need to use: pip install pillow

img = Image.new('RGB', (1200,400), "black")
pix = img.load()
y = 0

f = open(input("Input file: "), "rb")
a = f.read()[44:]; f.close()
total_samples = len(a) / 2
reduction_range = total_samples / 1200

B=[]
for b in range(0, int(total_samples), 4):
  vals = struct.unpack("<hh", a[b: b + 4])
  for val in vals:
    B.append(val)

reduction_range = len(B)/1200

for x in range(1200):
    val = B[x * int(reduction_range)]
    display_y = int((val / 200)) + 200
    if val > 0:
        for p in range(200, display_y):
            pix[x, p] = (255, 0, 0)
    if val < 0:
        for p in range(200, display_y, -1):
            pix[x, p] = (255, 0, 0)

img = img.save("display.png")

