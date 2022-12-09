#1 create a filter that change the intake voice
#2 ADD GUI
#3 Store sound into an audio file
#4 add normal voice & robot voice option
#5 Frequency slider

import pyaudio
import struct
import math
import wave
import tkinter as Tk
import numpy as np
# from scipy.signal import spectrogram, windows

def clip16( x ):    
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x        
    return (x) 

def fun_quit():
  global CONTINUE
  print('Good bye')
  CONTINUE = False

BLOCKLEN = 64      # Number of frames per block
WIDTH = 2           # Number of bytes per signal value
CHANNELS = 1        # mono
RATE = 32000        # Frame rate (frames/second)

# f0 = 400    # Modulation frequency (Hz)

# Copy of the sound file will be store
wf = wave.open('dsp.wav', 'w')		# wf : wave file
wf.setnchannels(1)			        # one channel (mono)
wf.setsampwidth(2)			
wf.setframerate(RATE)	            # samples per second

# Define TKinter root
root = Tk.Tk()

# Define Tk variables
freq = Tk.DoubleVar()

# order = 7
# [b_lpf, a_lpf] = signal.ellip(order, 0.2, 50, 0.48)
# I = 1j
# s = [I ** i for i in range(0, order + 1)]
# b = [0 ** i for i in range(0, order + 1)]
# a = [0 ** i for i in range(0, order + 1)]

# for i in range(0, order + 1):
    # b[i] = b_lpf[i] * s[i]
    # a[i] = a_lpf[i] * s[i]

# Define widgets
S_freq = Tk.Scale(root, label = 'Frequency', variable = freq, from_ = 100, to = 600, tickinterval = 50)

B_quit = Tk.Button(root, text = 'Quit', command = fun_quit)

L_label = Tk.Label(root, text = 'Voice_Option')

option = Tk.IntVar()
R_func = Tk.Radiobutton(root, text="Robot_Voice", value="1", var=option)
R_func2 = Tk.Radiobutton(root, text="Normal_Voice", value="2", var=option)

# Place widgets
# Pack will use in this case
S_freq.pack(side = Tk.LEFT)
B_quit.pack(side = Tk.BOTTOM, fill = Tk.X, padx = 50)
L_label.pack(padx = 5)
R_func.pack(padx = 5)
R_func2.pack(padx = 5)

p = pyaudio.PyAudio()
stream = p.open(
    format      = p.get_format_from_width(WIDTH),
    channels    = CHANNELS,
    rate        = RATE,
    input       = True,
    output      = True,
    frames_per_buffer = 128)

# Initialize phase
output_block = BLOCKLEN * [0]
theta = 0
CONTINUE = True

while CONTINUE:
    root.update()
    
    input_bytes = stream.read(BLOCKLEN, exception_on_overflow = False)   
    input_tuple = struct.unpack('h' * BLOCKLEN, input_bytes)
    
    
    #Robot Voice
    if option.get() == 1:
        om = 2*math.pi*freq.get()/RATE
        for n in range(0, BLOCKLEN):
            theta = theta + om
            output_block[n] = int(input_tuple[n] * math.cos(theta))
            output_block[n] = clip16(int(output_block[n] * 0.5))

        # keep theta betwen -pi and pi
        while theta > math.pi:
            theta = theta - 2*math.pi

    #Normal Voice
    if option.get() == 2:
        x = np.fft.rfft(input_tuple)
        output_block = np.fft.irfft(x)
        output_block = output_block.astype(int)

    # Convert values to binary data
    output_bytes = struct.pack('h' * BLOCKLEN, *output_block)

    # Write binary data to audio output stream
    stream.write(output_bytes)
    # Write binary data to audio file
    wf.writeframesraw(output_bytes)

print('* Finished')

stream.stop_stream()
stream.close()
wf.close()
p.terminate()
