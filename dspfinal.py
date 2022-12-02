#1 create a filter that change the intake voice
#2 ADD GUI

import pyaudio
import struct
import math
import tkinter as Tk
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

f0 = 400    # Modulation frequency (Hz)

BLOCKLEN = 64      # Number of frames per block
WIDTH = 2           # Number of bytes per signal value
CHANNELS = 1        # mono
RATE = 32000        # Frame rate (frames/second)

# Define TKinter root
root = Tk.Tk()

# demo_5
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
B_quit = Tk.Button(root, text = 'Quit', command = fun_quit)

# Place widgets
B_quit.pack(side = Tk.BOTTOM, fill = Tk.X)

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
    
    om = 2*math.pi*f0/RATE

    for n in range(0, BLOCKLEN):
        
        theta = theta + om
        output_block[n] = int(input_tuple[n] * math.cos(theta))
        output_block[n] = clip16(int(output_block[n] * 0.5))

    # keep theta betwen -pi and pi
    while theta > math.pi:
        theta = theta - 2*math.pi

    # Convert values to binary data
    output_bytes = struct.pack('h' * BLOCKLEN, *output_block)

    # Write binary data to audio output stream
    stream.write(output_bytes)

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
