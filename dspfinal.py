#1 create a filter that change the intake voice

import pyaudio
import struct
import math
import wave
import numpy as np
from scipy.signal import spectrogram, windows

def clip16( x ):    
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x        
    return (x)

# f0 = 0      # Normal audio
f0 = 400    # Modulation frequency (Hz)

BLOCKLEN = 64      # Number of frames per block
WIDTH = 2           # Number of bytes per signal value
CHANNELS = 1        # mono
RATE = 32000        # Frame rate (frames/second)

p = pyaudio.PyAudio()

stream = p.open(
    format      = p.get_format_from_width(WIDTH),
    channels    = CHANNELS,
    rate        = RATE,
    input       = True,
    output      = True)


output_block = BLOCKLEN * [0]

# Initialize phase
om = 2*math.pi*f0/RATE
theta = 0

while (True):

    input_bytes = stream.read(BLOCKLEN, exception_on_overflow = False)   
    input_tuple = struct.unpack('h' * BLOCKLEN, input_bytes)
   
    for n in range(0, BLOCKLEN):

        theta = theta + om
        # output_block[n] = clip16(int( input_tuple[n] * math.cos(theta) ))
        output_block[n] = clip16(int(math.sin(2*math.pi*f0/RATE)))
        # output_block[n] = clip16(int(np.sin(2*np.pi*f0/RATE)))
    
    # f, t, sxx = spectrogram(np.array(input_tuple), fs=f0, nfft=BLOCKLEN, noverlap=None)
    # output_block = sxx
    # x = np.fft.rfft(input_tuple)
    # output_block = np.fft.irfft(x)
    # output_block = output_block.astype(int)

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
