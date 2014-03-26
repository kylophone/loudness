#!/usr/bin/python
import os, sys, re, subprocess, string, mimetypes, math

#Directory Mode:
if len(sys.argv) == 2 and os.path.isdir(sys.argv[1]):
	os.chdir(sys.argv[1])
	fileList = os.listdir(sys.argv[1])
	for thisFile in fileList:
		if thisFile.startswith(".") or mimetypes.guess_type(re.escape(thisFile))[0] == None or not mimetypes.guess_type(re.escape(thisFile))[0].startswith("audio"):
			continue
		print "Processing " + thisFile + "...",
		proc = subprocess.Popen("ffmpeg -nostats -i " + re.escape(thisFile) + " -filter_complex ebur128 -f null - 2>&1| tail -n 14", shell = True, stdout = subprocess.PIPE)
		stats = proc.communicate()[0]
		#Error-check:
		if "No such file" in stats or "could not find" in stats or "Error" in stats:
			print "Error."
			continue
		#Get IL:
		IL = stats.split("\n")[6]
		IL = IL.replace("LUFS", "")
		IL = IL.replace("I:", "")
		#Adjust Gain:
		dB = (-1 * (23.0 + float(IL)))
		linear = 10 ** (dB / 20)
		if not os.path.isdir("./neg23"):
			os.makedirs("neg23")
		subprocess.Popen("ffmpeg -v 0 -y -i " + re.escape(thisFile) + " -af 'volume=" + str(linear) + "' ./neg23/" + re.escape(thisFile), shell = True)
		print "Done"
	print "Batch complete."
#Singlefile Mode:
elif len(sys.argv) == 2 and os.path.isfile(sys.argv[1]):
	os.chdir(os.path.dirname(sys.argv[1]))
	if sys.argv[1].startswith(".") or mimetypes.guess_type(re.escape(sys.argv[1]))[0] == None or not mimetypes.guess_type(re.escape(sys.argv[1]))[0].startswith("audio"):
			sys.exit("Not a valid audio file.")
	print "Processing " + sys.argv[1] + "...",
	proc = subprocess.Popen("ffmpeg -nostats -i " + re.escape(sys.argv[1]) + " -filter_complex ebur128 -f null - 2>&1| tail -n 14", shell = True, stdout = subprocess.PIPE)
	stats = proc.communicate()[0]
	#Error-check:
	if "No such file" in stats or "could not find" in stats or "Error" in stats:
		sys.exit("Error.")
	#Get IL:
	IL = stats.split("\n")[6]
	IL = IL.replace("LUFS", "")
	IL = IL.replace("I:", "")
	#Adjust Gain:
	dB = (-1 * (23.0 + float(IL)))
	linear = 10 ** (dB / 20)
	if not os.path.isdir("./neg23"):
		os.makedirs("neg23")
	subprocess.Popen("ffmpeg -v 0 -y -i " + re.escape(sys.argv[1]) + " -af 'volume=" + str(linear) + "' ./neg23/" + re.escape(os.path.basename(sys.argv[1])), shell = True)
	print "Done"
else:
	print "Please provide a single file or directory.\nCorrect usage: neg23 somefile.wav OR neg23 /directory/for/batch/processing/"

