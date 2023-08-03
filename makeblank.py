# Name:		makeblank.py
# Purpose:	Creates an "empty" .wav file which can be melded to imported .wav files
#		which may have a header length different than 44 in order to convert them
#		to 44 byte header size for compatibility.
# Author:	Michael Root
# Date:		2023.07.23

import wave, struct, math, random

sample_rate = 44100.0
save_to = input("[+] save to file: ")
wavef = wave.open(save_to,'wb')
wavef.setnchannels(2)
wavef.setsampwidth(2)
wavef.setframerate(sample_rate)

# make array to store sample bits
B = [0.0] * 176400

for b in B:
    wavef.writeframesraw(struct.pack('<hh', 1, 1))

wavef.close()

