# demo_filter_blocks_corrected.py
# Block filtering of a wave file, save the output to a wave file.
# Corrected version.

import pyaudio, wave, struct, math
import numpy as np
import scipy.signal
from matplotlib import pyplot as plt

plt.ion()           # Turn on interactive mode so plot gets updated
plt.figure(1)


# Read the wave file properties
CHANNELS        = 1     # Number of channels
RATE            = 16000 # Sampling rate (frames/second)
DURATION        = 8     # Duration (seconds)
WIDTH           = 2     # Number of bytes per sample
BLOCKSIZE       = 1024   # length of block (samples)


# Difference equation coefficients
b0 =  0.008442692929081
b2 = -0.016885385858161
b4 =  0.008442692929081
b = [b0, 0.0, b2, 0.0, b4]

# a0 =  1.000000000000000
a1 = -3.580673542760982
a2 =  4.942669993770672
a3 = -3.114402101627517
a4 =  0.757546944478829
a = [1.0, a1, a2, a3, a4]

p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(
    format      = p.get_format_from_width(WIDTH),
    channels    = CHANNELS,
    rate        = RATE,
    input       = True,
    output      = True )

BLOCKLEN = 1024
MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)
n = range(0, BLOCKLEN)

# Setup plot
# PLOT 1
plt.subplot(1, 2, 1)
plt.title("input")
plt.xlim(0, BLOCKLEN)         # set x-axis limits
plt.ylim(-5000, 5000)
[line1] = plt.plot([], [], color = 'blue')  # Create empty line
line1.set_xdata(n)                 


# PLOT 2
plt.subplot(1, 2, 2)
plt.title("output")
plt.xlim(0, BLOCKLEN)         # set x-axis limits
plt.ylim(-5000, 5000)
[line2] = plt.plot([], [], color = 'red')  # Create empty line
line2.set_xdata(n)    

NumBlocks = int( DURATION * RATE / BLOCKSIZE )
ORDER = 4   # filter is fourth order
states = np.zeros(ORDER)

for i in range(0, NumBlocks):

    input_bytes = stream.read(BLOCKSIZE)                     # Read audio input stream
    input_block = struct.unpack('h' * BLOCKSIZE, input_bytes)  # Convert

    # filter
    [output_block, states] = scipy.signal.lfilter(b, a, input_block, zi = states)

    # clipping
    output_block = np.clip(output_block, -MAXVALUE, MAXVALUE)

    # convert to integer
    output_block = output_block.astype(int)

    line1.set_ydata(input_block)  
    line2.set_ydata(output_block)  
    plt.pause(0.000001) # this is slow??
    

    # Convert output value to binary data
    binary_data = struct.pack('h' * BLOCKLEN, *output_block)

    # Write binary data to audio stream
    stream.write(binary_data)

    

print('* Finished')

plt.close()
stream.stop_stream()
stream.close()
p.terminate()

# Close wavefiles
wf.close()
output_wf.close()