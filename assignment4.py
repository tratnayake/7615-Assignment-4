'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  SOURCE FILE:    assignment4.py
--
--  AUTHORS:         Thilina Ratnayake & Justin Tom
--
--  PROGRAM:        Takes an audio clip and performs 5 manipulations on it. Listed 
--  				below
--
--  FUNCTIONS:      fadeIn()
--                  slowDown()
--                  speedUp()
--                  reverseSounds()
-- 					blendSounds()
--
--  DATE:           October 19, 2015
--
--  REVISIONS:
--
--  NOTES:
--  The program requires the PyDub library. (pip install pydub)
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#Imrports
from pydub import AudioSegment #Used for manipulating songs
from pydub.effects import * #PydubAPI for doing signal processing
import wave, warnings, os


#Simply fades in until 5 seconds into the start of the clip
def fadeIn(clip,value):
	return clip.fade_in(5000)

#Slows down the speed of the song (changes the pitch)
def slowDown(song,value):
	#Export a slice of the song to slow down
	song.export("slowSongBefore.wav", 'wav')
	#Open Old Clip
	originalClip = wave.open("slowSongBefore.wav","r")
	#Open a new clip file
	slowClip = wave.open("SLOW.wav","w")
	#Set the parameters of the new clip to have the same ones as the old clip
	slowClip.setparams(originalClip.getparams())
	#Grab all the frames of the original clip
	originalFrames = originalClip.readframes(originalClip.getnframes())
	#Set the framerate to consume those frames  at a certain volume
	slowClip.setframerate(int(round(originalClip.getframerate() * value)))
	#Write the original frames to file using new framerate
	slowClip.writeframes(originalFrames)
	#close the file
	slowClip.close()
	#Export to the sound object	
	changedSlowClip = AudioSegment.from_file("SLOW.wav")

	#Delete the unnecessary ones
	os.remove("slowSongBefore.wav")
	os.remove("SLOW.wav")
	return changedSlowClip

#Speeds up the tempo of the song, also does a pitch change.
def speedUp(song,value):
	#Export a slice of the song to slow down
	song.export("speedSongBefore.wav", 'wav')
	#Open clip
	originalClip = wave.open("speedSongBefore.wav","r")

	fastClip = wave.open("FAST.wav","w")
	fastClip.setparams(originalClip.getparams())

	originalFrames = originalClip.readframes(originalClip.getnframes())
	fastClip.setframerate(int(round(originalClip.getframerate() * value)))

	fastClip.writeframes(originalFrames)
	fastClip.close()

	os.remove("speedSongBefore.wav")
	changedFastClip = AudioSegment.from_file("FAST.wav")
	os.remove("FAST.wav")
	return changedFastClip

#Plays the song in reverse
def reverseSound(song):
	reversedClip = song[0:10000].reverse()
	#reversedClip.export("cheerleaderReversed.wav","wav")
	return reversedClip

#Crossfades a song with another track.
def blendSounds(song1,song2):
	song1clipped = song1
	song2clipped = song2
	blendedSound = song1clipped.append(song2clipped,crossfade=5000)
	#blendedSound.export("blended.wav","wav")
	return blendedSound



if __name__ == "__main__":

	#Break the song into chunks
	song = AudioSegment.from_file(sys.argv[1])
	chunk1 = song
	length = len(song)/4
	chunk2 = song[0:length]
	chunk3 = song[length+1:length*2]
	chunk4 = song[length*2+1:length*3]
	chunk5 = song[length*3+1:length*4]

	#Apply operations to the chunks
	chunk1Changed = fadeIn(chunk1,6)
	chunk2Changed = slowDown(chunk2,0.5)
	chunk3Changed = speedUp(chunk3, 1.25)
	chunk4Changed = reverseSound(chunk4)
	chunk5Changed = blendSounds(chunk5,AudioSegment.from_mp3(sys.argv[2]))

	#Create outputs to see that we actually did something
	chunk1Changed.export("tests/TEST1FADEIN.wav","wav")
	chunk2Changed.export("tests/TEST2SLOWDOWN.wav","wav")
	chunk3Changed.export("tests/TEST3SPEEDUP.wav","wav")
	chunk4Changed.export("tests/TEST4REVERSE.wav","wav")
	chunk5Changed.export("tests/TEST5BLEND.wav","wav")	

	#Export the new song
	newSong = chunk1Changed.append(chunk2Changed.append(chunk3Changed.append(chunk4Changed.append(chunk5Changed))))
	newSong.export("outputFiles/ClipModifiedCHANGED.wav", 'wav')

