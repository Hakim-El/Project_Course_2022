import sounddevice as sd
sd.default.device = [2,1]

duration = 5.0  # seconds

fs = 44100
num_channels = [2,2]   #numero input/output

sd.default.channels = num_channels

myrecording = sd.rec(int(duration * fs), samplerate=fs)
sd.wait()

sd.play(4*myrecording, fs)


#sd.play(4*myrecording[:,0], fs)   play 1 canale
#sd.play(4*myrecording[:,1], fs)    play 2 canale 