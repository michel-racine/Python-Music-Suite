# Name:		makebeat.py
# Purpose:	Generate simple dope beat.
# Author:	Michael Root
# Date:		2023.07.23

import wave, struct, math, random

sample_rate = 44100.0
save_to = input("[+] save to file: ")
wavef = wave.open(save_to, 'wb')
wavef.setnchannels(2) # Stereo
wavef.setsampwidth(2)
wavef.setframerate(sample_rate)

# Factor by which to divide final output amplitude
# Is basically volume for output (but inverse).
DAMPEN = 3.5

# special function to "add" amplitudes in lieu of proper solution
def add_B(locatino, y):
    u = B[locatino]
    B[locatino] = u + (32767 - u) / 32767.0 * y

# BASS DRUM SETUP
f_bd = 200.0
theta_bd = 0.0
wavelen_bd = 0.0
y_bd = 0.0
r_bd = 30000

# HI-HAT plotter
def plot_hh(trigger):
    f_hh = 200.0
    theta_hh = 0.0
    wavelen_hh = 0.0
    y_hh = 0.0
    r_hh = 25000
    for bit in range(5000):
        r_hh = ((bit - 5000.0) / 5000) ** 2 * 30000
        f_hh = random.randint(10000, 15000) * 1.0
        wavelen_hh = sample_rate / f_hh
        theta_inc_hh = 2 * math.pi / wavelen_hh
        y_hh = r_hh * math.cos(theta_hh)
        theta_hh += theta_inc_hh
        B[bit + trigger] += y_hh

# OPEN HI-HAT plotter
def plot_open_hh(trigger):
    theta_hh = 0; r_hh = 30000.0
    for bit in range(5000):
        f_hh = random.randint(10000, 15000) * 1.0
        wavelen_hh = sample_rate / f_hh
        theta_inc_hh = 2 * math.pi / wavelen_hh
        y_hh = r_hh * math.cos(theta_hh)
        theta_hh += theta_inc_hh
        B[bit + trigger] += y_hh

# SNARE DRUM plotter
def plot_snare(trigger):
    f_sd = 200.0
    theta_sd = 0.0
    wavelen_sd = 0.0
    y_sd = 0.0
    r_sd = 30000
    theta_sd = 0.0
    theta_inc_sd = 0.0
    wavelen_sd = 0.0
    y_sd = 0.0
    r_sd = 30000
    for bit in range(5000):
        r_sd = ((bit - 5000.0) / 5000)**2 * 30000
        f_sd = random.randint(-2440, 6000) * 1.0
        wavelen_sd = sample_rate / (f_sd + 0.000000001)
        theta_inc_sd = 2*math.pi / wavelen_sd
        y_sd = r_sd * math.cos(theta_sd)
        theta_sd += theta_inc_sd
        add_B(bit + trigger, y_sd)

# Important array to store wave amplitudes for each sample
B = [0.0] * 176400

# Write bass drums
for bit in range(5000):
    r_bd = ((bit - 5000.0) / 5000)**2 * 30000
    f_bd = ((bit - 5000.0) / 5000)**2 * 200
    wavelen_bd = sample_rate / f_bd
    theta_inc_bd = 2 * math.pi / wavelen_bd
    y_bd = r_bd * math.cos(theta_bd)
    theta_bd += theta_inc_bd
    for i in range(8):
        add_B(bit + (i * 22050), y_bd)


SLOT_CHOICES = [1, 2, 3, 5, 6, 7, 9, 10 , 11, 13, 14, 15, 17, 18, 19, 21, 22, 23, 25, 26, 27, 29, 30, 31]

# Write hi-hats
for note in range(20):
  q = random.choice(SLOT_CHOICES)
  SLOT_CHOICES.pop(SLOT_CHOICES.index(q))
  plot_hh(int(5512.5 * q))

# Open hi-hat sounds bad, needs work
"""
# HI HAT (OPEN)
for note in range(4):
  q = random.choice(SLOT_CHOICES)
  SLOT_CHOICES.pop(SLOT_CHOICES.index(q))
#  plot_open_hh( int( 5512.5 * q ) )
"""

# Write snares
SNARE_SLOTS = [4, 12, 20, 28]
for i in range(4):
  plot_snare(int(5512.5 * SNARE_SLOTS[i]))


# Write song to file
for b in B:
    wavef.writeframesraw(struct.pack('<hh', int(b / DAMPEN), int(b / DAMPEN)))

wavef.close()

