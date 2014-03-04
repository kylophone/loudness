#!/usr/bin/python
import os, sys, subprocess, re, mimetypes

def normalize(audioIn, audioOut):
	print "Processing " + os.path.basename(audioIn) + "...",
	audioIn = re.escape(audioIn)
	audioOut = re.escape(audioOut)
	#Passes the audiofile to FFmpeg, parses the output and gets the loudness.
	proc = subprocess.Popen("ffmpeg -nostats -i " + audioIn + " -filter_complex ebur128 -f null - 2>&1 | tail | grep I: | tr -d I: | tr -d LUFS | tr -d \ ", shell = True, stdout = subprocess.PIPE)
	loudness = proc.communicate()[0]
	#Passes the audiofile and its loudness to sox for gain adjustment.
	os.system("sox " + audioIn + " " + audioOut + " gain " + str(-1 * (23.0 + float(loudness))))
	print "Done!"

def isAudio(inputPath):
	return mimetypes.guess_type(re.escape(inputPath))[0].startswith("audio")

#fix for relative path input 
if len(sys.argv) == 2:
	if sys.argv[1].startswith("./"):
			sys.argv[1] = os.getcwd() + "/" + sys.argv[1][2:]
	elif sys.argv[1].startswith("../"):
		sys.argv[1] = os.path.dirname(os.getcwd()) +  "/" + sys.argv[1][3:]
	elif sys.argv[1].startswith("/"):
		sys.argv[1] = sys.argv[1]
	else:
		sys.argv[1] = os.getcwd() + "/" + sys.argv[1]

#Batch
if len(sys.argv) == 2 and os.path.isdir(sys.argv[1]):
	fileList = os.listdir(sys.argv[1])
	for thisFile in fileList:
		if not thisFile.startswith(".") and os.path.isfile(sys.argv[1] + "/" + thisFile):
			if isAudio(os.path.dirname(sys.argv[1]) + "/" + thisFile):
				pathIn = sys.argv[1] + "/" + thisFile
				pathOut = sys.argv[1] + "/neg23/" + thisFile
				if not os.path.isdir(os.path.dirname(pathOut)):
					os.mkdir(os.path.dirname(pathOut))
				normalize(pathIn, pathOut)
	print "Batch complete."
#Single
elif len(sys.argv) == 2 and os.path.isfile(sys.argv[1]) and isAudio(sys.argv[1]): 
	pathIn = sys.argv[1]
	pathOut = os.path.dirname(sys.argv[1]) + "/neg23/" + os.path.basename(pathIn)
	if not os.path.isdir(os.path.dirname(pathOut)):
		os.mkdir(os.path.dirname(pathOut))
	normalize(pathIn, pathOut)
else:
	print "Please provide a single file or directory.\nCorrect usage: neg23 somefile.wav OR neg23 /directory/for/batch/processing/"
