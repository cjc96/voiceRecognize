import pyaudio
import wave
import pylab as pl
import numpy as np
import sys
import thread
import time

duration = 60

def hello(_, tick):
	while (tick <= duration):
		time.sleep(1)
		print tick
		tick += 1
	thread.exit()

def record(_1, _2):
	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 8192
	RECORD_SECONDS = duration
	WAVE_OUTPUT_FILENAME = 'oral.wav'
	p = pyaudio.PyAudio()
	stream = p.open(format=FORMAT,
	                channels=CHANNELS,
	                rate=RATE,
	                input=True,
	                frames_per_buffer=CHUNK)
	print("* recording")
	frames = []
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	    data = stream.read(CHUNK)
	    frames.append(data)
	print("* done recording")
	stream.stop_stream()
	stream.close()
	p.terminate()
	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()
	thread.exit()


thread.start_new_thread(hello, ('t1', 1))
thread.start_new_thread(record, ('t2',''))
while 1:
	pass