from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import math
import sounddevice as sd
from scipy.io.wavfile import write

#Appends zeros on to a list of data to make the len of that list a power of two.
def power_2(data):
    x = math.ceil(math.log(len(data), 2))
    padding = 2**x - len(data)
    for i in range(padding):
            data.append(0)
    return data

#FFT algorithm. Computes the intensity of the different frequency components found in a signal.
def FFT(x):
    N = len(x)

    if N == 1:
        return x

    else:
        Even_x = x[::2]
        Odd_x = x[1::2]

        Even_val = FFT(Even_x)
        Odd_val = FFT(Odd_x)

        y = [0]*N
        for j in range(int(N/2)):
            w1 = math.cos(2*math.pi*j/N)
            w2 = -math.sin(2*math.pi*j/N)
            w = complex(w1, w2)
            y[j] = Even_val[j] + (Odd_val[j])*w
            y[int(j+N/2)] = Even_val[j] - (Odd_val[j])*w
        return y

#Computes the magnitude of FFT results and calculates proper frequency
def magnitude(fft_values, samplingRate):
    fft_values = fft_values[:len(fft_values)//2]
    y = [0]*len(fft_values)
    x = [(samplingRate*i)/(len(fft_values)*2) for i in range(len(fft_values))]

    for i, ele in enumerate(fft_values):
        y[i] = (math.sqrt((ele.real**2)+ele.imag**2))/(len(fft_values)/2)
    return x, y

#Returns the frequency with the strongest amplitude.
def getCarrierFrequency(input_list, freq):
    max_value = max(input_list)
    index = input_list.index(max_value)
    index = freq[index]
    return index


#creates audio file
fs = 44100  # Sample rate
seconds = 1  # Duration of recording
print('start')
myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
sd.wait()  # Wait until recording is finished
print('stop')
write('output.wav', fs, myrecording)

#Initializes layout of plot
plot1 = plt.subplot2grid((3, 3), (0, 0), colspan=3)
plot2 = plt.subplot2grid((3, 3), (1, 0), rowspan=3, colspan=3)

#Extract amplitude data from audio file
input_data = read("output.wav")
audio = input_data[1]
time = [i/fs for i in range(len(audio))]
amplitude = [val[0] for val in audio]

#Creates Amplitude vs Time graph of audio signal
max_value = max(amplitude)
plot1.set_xlim([0.400, 0.5])
plot1.set_ylim([-max_value, max_value])
plot1.plot(time, amplitude, color = 'g')
plot1.set_ylabel(["Amplitude"])
plot1.set_xlabel(["Time in Seconds"])

#Use FFT algorithm to convert data from the time domain to the frequency domain. 
#Returns most prominent frequency contained in the audio data.
result = power_2(amplitude)
sampleRate = fs
frequency, amplitude = magnitude(FFT(result),sampleRate)
carrier_frequency = getCarrierFrequency(amplitude, frequency)

#Creates Amplitude vs Frequency graph of audio signal
print(f'carrier frequency: {carrier_frequency}')
plot2.plot(frequency, amplitude)
plot2.set_xlim([0, carrier_frequency*2])
plot2.set_ylabel(["Amplitude"])
plot2.set_xlabel(["Frequency"])
plt.tight_layout()
plt.show()


