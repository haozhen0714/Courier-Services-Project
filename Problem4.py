import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import copy
from fastdtw import fastdtw
import IPython.display
from scipy.spatial.distance import euclidean


def dtw(s, t, window):
    n, m = len(s), len(t)

    w = np.max([window, abs(n - m)])
    dtw_matrix = np.zeros((n + 1, m + 1))

    for i in range(n + 1):
        for j in range(m + 1):
            dtw_matrix[i, j] = np.inf

    # initialize first position to 0
    dtw_matrix[0, 0] = 0

    for i in range(1, n + 1):
        for j in range(np.max([1, i - w]), np.min([m, i + w]) + 1):
            dtw_matrix[i, j] = 0

    for i in range(1, n + 1):
        for j in range(np.max([1, i - w]), np.min([m, i + w]) + 1):
            cost = abs(s[i - 1] - t[j - 1])
            # take minimum values among three values,top right,left and bottom
            last_min = np.min([dtw_matrix[i - 1, j], dtw_matrix[i, j - 1], dtw_matrix[i - 1, j - 1]])

            dtw_matrix[i, j] = cost + last_min

    return dtw_matrix


print("Simple implementation of Dynamic Time Warping (DTW)\n")
x = np.array([1, 6, 4, 9, 9, 2, 1, 5, 7, 3])
y = np.array([1, 7, 2, 3, 3, 9, 4, 8, 6, 3])

distance, path = fastdtw(x, y, dist=euclidean)
array = dtw(x, y, window=3)
warp_array = np.delete(np.delete(array, 0, 0), 0, 1)
print(warp_array)
#The last element (last row, last column) of the matrix is the distance of the two series
last_element = array[-1:, -1:]
print('Distance:', last_element)
print('Distance from dtw library:', distance)
print('Warping path:\n', path, '\n\n')


def load_wav(name):
    # load .wav audio file to get y: audio time series, and sr: sampling rate of y
    y_value, sr_value = librosa.load('P4/Audio/' + name + '.wav')
    return y_value, sr_value


def display_waveform(name, y_value, sr_value):
    # save waveform of audio into jpg
    plt.figure(figsize=(14, 5))
    librosa.display.waveplot(y=y_value, sr=sr_value)
    plt.savefig('P4/Waveform of ' + name + '.jpg')


def convert_and_preprocess_mfcc(y_value, sr_value):
    # convert data to Mel-frequency cepstral coefficients (MFCCs)
    mfcc_value = librosa.feature.mfcc(y_value, sr_value)
    # remove mean and normalize each column of MFCC
    mfcc_cp = copy.deepcopy(mfcc_value)
    for i in range(mfcc_value.shape[1]):
        mfcc_cp[:, i] = mfcc_value[:, i] - np.mean(mfcc_value[:, i])
        mfcc_cp[:, i] = mfcc_cp[:, i] / np.max(np.abs(mfcc_cp[:, i]))
    return mfcc_cp


def get_window_size(mfcc_value, mfcc_test_value):
    # compute the average window size of training
    window_size_value = 0
    for i in range(len(mfcc_value)):
        window_size_value += mfcc[i].shape[1]
    window_size_value = int(window_size_value/len(mfcc_value))
    # find the size of distance window
    dists_value = np.zeros(mfcc_test_value.shape[1] - window_size_value)
    return window_size_value, dists_value


def get_distances(name, window_size_value, dists_value, mfcc_test_value, mfcc_value):
    # for each ith window,
    for i in range(len(dists)):
        # get the mfccTest with window size = average window size of training
        mfcci = mfcc_test_value[:, i:i + window_size_value]
        # compute distances between mfccTest and mfcc train using fastdtw and the average distance
        for j in range(len(mfcc_value)):
            dists_value[i] += fastdtw(mfcc_value[j].T, mfcci.T, dist=lambda x, y: np.exp(np.linalg.norm(x - y, ord=1)))[0]
        dists_value[i] /= len(mfcc_value)
    plt.plot(dists_value)
    plt.savefig('P4/Plotting of ' + name + ' distance.jpg')


def get_desired_word_audio(dists_value, name):
    # get the window with minimum distance (the window with desired word)
    word_match_idx = dists_value.argmin()
    # get the starting and ending index of the window of desired word
    word_match_idx_bnds = np.array([word_match_idx, np.ceil(word_match_idx + window_size)])
    samples_per_mfcc = 512
    word_samp_bounds = 1 + (word_match_idx_bnds * samples_per_mfcc)
    # get the boundaries of desired word from test audio series
    # save in .wav file
    word = yTest[int(word_samp_bounds[0]): int(word_samp_bounds[1])]
    audio = IPython.display.Audio(data=word, rate=srTest)
    with open('P4/Audio/' + name + '.wav', 'wb') as f:
        f.write(audio.data)


print("Implementation of DTW in speech recognition\n")
print("- Identify 'kurier J&T ekspres' word -\n")
fileTest = "harian_metro_jnt_ekspres"
fileWordAstro = "astro_kurier_jnt_ekspres"
fileWordInsight = "insight_kurier_jnt_ekspres"
fileDesiredWord = "P4 kurier_jnt_ekspres"
yTest, srTest = load_wav(fileTest)
y1, sr1 = load_wav(fileWordAstro)
y2, sr2 = load_wav(fileWordInsight)
display_waveform(fileTest, yTest, srTest)
display_waveform(fileWordAstro, y1, sr1)
display_waveform(fileWordInsight, y2, sr2)
mfccTest = convert_and_preprocess_mfcc(yTest, srTest)
mfcc1 = convert_and_preprocess_mfcc(y1, sr1)
mfcc2 = convert_and_preprocess_mfcc(y2, sr2)
mfcc = [mfcc1, mfcc2]
window_size, dists = get_window_size(mfcc, mfccTest)
get_distances(fileDesiredWord, window_size, dists, mfccTest, mfcc)
get_desired_word_audio(dists, fileDesiredWord)
y, sr = load_wav(fileDesiredWord)
display_waveform(fileDesiredWord, y, sr)
print("- Done identifying. Audio name:  "+fileDesiredWord+" -")


print("\n- Identify 'isu dalaman' word -\n")
fileTest = "harian_metro_isu"
fileWordInsight = "insight_isu_dalaman"
fileWordTV3 = "tv3_isu_dalaman"
fileDesiredWord = "P4 isu_dalaman"
yTest, srTest = load_wav(fileTest)
y1, sr1 = load_wav(fileWordInsight)
y2, sr2 = load_wav(fileWordTV3)
display_waveform(fileTest, yTest, srTest)
display_waveform(fileWordInsight, y1, sr1)
display_waveform(fileWordTV3, y2, sr2)
mfccTest = convert_and_preprocess_mfcc(yTest, srTest)
mfcc1 = convert_and_preprocess_mfcc(y1, sr1)
mfcc2 = convert_and_preprocess_mfcc(y2, sr2)
mfcc = [mfcc1, mfcc2]
window_size, dists = get_window_size(mfcc, mfccTest)
get_distances(fileDesiredWord, window_size, dists, mfccTest, mfcc)
get_desired_word_audio(dists, fileDesiredWord)
y, sr = load_wav(fileDesiredWord)
display_waveform(fileDesiredWord, y, sr)
print("- Done identifying. Audio name:  "+fileDesiredWord+" -")
