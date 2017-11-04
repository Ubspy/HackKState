import pysynth_b
import random


BPM = 120

songLength = 5.0

beatsInSong = BPM * songLength / 60
cellularListLength = round(beatsInSong * 16)

cellularList = []

for i in range(0, cellularListLength):
    chance = random.uniform(0, 1)
    if chance <= 0.13:
        cellularList.append(1)
    elif chance >= 0.13 and chance <= 0.67:
        cellularList.append(2)
    else:
        cellularList.append(0)

print(cellularList)

notesTuple = ()

index = 0

def findNextNumInArray(currentIndex):
    if currentIndex != len(cellularList) - 1:
        return cellularList[currentIndex + 1]

while index <= len(cellularList) - 1:
    if cellularList[index] == 0:
        notesTuple += ('r', 16),
        index += 1
    elif cellularList[index] == 1 or cellularList[index] == 2:
        hold = 0
        while findNextNumInArray(index + hold) == 2:
            hold += 1
        if hold == 0:
            notesTuple += ('c4', 16),
            index += 1
        else:
            notesTuple += ('c4', float(16 / (hold + 1))),
            index += hold

pysynth_b.make_wav(notesTuple, fn="sound.wav")

print(notesTuple)

noteTypes = {'quarter': 4, 'half': 2, 'whole': 1, 'eighth': 8, 'sixteenth': 16}



'''
furElise = wave.open('furElise.mp3')
length = furElise.getnframes()

for i in len(length):
    data = furElise.readframes(CHUNK)
'''

#print(data)

#def generateNotePatern():

#pysynth.make_wav(test, fn = "sound.wav")