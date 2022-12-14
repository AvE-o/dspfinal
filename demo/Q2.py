# Tk_demo_04_slider.py
# TKinter demo
# Play a sinusoid using Pyaudio. Use two sliders to adjust the frequency and gain.

from math import cos, pi, sin
import wave
import pyaudio, struct
import tkinter as Tk   	
import numpy as np
from matplotlib import pyplot as plt # plot

plt.ion()           # Turn on interactive mode so plot gets updated

def fun_quit():
  global CONTINUE
  print('Good bye')
  CONTINUE = False

Fs = 8000     # rate (samples/second)
gain = 0.2 * 2**15
temp = 500

wf = wave.open('8.wav', 'w')		# wf : wave file
wf.setnchannels(1)			# one channel (mono)
wf.setsampwidth(2)			
wf.setframerate(Fs)			# samples per second

# Define Tkinter root
root = Tk.Tk()

# Define Tk variables
f1 = Tk.DoubleVar()
gain = Tk.DoubleVar()
max = Tk.DoubleVar()
min = Tk.DoubleVar()
time = Tk.DoubleVar()

# Initialize Tk variables
# f1.set(200)   # f1 : frequency of sinusoid (Hz)
gain.set(0.2 * 2**15)
time.set(50)


# Define widgets                                                             
S_freq = Tk.Scale(root, label = 'Max_Frequency', variable = max, from_ = 1000, to = 3000, tickinterval = 100)
S_freq2 = Tk.Scale(root, label = 'Min_Frequency', variable = min, from_ = 100, to = 1000, tickinterval = 100)
S_time = Tk.Scale(root, label = 'Time(slow to quick)', variable = time, from_ = 20, to = 100, tickinterval = 10)

S_gain = Tk.Scale(root, label = 'Gain', variable = gain, from_ = 0, to = 2**15-1)
B_quit = Tk.Button(root, text = 'Quit', command = fun_quit)

option = Tk.IntVar()
R_func = Tk.Radiobutton(root, text="Option1", value="1", var=option)
R_func2 = Tk.Radiobutton(root, text="Option2", value="2", var=option)


# Place widgets
B_quit.pack(side = Tk.BOTTOM, fill = Tk.X)
S_freq.pack(side = Tk.LEFT)
S_freq2.pack(side=Tk.LEFT)
S_gain.pack(side = Tk.LEFT)
S_time.pack(side=Tk.LEFT)
R_func.pack(side = Tk.LEFT)
R_func2.pack(side = Tk.LEFT)

# Create Pyaudio object
p = pyaudio.PyAudio()
stream = p.open(
  format = pyaudio.paInt16,  
  channels = 1, 
  rate = Fs,
  input = False, 
  output = True,
  frames_per_buffer = 128)            
  # specify low frames_per_buffer to reduce latency

BLOCKLEN = 256
output_block = [0] * BLOCKLEN
theta = 0
CONTINUE = True
print('* Start')

DBscale = False
# DBscale = True

# Initialize plot window:
plt.figure(1)
if DBscale:
    plt.ylim(0, 150)
else:
    plt.ylim(0, 40*Fs)

# Frequency axis (Hz)
plt.xlim(0, 0.5*Fs)         # set x-axis limits
# plt.xlim(0, 2000)         # set x-axis limits
plt.xlabel('Frequency (Hz)')
f = Fs/BLOCKLEN * np.arange(0, BLOCKLEN)

line, = plt.plot([], [], color = 'blue')  # Create empty line
line.set_xdata(f)                         # x-data of plot (frequency)

prev_gain = gain.get() # get gain value from previous block
while CONTINUE:
  
  temp = temp + time.get()
  f1.set(temp)

  root.update()
  now_gain = gain.get() # get gain value from the block we are using rn
  diff_gain = now_gain - prev_gain

  # Option 1
  if option.get() == 1:
    om1 = 2.0 * pi * f1.get() / Fs

    for i in range(0, BLOCKLEN):
      output_block[i] = int((prev_gain + diff_gain / BLOCKLEN) * cos(theta))
      theta = theta + om1
  
  # Option 2
  if option.get() == 2:
    om1 = 5.0 * pi * f1.get() / Fs

    for i in range(0, BLOCKLEN):
      output_block[i] = int((prev_gain + diff_gain / BLOCKLEN) * sin(theta) * 3)
      theta = theta + om1
  
  if theta > pi:
    theta = theta - 2.0 * pi
  
  if temp > max.get():
    temp = min.get()

  prev_gain = now_gain # get gain value from previous block
  
  X = np.fft.fft(output_block)
    # Update y-data of plot
  if DBscale:
      line.set_ydata(20 * np.log10(np.abs(X)))
  else:
      line.set_ydata(np.abs(X))
  plt.pause(0.001)

    # plt.draw()
  binary_data = struct.pack('h' * BLOCKLEN, *output_block)   # 'h' for 16 bits
  stream.write(binary_data)
  wf.writeframesraw(binary_data)


print('* Finished')

plt.close()
stream.stop_stream()
stream.close()
wf.close()
p.terminate()

