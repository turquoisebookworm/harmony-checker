# 4-part harmony checker!!

# 1. check they make chords (triads) - done!
# 2. check for consecutive octaves - done!
# 3. check for consecutive 5ths - done!
# 4. check distances between parts
# 5. output chord sequence and check it makes a cadence - done!
# 6. make it work for 7ths, prepared + resolved

# things to do next:
# turn it into slash notation for letter prog

#---notes to numbers function---
def notesToNumbers(noteNames):

  numbers = []

  for x in range(len(noteNames)):
    noteName = noteNames[x]

    if noteName[0:1] in notes:
      noteNumber = notes.index(noteName[0:1])+1

      if len(noteName) > 1:
        if noteName[1:2] == '#':
          noteNumber = noteNumber + 1
        if noteName[1:2] == 'b':
          noteNumber = noteNumber - 1

      if len(noteName) > 1:
        if noteName[len(noteName)-1:len(noteName)].isdigit():
          octaveNumber = int(noteName[len(noteName)-1:len(noteName)])
          noteNumber = noteNumber + (12 * octaveNumber)

    else:
      noteNumber = -1

    numbers.append(noteNumber)
  return(numbers)

#---inputting the notes---

notes = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
soprano = []
alto = []
tenor = []
bass = []

numberOfNotes = int(input('how many chords are there? '))

print('type 1 or 2 after the note to increase the octave')

for x in range(numberOfNotes):
  sopranoNotes = input('enter the next soprano note ')
  soprano.append(sopranoNotes)
  altoNotes = input('enter the next alto note ')
  alto.append(altoNotes)
  tenorNotes = input('enter the next tenor note ')
  tenor.append(tenorNotes)
  bassNotes = input('enter the next bass note ')
  bass.append(bassNotes)

#---calling notes to numbers function---

sopranoNumbers = notesToNumbers(soprano)
altoNumbers = notesToNumbers(alto)
tenorNumbers = notesToNumbers(tenor)
bassNumbers = notesToNumbers(bass)

#---checking if the notes make a triad + calculating inversions---

triadCount = 0
chordProgressionNumbers = []
tonalityProgression = []
thisChordUnsorted = []
inversionsGlobal = []

def findInversion(chordNumbers):
  inversion = ''
  if chordNumbers[3] == thisChord[0]:
    inversion = ''
  elif chordNumbers[3] == thisChord[1]:
    inversion = 'b'
  elif chordNumbers[3] == thisChord[2]:
    inversion = 'c'
  return(inversion)

for x in range (numberOfNotes):
  thisChord = []
  thisChordUnsorted = []
  thisChord.append(sopranoNumbers[x])
  thisChord.append(altoNumbers[x])
  thisChord.append(tenorNumbers[x])
  thisChord.append(bassNumbers[x])
  for n in range (len(thisChord)):
    thisChordUnsorted.append(thisChord[n])
  thisChord.sort()
  chordProgressionNumbers.append(thisChord[0])

  inversionGlobal = findInversion(thisChordUnsorted)
  inversionsGlobal.append(inversionGlobal)

  if thisChord[0] + 4 == thisChord[1] and thisChord[1] + 3 == thisChord[2] and thisChord[2] + 5 == thisChord[3]:
    triadCount = triadCount + 1
    tonality = 'major'
    tonalityProgression.append(tonality)
  elif thisChord[0] + 3 == thisChord[1] and thisChord[1] + 4 == thisChord[2] and thisChord[2] + 5 == thisChord[3]:
    triadCount = triadCount + 1
    tonality = 'minor'
    tonalityProgression.append(tonality)
  else:
    print('triad number ' + str(x+1) + ' is incorrect')

if triadCount == numberOfNotes:
  print('All your chords are triads')
  
#---checking chord progression---

chordProgressionLetters = []
progressionToPrintList = []

for x in range (numberOfNotes):
  thisRoot = chordProgressionNumbers[x]
  chordProgressionLetters.append(notes[thisRoot - 1])

for x in range(numberOfNotes):
  progressionToPrintList.append(chordProgressionLetters[x])
  if tonalityProgression[x] == 'minor':
    progressionToPrintList.append('m ')
    if inversionsGlobal[x] == 'b' or inversionsGlobal[x] == 'c':
      progressionToPrintList.append(f'/{bass[x]}')
    progressionToPrintList.append('- ')
  elif tonalityProgression[x] == 'major':
    if inversionsGlobal[x] == 'b' or inversionsGlobal[x] == 'c':
      progressionToPrintList.append(f'/{bass[x]}')
    progressionToPrintList.append('- ')

def removeSymbols(toPrintList):
  toPrintString = str(toPrintList)
  toPrintString = toPrintString.replace("'", "")
  toPrintString = toPrintString.replace("]", "")
  toPrintString = toPrintString.replace("[", "")
  toPrintString = toPrintString.replace(",", "")
  toPrintString = toPrintString.replace(" ", "")
  toPrintString = toPrintString[:-1]
  return(toPrintString)

progressionToPrintString = removeSymbols(progressionToPrintList)
print('The chord progression is ' + progressionToPrintString)

#---chord progression in roman numerals + cadences---

romanNumerals = []

keyStr = input('What key is it in? ')
keyList = [keyStr]
keyNumber = notesToNumbers(keyList)

if keyStr[-1] == 'm':
  keyTonality = 'minor'
  romanNumerals = ['blank', 'i', 'ii°', 'III', 'iv', 'V', 'VI', 'vii°']
else:
  keyTonality = 'major'
  romanNumerals = ['blank', 'I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii°' ]

diatonicChordsNumbers = [0, 1, 3, 5, 6, 8, 10, 12]

chordKeyNumbers  = []

for x in range (numberOfNotes):
  if chordProgressionNumbers[x] in diatonicChordsNumbers:
    isDiatonic = True

keyAdjust = keyNumber[0] - 1
keyAdjustedList = []

if isDiatonic:
  keyAdjustedList = [x + keyAdjust for x in diatonicChordsNumbers]
  for x in range(len(keyAdjustedList)):
    if keyAdjustedList[x] > 12:
      keyAdjustedList[x] = keyAdjustedList[x] - 12
  for x in range(numberOfNotes):
    chordKeyNumbers.append(keyAdjustedList.index(chordProgressionNumbers[x]))
      
else:
  print('not diatonic chords')

def numberToRomanNumeral(num):
  return romanNumerals[num]

romanChordProgression = []
romanChordsOnly = []

for x in range (numberOfNotes):
  romanChordProgression.append(numberToRomanNumeral(chordKeyNumbers[x]))
  romanChordProgression.append(inversionsGlobal[x])
  romanChordProgression.append(' - ')

for x in range(numberOfNotes*3):
  if romanChordProgression[x] in romanNumerals:
    romanChordsOnly.append(romanChordProgression[x])

print(f'The chord progression is {removeSymbols(romanChordProgression)}')

for x in range (numberOfNotes):
  if x+1 < numberOfNotes:
    if romanChordsOnly[x+1] == 'V':
      if romanChordsOnly[x] == 'I' or romanChordsOnly[x] == 'i' or romanChordsOnly[x] == 'IV' or romanChordsOnly[x] == 'ii':
        print('imperfect cadence between chords ' + str(x+1) + ' and ' + str(x+2))
      elif romanChordsOnly[x] == 'IV' or romanChordsOnly[x] == 'iv':
         print('plagal cadence between chords ' + str(x+1) + ' and ' + str(x+2))
    elif romanChordsOnly[x] == 'V':
      if romanChordsOnly[x+1] == 'I' or romanChordsOnly[x+1] == 'i':
        print('perfect cadence between chords ' + str(x+1) + ' and ' + str(x+2))
      elif romanChordsOnly[x+1] == 'vi':
        print('interrupted cadence between chords ' + str(x+1) + ' and ' + str(x+2))

#---checking for consecutive intervals---

def consecutiveIntervals (voice1, voice2, intervalInSemitones):

  foundConsecutiveIntervals = False
  firstvoice = False
  secondvoice = False

  if numberOfNotes > 1:
   for x in range(numberOfNotes - 1):
     firstvoice = False
     secondvoice = False

     difference1 = voice1[x] - voice2[x]
     if difference1 == intervalInSemitones:
        firstvoice = True
     difference2 = voice1[x+1] - voice2[x+1]
     if difference2 == intervalInSemitones:
       secondvoice = True
     if firstvoice and secondvoice:
       foundConsecutiveIntervals = True
  return(foundConsecutiveIntervals)

def consecutiveIntervalsAcrossVoices (intervalInSemitones):

  sopranobass = consecutiveIntervals(sopranoNumbers, bassNumbers, intervalInSemitones)
  sopranoalto = consecutiveIntervals(sopranoNumbers, altoNumbers, intervalInSemitones)
  sopranotenor = consecutiveIntervals(sopranoNumbers, tenorNumbers, intervalInSemitones)
  altobass = consecutiveIntervals(altoNumbers, bassNumbers, intervalInSemitones)
  altotenor = consecutiveIntervals(altoNumbers, tenorNumbers, intervalInSemitones)
  tenorbass = consecutiveIntervals(tenorNumbers, bassNumbers, intervalInSemitones)

  return (sopranobass == True or sopranoalto == True or sopranotenor == True or altobass == True or tenorbass == True or altotenor == True)

if consecutiveIntervalsAcrossVoices(12):
  print('There are consecutive octaves')
else:
  print('There are no consecutive octaves')

if consecutiveIntervalsAcrossVoices(7):
  print('There are consecutive fifths')
else:
  print('There are no consecutive fifths')

