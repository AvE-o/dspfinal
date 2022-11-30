# mic_filter.py
# Record from microphone, filter the signal,
# and play the output signal on the loud speaker.

from cmath import cos, pi
from pickle import bytes_types
import pyaudio
import struct
import math
import wave

def clip16( x ):    
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x        
    return (x)

WIDTH       = 2         # Number of bytes per sample
CHANNELS    = 1         # mono
RATE        = 16000     # Sampling rate (frames/second)
DURATION    = 6         # duration of processing (seconds)

wf = wave.open('sound.wav', 'w')
wf.setnchannels(1)			
wf.setsampwidth(2)			
wf.setframerate(16000)	

N = DURATION * RATE     # N : Number of samples to process


# Difference equation coefficients
b0 =  0.008442692929081
b2 = -0.016885385858161
b4 =  0.008442692929081

# a0 =  1.000000000000000
a1 = -3.580673542760982
a2 =  4.942669993770672
a3 = -3.114402101627517
a4 =  0.757546944478829

f0 = 400

# Initialization
x1 = 0.0
x2 = 0.0
x3 = 0.0
x4 = 0.0
y1 = 0.0
y2 = 0.0
y3 = 0.0
y4 = 0.0

p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(
    format      = p.get_format_from_width(WIDTH),
    channels    = CHANNELS,
    rate        = RATE,
    input       = True,
    output      = True)

print('* Start')

for n in range(0, N):

    # Get one frame from audio input (microphone)
    input_bytes = stream.read(1)
    # If you get run-time time input overflow errors, try:
    # input_bytes = stream.read(1, exception_on_overflow = False)

    # Convert binary data to tuple of numbers
    input_tuple = struct.unpack('h', input_bytes)

    # Convert one-element tuple to number
    x0 = input_tuple[0]

    # Difference equation cos(2*pi*400) -> math.cos(2*math.pi*400)
    # y0 = b0*x0 + b2*x2 + b4*x4 - a1*y1 - a2*y2 - a3*y3 - a4*y4  

    # Delays
    #x4 = x3
    #x3 = x2
    #x2 = x1
    #x1 = x0
    #y4 = y3
    #y3 = y2
    #y2 = y1
    #y1 = y0

    # Compute output value
    output_value = int(clip16(x0 * math.cos(2 * math.pi * f0 * n/RATE)))    # Number

    # output_value = int(clip16(x0))   # Bypass filter (listen to input directly)

    # Convert output value to binary data
    output_bytes = struct.pack('h', output_value)  
    #bytes_string = struct.pack('h', output_value)
    
    # Write to wav file
    wf.writeframesraw(output_bytes)

    # Write binary data to audio stream
    stream.write(output_bytes)
    

print('* Finished')

wf.close()
stream.stop_stream()
stream.close()
p.terminate()
