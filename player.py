import pysynth_b
import random

class Input:
    BPM = 0
    songLength = 0

def getBPM():
    if Input.BPM == 0:
        return random.randrange(80, 160)

def getSongLength():
    if Input.songLength == 0:
        return random.randrange(5, 20)


def findBeatsInSong():
    beatsInSong = int((Input.BPM / 60) * Input.songLength)
    return beatsInSong


def generateNotePatern(listLength):
    noteList = []

    for i in range(0, listLength - 1):
        chance = random.uniform(0, 1)
        if chance <= 0.13:
            noteList.append(1)
        elif chance >= 0.13 and chance <= 0.67:
            noteList.append(2)
        else:
            noteList.append(0)

    return noteList

def findNextNumInArray(list, currentIndex):
    if currentIndex != len(list) - 1:
        return list[currentIndex + 1]

def createNoteTuple(noteList):
    index = 0
    notesTuple = ()

    while index <= len(noteList) - 1:
        print(index)

        if noteList[index] == 0:
            notesTuple += ('r', 16),
            index += 1
        elif noteList[index] == 1 or noteList[index] == 2:
            hold = 0
            while findNextNumInArray(noteList, index + hold) == 2:
                hold += 1
            if hold == 0:
                notesTuple += ('c4', 8),
                index += 1
            else:
                notesTuple += ('c4', float(8 / (hold + 1))),
                index += hold + 1
    return notesTuple

Input.songLength = getSongLength()
Input.BPM = getBPM()

cellularListLength = findBeatsInSong()
cellularList = generateNotePatern(cellularListLength)

notesTuple = createNoteTuple(cellularList)

pysynth_b.make_wav(notesTuple, fn="sound.wav", bpm = 120, repeat=1, boost=1.2, silent=False)

#print(data)

#def generateNotePatern():

#pysynth.make_wav(test, fn = "sound.wav")