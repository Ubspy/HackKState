import pysynth_b
import random
from pydub import AudioSegment
import math

from reportlab.graphics.charts.axes import _isListOfDaysAndMonths


class Input:
    BPM = 0
    songLength = 0
    key = 0
    songName = "sound.wav"


# Key signatures disctionary
keySignatures = {
    'C': ['c', 'd', 'e', 'f', 'g', 'a', 'b'],
    'F': ['f', 'g', 'a', 'a#', 'c', 'd', 'e'],
    'B-flat': ['a#', 'c', 'd', 'd#', 'f', 'g', 'a'],
    'E-flat': ['d#', 'f', 'g', 'g#', 'a#', 'c', 'd'],
    'A-flat': ['g#', 'a#', 'c', 'c#', 'd#', 'f', 'g'],
    'D-flat': ['c#', 'd#', 'f', 'f#', 'g#', 'a#', 'c'],
    'G-flat': ['f#', 'g#', 'a#', 'b', 'c#', 'd#', 'f'],
    'B': ['b', 'c#', 'd#', 'e', 'f#', 'g#', 'a#'],
    'E': ['e', 'f#', 'g#', 'a', 'b', 'c#', 'd#'],
    'A': ['a', 'b', 'c#', 'd', 'e', 'f#', 'g#'],
    'D': ['d', 'e', 'f#', 'g', 'a', 'b', 'c#'],
    'G': ['g', 'a', 'b', 'c', 'd', 'e', 'f#']
}

def getBPM():
    if Input.BPM == 0:
        # Creates random BPM in between 80 and 160
        return random.randrange(80, 160)


def getSongLength():
    if Input.songLength == 0:
        # Creates random song length between 5 and 20 seconds
        return random.randrange(5, 20)

def getKeySignature():
    if Input.key == 0:
        return random.choice(list(keySignatures.keys()))


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

    # Empty tuple
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


def findNumberOfNotes(tuple):
    count = 0

    for i in tuple:
        # If it's a note to play
        if i[0] == 'c4':
            count += 1

    return count


def findNote(currentNote, currentOctave, spaceBetweenNotes):
    noteIndex = keySignatures[Input.key].index(currentNote[:len(currentNote) - 1])

    # Sets default octave move to zero
    octaveMove = 0

    # If it needs to move between octaves
    if (noteIndex + spaceBetweenNotes) < 0 or (noteIndex + spaceBetweenNotes) > 6:
        octaveMove = math.floor((spaceBetweenNotes + noteIndex) / 7)

        if int(currentOctave) + octaveMove <= 2 or int(currentOctave) + octaveMove >= 6:
            spaceBetweenNotes = spaceBetweenNotes * -1
            octaveMove = math.floor((spaceBetweenNotes + noteIndex) / 7)

        indexOfNewNote = (spaceBetweenNotes - (octaveMove * 7)) + noteIndex
    else:
        indexOfNewNote = spaceBetweenNotes + noteIndex

    newNote = keySignatures[Input.key][indexOfNewNote]
    newOctave = int(currentOctave) + int(octaveMove)

    newNote = str(newNote) + str(newOctave)

    return newNote


def generateNotes(length):
    startingNote = random.choice(keySignatures[Input.key])
    startingOctave = random.randrange(3, 5)

    startingNote += str(startingOctave)

    noteList = []
    noteList.append(startingNote)

    normalizeCurvePercents = [0.021, 0.157, 0.500, 0.843, 0.979]

    for i in range(length):
        chance = random.uniform(0, 1)
        space = 0

        # Checks chance
        if chance <= normalizeCurvePercents[0]:
            space = -random.randrange(8, 10)
        elif (chance > normalizeCurvePercents[0]) and (chance <= normalizeCurvePercents[1]):
            space = -random.randrange(5, 7)
        elif (chance > normalizeCurvePercents[1]) and (chance <= normalizeCurvePercents[2]):
            space = -random.randrange(1, 4)
        elif (chance > normalizeCurvePercents[2]) and (chance <= normalizeCurvePercents[3]):
            space = random.randrange(1, 4)
        elif (chance > normalizeCurvePercents[3]) and (chance <= normalizeCurvePercents[4]):
            space = random.randrange(5, 7)
        elif chance > normalizeCurvePercents[4]:
            space = random.randrange(8, 10)

        nextNote = findNote(noteList[-1], noteList[-1][-1], space)
        noteList.append(nextNote)

    return noteList


def changeNotes(noteList, noteTuple):
    noteIndex = 0
    newNoteTuple = ()

    for i in noteTuple:
        if i[0] == 'c4':
            iList = list(i)
            iList[0] = noteList[noteIndex]
            noteIndex += 1
            newNoteTuple += tuple(iList),
        else:
            newNoteTuple += i,

    return newNoteTuple


def makeSongLouder():
    song = AudioSegment.from_wav(Input.songName)
    song += 5
    song.export(Input.songName, "wav")


Input.songLength = getSongLength()
Input.BPM = getBPM()
Input.key = getKeySignature()

print(Input.key)

cellularListLength = findBeatsInSong()
cellularList = generateNotePatern(cellularListLength)

notesTuple = createNoteTuple(cellularList)

notesListLength = findNumberOfNotes(notesTuple)
notesList = generateNotes(notesListLength)

notesTuple = changeNotes(notesList, notesTuple)

pysynth_b.make_wav(notesTuple, fn=Input.songName, bpm=120, silent=False)
makeSongLouder()