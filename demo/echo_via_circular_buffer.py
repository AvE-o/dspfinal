# base on echo_via_circular_buffer.py
import pyaudio
import wave
import struct
from myfunctions import clip16
import numpy as np


num_channels    = 1        # Number of channels
RATE            = 8000     # Sampling rate (frames/second)
duration        = 2        # Signal length
width           = 2        # Number of bytes per sample

# Karplus-Strong paramters
K = 0.9
N = 10

a1 = 1
axi = -K/2
axii = -K/2
b0 = 1

# Set parameters of delay system

# print('The delay of %.3f seconds is %d samples.' %  (delay_sec, N))
# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format      = pyaudio.paInt16,
                channels    = 1,
                rate        = RATE,
                input       = False,
                output      = True )

bufferyxi = 11 * [0]
bufferyxii = 11 * [0]

# Initialize buffer index (circular index)
kxi = 0
kxii = 0


print('* Start')


lengthx = duration * RATE + N
x = [0] * (lengthx)

# input signal
# x = [randn(1, N) zeros(1, round(T*Fs))];
# y(n) = x(n) + K/2 y(n-N) + K/2 y(n-N-1)
for i in range(N):
    x[i] = np.random.randn() * 1000000

for i in range(lengthx):
    x0 = x[i]


    y0 = b0 * x0 - axi * bufferyxi[kxi] - axii * bufferyxii[kxii]

    # Update buffer
    bufferyxi[kxi] = y0
    bufferyxii[kxii] = y0
    
    # Increment buffer index
    kxi = kxi + 1
    kxii = kxii + 1

    if kxi >= N + 1:
        # The index has reached the end of the buffer. Circle the index back to the front.
        kxi = 0

    if kxii >= N + 1:
        # The index has reached the end of the buffer. Circle the index back to the front.
        kxii = 0
    # Clip and convert output value to binary data
    output_bytes = struct.pack('h', int(clip16(y0)))

    # Write output value to audio stream
    stream.write(output_bytes)

    # Get next frame
    # input_bytes = wf.readframes(1)     

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
#wf.close()