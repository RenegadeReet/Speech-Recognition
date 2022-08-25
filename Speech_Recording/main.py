import pyaudio
import wave

FRAMES_PER_BUFFER = 3200
RATE = 16000
CHANNELS = 1
FORMAT = pyaudio.paInt16

p = pyaudio.PyAudio()

stream = p.open(channels=CHANNELS , frames_per_buffer = FRAMES_PER_BUFFER , rate=RATE,input=True,format=FORMAT)

SECONDS = 5
FRAMES = []
print("Start Recording")

for i in range(0 , int(RATE/FRAMES_PER_BUFFER*SECONDS)):
    data = stream.read(FRAMES_PER_BUFFER)
    FRAMES.append(data)

stream.stop_stream()
stream.close()
p.terminate()

obj = wave.open("Output.wav" , "wb")
obj.setnchannels(CHANNELS)
obj.setsampwidth(p.get_sample_size(FORMAT))
obj.setframerate(RATE)
obj.writeframes(b"".join(FRAMES))
obj.close()

