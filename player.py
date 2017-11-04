import wave, struct, math

RATE = 44100.0 # hertz
SINCONST = 32767

wavef = wave.open('sound.wav','w')
wavef.setnchannels(2)
wavef.setsampwidth(2)
wavef.setframerate(RATE)

def createTone(frequency, length):
    frames = []

    for i in range(int(length * RATE)):
        sinValue = int(SINCONST * math.sin(i * math.pi * frequency / float(RATE)))
        data = struct.pack('<h', sinValue)
        frames.append(data)
        # wavef.writeframesraw(data)

    return frames

def writeSound(sound):
    for i in sound:
        wavef.writeframesraw(i)

sound1 = createTone(300, 1)
sound2 = createTone(500, 1)

writeSound(sound1)
writeSound(sound2)

#wavef.writeframesraw(createTone(300, 1))
wavef.writeframes('')
wavef.close()