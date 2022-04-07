import sounddevice as sd
sd.default.device = [0,0]



duration = 5.0  # seconds

fs = 44100
num_channels = [1,0]   #numero input/output

sd.default.channels = num_channels

myrecording = sd.rec(int(duration * fs), samplerate=fs)
sd.wait()

sd.play(myrecording*4,fs,[1]) #scelta loudspeaker


#sd.play(4*myrecording[:,0], fs)  # play 1 canale
#sd.play(4*myrecording[:,1], fs)   # play 2 canale 