#neg23
Python script to automate loudness normalization (to -23 LUFS) using <a href="http://www.ffmpeg.org/">FFmpeg</a> and <a href="http://sox.sourceforge.net/">sox</a>. Run the program with a single argument, either an audiofile or a directory, and the files will be handed to FFmpeg for EBU R128 analysis and then to sox for gain adjustment. Processing, even large files, is very fast. Processed files are saved in the input directory (in a subfolder called neg23.) Correct usage: 
```bash
$ neg23 somefile.wav
$ neg23 /directory/for/batch/processing/
```

If you want to be able to run neg23.py from the terminal by just typing 'neg23', first make the script executable and then copy it to /usr/bin. Like this:
```bash
$ chmod +x neg23.py
$ cp neg23.py /usr/bin/neg23
```

You should have both FFmpeg and sox installed on your machine.
```bash
$ brew install ffmpeg
$ brew install sox
```
