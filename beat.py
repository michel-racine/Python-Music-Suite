
SCALE={						# note frequency dictionary
    "X0"  :   0.00000001,
    "C2"  :  65.41,
    "D2"  :  73.42,
    "E2"  :  82.41,
    "F2"  :  87.31,
    "F2#" :  92.50,
    "G2"  :  98.00,
    "A2"  : 110.00,
    "B2"  : 123.47,
    "C3"  : 130.81,
    "C3#" : 138.59,
    "D3"  : 146.83,
    "E3"  : 164.81,
    "F3"  : 174.61,
    "F3#" : 185.00,
    "G3"  : 196.00,
    "G3#" : 207.65,
    "A3"  : 220.00,
    "B3"  : 246.94,
    "C4"  : 261.63,
    "C4#" : 277.18,
    "D4"  : 296.66,
    "E4"  : 329.63,
    "F4"  : 349.23,
    "F4#" : 369.99,
    "G4"  : 392.00,
    "A4"  : 440.00,
    "B4"  : 493.88,
    "C5"  : 523.25,
    "A5"  : 880.00
    }

# 21.05.06
# simple 4 second song 120 bpm. cheesy beat but good example.
# improved with lead synth

import wave, struct, math, random

sample_rate = 44100.0
save_to = input("[+] save to file: ")
wavef = wave.open(save_to,'wb')
wavef.setnchannels(2)                 		# stereo
wavef.setsampwidth(2)
wavef.setframerate(sample_rate)

# BASS DRUM SETUP
f_bd = 200.0
theta_bd = 0.0
wavelen_bd = 0.0
y_bd = 0.0
r_bd = 30000

def add_B( locatino, y ):	# special function to "add" amplitudes in lieu of proper solution
    u = B[ locatino ]
    B[ locatino ] = u + ( 32767 - u ) / 32767.0 * y

# HI-HAT SEQUENCER SETUP
def plot_hh( trigger ):
    f_hh = 200.0
    theta_hh = 0.0
    wavelen_hh = 0.0
    y_hh = 0.0
    r_hh = 30000
    for bit in range(5000):
        r_hh = ( ( bit - 5000.0 ) / 5000 ) ** 2 * 30000
        f_hh = random.randint(10000,15000) * 1.0
        wavelen_hh = sample_rate / f_hh
        theta_inc_hh = 2*math.pi / wavelen_hh
        y_hh = r_hh * math.cos(theta_hh)
        theta_hh += theta_inc_hh
        B[ bit + trigger ] += y_hh

# OPEN HI-HAT SEQUENCER SETUP
def plot_open_hh( trigger ):
    theta_hh = 0; r_hh = 30000.0
    for bit in range(5000):
        f_hh = random.randint(10000,15000) * 1.0
        wavelen_hh = sample_rate / f_hh
        theta_inc_hh = 2*math.pi / wavelen_hh
        y_hh = r_hh * math.cos(theta_hh)
        theta_hh += theta_inc_hh
        B[ bit + trigger ] += y_hh

# SNARE DRUM SEQUENCER SETUP
def plot_snare( trigger ):
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
        r_sd = ( ( bit - 5000.0 ) / 5000 ) ** 2 * 30000
        f_sd = random.randint(-2440,6000) * 1.0
        wavelen_sd = sample_rate / (f_sd + 0.000000001)
        theta_inc_sd = 2*math.pi / wavelen_sd
        y_sd = r_sd * math.cos(theta_sd)
        theta_sd += theta_inc_sd
        #B[ bit + trigger ] += y_sd
        add_B( bit+trigger, y_sd )

# BASS SEQUENCER SETUP ### rem: 44100 * 4 = 176400
def plot( f_sq, trigger ):
#    f_sq = 220.0
    theta_sq = 0.0
    theta_inc_seq = 0.0
    wavelen_sq = 0.0
    y_sq = 0.0
    r_sq = 30000
    for bit in range(5000):
        r_sq = ( ( bit - 8000 ) / 8000 ) ** 2 * 30000
        wavelen_sq = sample_rate / f_sq
        theta_inc_sq = 2 * math.pi /wavelen_sq
        y_sq = r_sq * math.cos(theta_sq)
        theta_sq += theta_inc_sq
        B[ bit + trigger ] += y_sq
# make array to store sample bits
B = [0.0] * 176400

# LEAD SEQUENCER SETUP ###
def plot_lead( f_ld, trigger ):
    theta_ld = 0.0
    theta_ld_inc = 0.0
    wavelen_ld = 0.0
    y_ld = 0.0
    r_ld = 30000
    for bit in range(5000):
        if bit == 4820:
            f_ld *= 2
        r_ld = ( ( bit - 5000.0 ) / 5000 ) ** 2 * 30000
        wavelen_ld = sample_rate / f_ld
        theta_inc_ld = 2*math.pi / wavelen_ld
        y_ld = r_ld * math.cos(theta_ld)
        if y_ld > 0:
            y_ld = 10000
        else:
            y_ld = -10000
        theta_ld += theta_inc_ld
        B[ bit + trigger ] += y_ld

# BASS DRUM ###
# exp drop base
for bit in range(5000):
    r_bd = ( ( bit - 5000.0 ) / 5000 ) ** 2 * 30000
    f_bd = ( ( bit - 5000.0 ) / 5000 ) ** 2 * 200
    wavelen_bd = sample_rate / f_bd
    theta_inc_bd = 2*math.pi / wavelen_bd
    y_bd = r_bd * math.cos(theta_bd)
    theta_bd += theta_inc_bd
    for i in range(8):
        add_B( bit + ( i * 22050 ), y_bd )

SLOT_CHOICES = [1,2,3,5,6,7,9,10,11,13,14,15,17,18,19,21,22,23,25,26,27,29,30,31]

# HI HAT ###
for note in range(10):
  q = random.choice(SLOT_CHOICES)
  SLOT_CHOICES.pop(SLOT_CHOICES.index(q))
  plot_hh( int( 5512.5 * q ) )

# HI HAT (OPEN)
for note in range(4):
  q = random.choice(SLOT_CHOICES)
  SLOT_CHOICES.pop(SLOT_CHOICES.index(q))
  plot_open_hh( int( 5512.5 * q ) )

# SNARE DRUM ###
SLOT_CHOICES = [4,12,20,28]
for note in range(4):
  q = random.choice(SLOT_CHOICES)
  SLOT_CHOICES.pop(SLOT_CHOICES.index(q))
  plot_snare( int( 5512.5 * q ) )

############ SEQUENCER ##############
SLOT_CHOICES = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
NOTE_CHOICES  = ["A2","C2","E2","G3","A2","C3","E2","A3","B2","E2","G3","C3","E3"] 
#NOTE_CHOICES = ["D2","F2","A2","D3","F3","A3","D4","A3","F3","D3","A2","F2","D2"]
#NOTE_CHOICES = ["C2","E2","G2","C3","E3","G3","C4","G3","E3","C3","G2","E2","C2"]
#NOTE_CHOICES = ["F2","A2","D3","F3","A3","D4","F4","D4","A3","F3","D3","A2","F2"]
#NOTE_CHOICES = ["A2","C3","E3","A3","C4","E4","A4","E4","C4","A3","E3","C3","A2"]

for note in NOTE_CHOICES:
  q = random.choice(SLOT_CHOICES)
  SLOT_CHOICES.pop(SLOT_CHOICES.index(q))
  plot( SCALE[note], int( 5512.5 * q ) )

########### LEAD ####################
# rem: now are 16 slot choices left
#NOTE_CHOICES  = ["A2","B2","C3","D3","E3","F3","G3","A3","A3","C3","F2","B3","E3"]
#NOTE_CHOICES = ["D2","F2","A2","D3","F3","A3","D4","A3","F3","D3","A2","F2","D2"]
#NOTE_CHOICES = ["C2","E2","G2","C3","E3","G3","C4","G3","E3","C3","G2","E2","C2"]
#NOTE_CHOICES = ["F2","A3","D3","F3","A3","C4","A4","D4","C3","A3","D3","C2","A2"]
NOTE_CHOICES = ["A2","C3","E3","A3","C4","E4","A4","E4","C4","A3","E3","C3","A2"]
for note in NOTE_CHOICES:
  q = random.choice(SLOT_CHOICES)
  SLOT_CHOICES.pop(SLOT_CHOICES.index(q))
  plot_lead( SCALE[note]*1.5, int( 5512.5 * q ) )

for b in B:
    wavef.writeframesraw(struct.pack('<hh', int(b/3.5), int(b/3.5)))

#wavef.writeframes(b"\x00")
wavef.close()

