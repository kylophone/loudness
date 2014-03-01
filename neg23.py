#!/usr/bin/python
import os, sys, subprocess, re
if len(sys.argv) == 2:
	
	#Passes the audiofile to FFmpeg, parses the output and saves the loudness as a string called loudness.
	AudioFileIn = re.escape(sys.argv[1])
	print "Processing " + os.path.basename(sys.argv[1]) + "..."
	proc = subprocess.Popen("ffmpeg -nostats -i " + AudioFileIn + " -filter_complex ebur128 -f null - 2>&1 | tail | grep I: | tr -d I: | tr -d LUFS | tr -d \ ", shell=True, stdout=subprocess.PIPE)
	loudness = proc.communicate()[0]

	#Passes the audiofile and its loudness to sox for gain adjustment.
	#the new filename has a "_neg23" appended and placed in the directory of the original file. Output file extension is the same as the input file.
	AudioFileOut = os.path.splitext(AudioFileIn)[0] + "_neg23" + os.path.splitext(AudioFileIn)[1]
	os.system("sox " + AudioFileIn + " " + AudioFileOut + " gain " + str(-1 * (23.0 + float(loudness))))
	print "Done!" 

else:
	print "Please provide a single input file. Correct usage: neg23 somefile.wav"
