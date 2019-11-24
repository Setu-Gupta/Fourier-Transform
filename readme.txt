sources:

1.Code to record and playback sound:
	https://realpython.com/playing-and-recording-sound-python/

2. Code inspiration for dtft:
	https://jakevdp.github.io/blog/2013/08/28/understanding-the-fft/

Dependencies:
	sounddevice
	scipy
	soundfile
	matplotlib
	numpy
	copy

How to run:
	On a 32bit linux machine type: "python3 main.py" (without quotes) on the terminal.
	
Results:
	BW: 1500Hz
	Differences after filter: The voice appeared to be deeper, and the time plot had fewer sharp edges and was smoothened out.
    Differences after zero_phase: The voice appeared to be garbled up and sounded like noise. Nothing was clear.
