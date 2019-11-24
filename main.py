import sounddevice as sd
from scipy.io.wavfile import write
import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from copy import deepcopy


fs = 6000  # Sample rate
seconds = 1  # Duration of recording
# print("Recording...")
# myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
sd.wait()  # Wait until recording is finished 
# write('sampled_voice.wav', fs, myrecording)  # Save as WAV file 
# print("Done!")

print("Playing...")
filename = 'sampled_voice.wav'
# Extract data and sampling rate from file
data, fs = sf.read(filename, dtype='float32')
sd.play(data, fs)
status = sd.wait()  # Wait until file is done playing`
print("Done!")

#------------------------------------------------------------------------------------------------------------------------------------

time_pts = np.linspace(0, seconds, int(seconds*fs))

figure = plt.figure()
plt.subplots_adjust(left=0.05, bottom=0.05, right=0.98, top=0.95, wspace=0.14, hspace=0.28)

axis_time = figure.add_subplot(3,2,3)
axis_time.clear()
axis_time.set_title("Time domain value", fontsize=6)
axis_time.set_xlabel("Time", fontsize=6)
axis_time.set_ylabel("Value", fontsize=6)
axis_time.tick_params(axis='both', labelsize=5)
axis_time.plot(time_pts, data, 'r-')
axis_time.set_xticks(np.linspace(0, seconds, 10))
axis_time.set_yticks(np.linspace(min(data)-0.1, max(data)+0.1, 10))
axis_time.autoscale(enable=True, axis='x', tight=True)
plt.grid(True)

#-------------------------------------------------------------------------------------------------------------------------------------

start_freq = -3000
end_freq = 3000
step = 1
freq_pts = np.arange(start_freq, end_freq, step)

def dtft():
	samples = len(data)
	n = np.arange(samples)
	freq_pts_dtft = freq_pts.reshape((len(freq_pts), 1))
	M = np.exp(-2j * np.pi * n * freq_pts_dtft / fs)
	return np.dot(M, data)

print("Calculating dtft...")
dtft_data = dtft();
print("Done!")

axis_dtft = figure.add_subplot(3,2,1)
axis_dtft.clear()
axis_dtft.set_title("Frequency domain value (Magnitude)", fontsize=6)
axis_dtft.set_xlabel("Frequency", fontsize=6)
axis_dtft.set_ylabel("Magnitude", fontsize=6)
axis_dtft.tick_params(axis='both', labelsize=5)
axis_dtft.plot(freq_pts, np.absolute(dtft_data), 'r-')
axis_dtft.set_xticks(np.linspace(start_freq, end_freq, 13))
axis_dtft.set_yticks(np.linspace(0, max(np.absolute(dtft_data))+0.1, 10))
axis_dtft.autoscale(enable=True, tight=True)
plt.grid(True)

axis_dtft_phase = figure.add_subplot(3,2,2)
axis_dtft_phase.clear()
axis_dtft_phase.set_title("Frequency domain value (Phase)", fontsize=6)
axis_dtft_phase.set_xlabel("Frequency", fontsize=6)
axis_dtft_phase.set_ylabel("Angle(Radians)", fontsize=6)
axis_dtft_phase.tick_params(axis='both', labelsize=5)
axis_dtft_phase.plot(freq_pts, np.angle(dtft_data), 'r-')
axis_dtft_phase.set_xticks(np.linspace(start_freq, end_freq, 13))
axis_dtft_phase.set_yticks(np.linspace(-np.pi, np.pi, 10))
axis_dtft_phase.autoscale(enable=True, tight=True)
plt.grid(True)

#----------------------------------------------------------------------------------------------------------------------------------

def idtft():
	n = np.arange(len(data))
	n = n.reshape((len(n), 1))
	freq_pts_idtft = freq_pts.reshape((1, len(freq_pts)))
	M = np.exp(2j * np.pi * freq_pts_idtft * n / fs)
	return np.dot(M, (1/fs)*dtft_data)

print("Calculating idtft...")
idtft_data = np.real(idtft());
print("Done!")

axis_idtft = figure.add_subplot(3,2,4)
axis_idtft.clear()
axis_idtft.set_title("Time domain value after IDTFT", fontsize=6)
axis_idtft.set_xlabel("Time", fontsize=6)
axis_idtft.set_ylabel("Value", fontsize=6)
axis_idtft.tick_params(axis='both', labelsize=5)
axis_idtft.plot(time_pts, idtft_data, 'r-')
axis_idtft.set_xticks(np.linspace(0, seconds, 10))
axis_idtft.set_yticks(np.linspace(min(idtft_data)-0.1, max(idtft_data)+0.1, 10))
axis_idtft.autoscale(enable=True, axis='x', tight=True)
plt.grid(True)

print("Playing...")
sd.play(idtft_data, fs)
status = sd.wait()  # Wait until file is done playing`
print("Done!")

#------------------------------------------------------------------------------------------------------------------------------------
dtft_data_original = deepcopy(dtft_data)
dtft_data = np.asarray([0]*1800 + dtft_data.tolist()[1800:-1800] + [0]*1800)

print("Calculating idtft...")
filtered_data = np.real(idtft())
print("Done!")

axis_idtft_filter = figure.add_subplot(3,2,5)
axis_idtft_filter.clear()
axis_idtft_filter.set_title("Time domain value after filter", fontsize=6)
axis_idtft_filter.set_xlabel("Time", fontsize=6)
axis_idtft_filter.set_ylabel("Value", fontsize=6)
axis_idtft_filter.tick_params(axis='both', labelsize=5)
axis_idtft_filter.plot(time_pts, filtered_data, 'r-')
axis_idtft_filter.set_xticks(np.linspace(0, seconds, 10))
axis_idtft_filter.set_yticks(np.linspace(min(filtered_data)-0.1, max(filtered_data)+0.1, 10))
axis_idtft_filter.autoscale(enable=True, axis='x', tight=True)
plt.grid(True)

print("Playing...")
sd.play(filtered_data, fs)
status = sd.wait()  # Wait until file is done playing`
print("Done!")

#-------------------------------------------------------------------------------------------------------------------------------------

dtft_data = np.absolute(dtft_data_original)

print("Calculating idtft...")
absolute_data = np.real(idtft())
print("Done!")

axis_idtft_zero_phase = figure.add_subplot(3,2,6)
axis_idtft_zero_phase.clear()
axis_idtft_zero_phase.set_title("Time domain value with zero phase", fontsize=6)
axis_idtft_zero_phase.set_xlabel("Time", fontsize=6)
axis_idtft_zero_phase.set_ylabel("Value", fontsize=6)
axis_idtft_zero_phase.tick_params(axis='both', labelsize=5)
axis_idtft_zero_phase.plot(time_pts, absolute_data, 'r-')
axis_idtft_zero_phase.set_xticks(np.linspace(0, seconds, 10))
axis_idtft_zero_phase.set_yticks(np.linspace(min(absolute_data)-0.1, max(absolute_data)+0.1, 10))
axis_idtft_zero_phase.autoscale(enable=True, axis='x', tight=True)
plt.grid(True)

print("Playing...")
sd.play(absolute_data, fs)
status = sd.wait()  # Wait until file is done playing`
print("Done!")

#--------------------------------------------------------------------------------------------------------------------------

plt.show()