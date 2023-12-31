import numpy
import scipy.io.wavfile
from matplotlib import pyplot, mlab
from collections import defaultdict

SAMPLE_RATE = 44100  # Hz
WINDOW_SIZE = 2048  # размер окна, в котором делается fft
WINDOW_STEP = 512  # шаг окна


def get_wave_data(wave_filename):
    sample_rate, wave_data = scipy.io.wavfile.read(wave_filename)
    assert sample_rate == SAMPLE_RATE, sample_rate
    if isinstance(wave_data[0], numpy.ndarray):  # стерео
        wave_data = wave_data.mean(1)
    return wave_data

def get_wave_data2(wave_filename):
    sample_rate, wave_data2 = scipy.io.wavfile.read(wave_filename)
    assert sample_rate == SAMPLE_RATE, sample_rate
    if isinstance(wave_data2[0], numpy.ndarray):  # стерео
        wave_data2 = wave_data2.mean(1)
    return wave_data2



def show_specgram(wave_data):
    fig = pyplot.figure()
    ax = fig.add_axes((0.1, 0.1, 0.8, 0.8))
    ax.specgram(wave_data,
                NFFT=WINDOW_SIZE, noverlap=WINDOW_SIZE - WINDOW_STEP, Fs=SAMPLE_RATE)
    pyplot.show()

def show_specgram2(wave_data2):
    fig = pyplot.figure()
    ax = fig.add_axes((0.1, 0.1, 0.8, 0.8))
    ax.specgram(wave_data2,
                NFFT=WINDOW_SIZE, noverlap=WINDOW_SIZE - WINDOW_STEP, Fs=SAMPLE_RATE)
    pyplot.show()


def get_fingerprint(wave_data, WINDOW_OVERLAP=None):
    # pxx[freq_idx][t] - мощность сигнала
    pxx, _, _ = mlab.specgram(wave_data,
                              NFFT=WINDOW_SIZE, noverlap=WINDOW_OVERLAP, Fs=SAMPLE_RATE)
    band = pxx[15:250]  # наиболее интересные частоты от 60 до 1000 Hz
    return numpy.argmax(band.transpose(), 1)  # max в каждый момент времени

def get_fingerprint2(wave_data2, WINDOW_OVERLAP=None):
    # pxx[freq_idx][t] - мощность сигнала
    pxx, _, _ = mlab.specgram(wave_data2,
                              NFFT=WINDOW_SIZE, noverlap=WINDOW_OVERLAP, Fs=SAMPLE_RATE)
    band = pxx[15:250]  # наиболее интересные частоты от 60 до 1000 Hz
    return numpy.argmax(band.transpose(), 1)  # max в каждый момент времени


def compare_fingerprints(base_fp, fp):
    base_fp_hash = defaultdict(list)
    for time_index, freq_index in enumerate(base_fp):
        base_fp_hash[freq_index].append(time_index)
    matches = [t - time_index  # разницы времен совпавших частот
               for time_index, freq_index in enumerate(fp)
               for t in base_fp_hash[freq_index]]




    pyplot.clf()
    pyplot.hist(matches, 1000)
    pyplot.show()



wave_data = get_wave_data('song.wav')
wave_data2 = get_wave_data2('broadcast.wav')
# show_specgram(wave_data)
# show_specgram2(wave_data2)


fin = get_fingerprint(wave_data)
fin2 = get_fingerprint2(wave_data2)
print(get_fingerprint(wave_data))
print("*****")
print(get_fingerprint2(wave_data2))
compare_fingerprints(fin2, fin)
# print(compare_fingerprints('broadcast.wav', 'song.wav'))
