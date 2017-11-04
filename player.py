import pysynth_b
import random
from pydub import AudioSegment

class Input:
    BPM = 0
    songLength = 0
    songName = "sound.wav"


def getBPM():
    if Input.BPM == 0:
        # Creates random BPM in between 80 and 160
        return random.randrange(80, 160)


def getSongLength():
    if Input.songLength == 0:
        # Creates random song length between 5 and 20 seconds
        return random.randrange(5, 20)


def findBeatsInSong():
    # Gets the beats in the song by finding beats per second, then multiplying by length
    return int((Input.BPM / 60) * Input.songLength)

def generateNotePatern(listLength):
    # Make empty list for ntoes
    noteList = []

    for i in range(0, listLength - 1):
        chance = random.uniform(0, 1)
        if chance <= 0.35:
            # New note is played
            noteList.append(1)
        elif chance >= 0.35 and chance <= 0.78:
            # Holds note
            noteList.append(2)
        else:
            # Rest
            noteList.append(0)
            
    return noteList


# Gets next number in an array
def findNextNumInArray(list, currentIndex):
    if currentIndex != len(list) - 1:
        return list[currentIndex + 1]


def createNoteTuple(noteList):
    index = 0

    # Empty tupple
    notesTuple = ()

    # Goes through whole list
    while index <= len(noteList) - 1:
        # If it needs to be add a rest
        if noteList[index] == 0:
            notesTuple += ('r', 8),
            index += 1
        # If it needs to be a new note or held
        elif noteList[index] == 1 or noteList[index] == 2:
            # Goes and sees how long the note needs to be held
            hold = 0
            while findNextNumInArray(noteList, index + hold) == 2:
                hold += 1

            # If it doesn't need to be held
            if hold == 0:
                notesTuple += ('c4', 8),
                index += 1
            # IF it does
            else:
                notesTuple += ('c4', float(8 / (hold + 1))),
                index += hold + 1
    return notesTuple


def makeSongLouder():
    song = AudioSegment.from_wav(Input.songName)
    song += 5
    song.export(Input.songName, "wav")


Input.songLength = getSongLength()
Input.BPM = getBPM()

cellularListLength = findBeatsInSong()
cellularList = generateNotePatern(cellularListLength)

notesTuple = createNoteTuple(cellularList)

pysynth_b.make_wav(notesTuple, fn=Input.songName, bpm=120, repeat=1, boost=1.2, silent=False)
makeSongLouder()
