# 4-part harmony checker!

# 1. check they make chords (triads)
# 2. check for consecutive octaves
# 3. check for consecutive 5ths
# 4. check distances between parts
# 5. output chord sequence and check it makes a cadence
# 6. make it work for 7ths, prepared + resolved

# things to do next:
# -> fully test consecutives function 
# (23/09: i think it works?? haven't found one where it doesn't)
# output chord sequence - done!! - this broke for 3  or more chords, idk why
# -> user inputs key, then work out chord progression in roman numerals, check it makes a cadence
# --> not working yet but i'm tryinggg
# output chord's inversion + include this in chord progression

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

numberOfNotes = int(input('how many chords are there?'))

print('type 1 or 2 after the note to increase the octave')

for x in range(numberOfNotes):
  sopranoNotes = input('enter the next soprano note')
  soprano.append(sopranoNotes)
  altoNotes = input('enter the next alto note')
  alto.append(altoNotes)
  tenorNotes = input('enter the next tenor note')
  tenor.append(tenorNotes)
  bassNotes = input('enter the next bass note')
  bass.append(bassNotes)

#---calling notes to numbers function---

sopranoNumbers = notesToNumbers(soprano)
altoNumbers = notesToNumbers(alto)
tenorNumbers = notesToNumbers(tenor)
bassNumbers = notesToNumbers(bass)

#---checking if the notes make a triad---

triadCount = 0
chordProgressionNumbers = []
tonalityProgression = []

for x in range (numberOfNotes):
  thisChord = []
  thisChord.append(sopranoNumbers[x])
  thisChord.append(altoNumbers[x])
  thisChord.append(tenorNumbers[x])
  thisChord.append(bassNumbers[x])
  thisChord.sort()
  chordProgressionNumbers.append(thisChord[0])
  
  
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
    progressionToPrintList.append('m - ')
  elif tonalityProgression[x] == 'major':
    progressionToPrintList.append('- ')
progressionToPrintString = str(progressionToPrintList)
  
# this bit broke and idk why
for x in range (len(progressionToPrintString)):
  if progressionToPrintString[x:x+1] in "'[ ],":
    progressionToPrintString = progressionToPrintString.replace(progressionToPrintString[x:x+1], '')
progressionToPrintString = progressionToPrintString.replace(progressionToPrintString[-1], '')
progressionToPrintString = progressionToPrintString[:-1]
print('The chord progression is ' + progressionToPrintString)

#---chord progression in roman numerals + cadences---

# changing this because it only works for cmaj 
# logic: if key in chord progression, that chord = 1 then calculate around from that
# also use diatonicchordsnumbers to help in that
# (might not use this because it relies on there being a chord 1 in it)
romanNumerals = []

keyStr = input('What key is it in?')
keyList = [keyStr]
keyNumber = notesToNumbers(keyList)

# i probably don't need this bit if i get the rest of it working (see further comment)
if keyStr[-1:-2] == 'm':
  keyTonality = 'minor'
  romanNumerals = ['blank', 'i', 'ii°', 'III', 'iv', 'V', 'VI', 'vii°']
else:
  keyTonality = 'major'
  romanNumerals = ['blank', 'I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii°' ]

diatonicChordsNumbers = [1, 3, 5, 6, 8, 10, 12]

chordKeyNumbers  = []

#for x in range (numberOfNotes):
  #if chordProgressionNumbers[x] in diatonicChordsNumbers:

isDiatonic = True
# -> convert into roman numerals and then if maj/min make capital or not

#fix this bit so it works in every key
# -> done, but it doesn't work because the adjusted number might not be in diatonic chord list
keyAdjust = keyNumber[0] - 1

if isDiatonic:
  for n in range (numberOfNotes):
    for i in range (6):
      diChoNumAdjusted = diatonicChordsNumbers[i] + keyAdjust
      if chordProgressionNumbers[n] == diChoNumAdjusted:
        if diChoNumAdjusted > 12:
          diChoNumAdjusted = diChoNumAdjusted - 12
        chordKeyNumbers.append(diChoNumAdjusted)
      
else:
  print('not diatonic chords')

print(chordKeyNumbers)

#this bit doesn't work either
romanChordProgression = []
for x in range (numberOfNotes):
  romanChordProgression.append(romanNumerals[chordKeyNumbers[x]])
print(romanChordProgression)

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

