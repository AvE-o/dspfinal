# Base on AM_from_microphone.py
# Record audio and play it with amplitude modulation. 
# This implementation:
#   uses blocking, 
#   corrects for block-to-block angle mismatch,
#   assumes mono channel
# Original by Gerald Schuller, 2013


from re import S
import pyaudio
import struct
import math
import cmath
# from matplotlib import pyplot
from myfunctions import clip16
from scipy import signal


# f0 = 0      # Normal audio
f0 = 400    # Modulation frequency (Hz)

BLOCKLEN = 1024     # Number of frames per block
WIDTH = 2           # Number of bytes per signal value
CHANNELS = 1        # mono
RATE = 32000        # Frame rate (frames/second)
RECORD_SECONDS = 5

p = pyaudio.PyAudio()

stream = p.open(
    format      = p.get_format_from_width(WIDTH),
    channels    = CHANNELS,
    rate        = RATE,
    input       = True,
    output      = True)


output_block = BLOCKLEN * [0]

# Initialize phase
om = 1 / RATE
theta = 0

# demo_5
order = 7
[b_lpf, a_lpf] = signal.ellip(order, 0.2, 50, 0.48)
I = 1j
s = [I ** i for i in range(0, order + 1)]
b = [0 ** i for i in range(0, order + 1)]
a = [0 ** i for i in range(0, order + 1)]

for i in range(0, order + 1):
    b[i] = b_lpf[i] * s[i]
    a[i] = a_lpf[i] * s[i]

# Number of blocks to run for
num_blocks = int(RATE / BLOCKLEN * RECORD_SECONDS)

print('* Recording for %.3f seconds' % RECORD_SECONDS)

# Start loop
for i in range(0, num_blocks):

    # Get frames from audio input stream
    # input_bytes = stream.read(BLOCKLEN)       # BLOCKLEN = number of frames read
    input_bytes = stream.read(BLOCKLEN, exception_on_overflow = False)   # BLOCKLEN = number of frames read

    # Convert binary data to tuple of numbers
    input_tuple = struct.unpack('h' * BLOCKLEN, input_bytes)
    
    R = signal.lfilter(b, a, input_tuple)
    # Go through block
    for n in R:

        theta = theta + om
        # g = r .* exp( I * 2 * pi * f1 * t );
        g = n * cmath.exp(I * 2 * cmath.pi * f0 * theta)
        # keep theta betwen -pi and pi
        while theta > math.pi:
            theta = theta - 2*math.pi

        y = clip16(int(g.real))
        output_byte = struct.pack('h', y)
        # Write binary data to audio output stream
        stream.write(output_byte)

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
