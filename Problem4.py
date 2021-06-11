import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import copy
from fastdtw import fastdtw
import IPython.display
from scipy.spatial.distance import euclidean
import seaborn as sbn


# Time complexity: O(ab)
def simple_dtw(x, y):
    a, b = len(x), len(y)
    # initialize a matrix with size of series x and y to infinity
    # +1 for later calculation purpose
    dtw_matrix = np.zeros((a+1, b+1))
    for i in range(a+1):  # O(a+1), a = length of series x
        for j in range(b+1):  # O(b+1), b = length of series y
            dtw_matrix[i, j] = np.inf

    # initilize the first element of matrix [0, 0] to 0
    dtw_matrix[0, 0] = 0

    # compute distance matrix
    for i in range(1, a+1):  # O(a), a = length of series x
        for j in range(1, b+1):  # O(b), b = length of series y
            cost = abs(x[i - 1] - y[j - 1])
            # take minimum values among three values,top right,left and bottom
            last_min = np.min([dtw_matrix[i - 1, j], dtw_matrix[i, j - 1], dtw_matrix[i - 1, j - 1]])
            dtw_matrix[i, j] = cost + last_min

    return dtw_matrix


# Time complexity: O(ab)
def display_simple_dtw():
    print("Simple implementation of Dynamic Time Warping (DTW)")
    x = np.array([1, 6, 4, 9, 9, 2, 1, 5, 7, 3])
    y = np.array([1, 7, 2, 3, 3, 9, 4, 8, 6, 3])

    # use fastdtw library to obtain distance and warping path
    distance, path = fastdtw(x, y, dist=euclidean)  # O(w)
    # call simple_dtw method
    array = simple_dtw(x, y)
    # delete first row, first column of distance matrix for displaying warping path purpose
    warp_array = np.delete(np.delete(array, 0, 0), 0, 1)
    # the last element (last row, last column) of the matrix is the distance of the two series
    last_element = array[-1:, -1:]
    # compare distance obtained through simple_dtw and fastdtw library
    print('Distance:', last_element)
    print('Distance from dtw library:', distance)
    print('Warping path:', path)

    # plot dtw cost matrix and warping path
    fig, ax = plt.subplots(figsize=(8, 8))
    ax = sbn.heatmap(warp_array.T, annot=True, square=True, linewidths=0.1, cmap="Pastel1", ax=ax)
    ax.invert_yaxis()
    # get the warp path in x and y directions
    path_x = [p[0] for p in path]
    path_y = [p[1] for p in path]
    # align the path from the center of each cell
    path_xx = [x + 0.5 for x in path_x]
    path_yy = [y + 0.5 for y in path_y]
    ax.plot(path_xx, path_yy, color='blue', linewidth=3, alpha=0.2)
    fig.savefig("P4/dtw_warping_path.png")
    print("Draw warping path: dtw_warping_path.jpg")


# Time complexity: O(1)
def load_wav(name):
    # load .wav audio file to get y: audio time series, and sr: sampling rate of y
    y_value, sr_value = librosa.load('P4/Audio/' + name + '.wav')
    return y_value, sr_value


# Time complexity: O(1)
def display_waveform(name, y_value, sr_value):
    # save waveform of audio into jpg
    plt.figure(figsize=(14, 5))
    librosa.display.waveplot(y=y_value, sr=sr_value)
    plt.savefig('P4/Waveform of ' + name + '.jpg')


# Time complexity: O(c)
def convert_and_preprocess_mfcc(y_value, sr_value):
    # convert data to Mel-frequency cepstral coefficients (MFCCs)
    mfcc_value = librosa.feature.mfcc(y_value, sr_value)
    # remove mean and normalize each column of MFCC
    mfcc_cp = copy.deepcopy(mfcc_value)
    for i in range(mfcc_value.shape[1]):  # O(c), c = no of column of mfcc
        mfcc_cp[:, i] = mfcc_value[:, i] - np.mean(mfcc_value[:, i])
        mfcc_cp[:, i] = mfcc_cp[:, i] / np.max(np.abs(mfcc_cp[:, i]))
    return mfcc_cp


# Time complexity: O(f)
def get_window_size(mfcc_value, mfcc_test_value):
    # compute the average window size of training
    window_size_value = 0
    for i in range(len(mfcc_value)):  # O(f), f = length of mfcc
        window_size_value += mfcc_value[i].shape[1]
    window_size_value = int(window_size_value/len(mfcc_value))
    # find the size of distance window
    dists_value = np.zeros(mfcc_test_value.shape[1] - window_size_value)
    return window_size_value, dists_value


# Time complexity: O(efw)
def get_distances(name, window_size_value, dists_value, mfcc_test_value, mfcc_value):
    # for each ith window,
    for i in range(len(dists_value)):  # O(e), e = length of distance values
        # get the mfccTest with window size = average window size of training
        mfcci = mfcc_test_value[:, i:i + window_size_value]
        # compute distances between mfccTest and mfcc train using fastdtw and the average distance
        for j in range(len(mfcc_value)):  # O(f), f = length of mfcc
            # fastdtw has time complexity of O(w)
            dists_value[i] += fastdtw(mfcc_value[j].T, mfcci.T, dist=lambda x, y: np.exp(np.linalg.norm(x - y, ord=1)))[0]
        dists_value[i] /= len(mfcc_value)
    plt.plot(dists_value)
    plt.savefig('P4/Plotting of ' + name + ' distance.jpg')


# Time complexity: O(1)
def get_desired_word_audio(dists_value, window_size_value, y_test, sr_test, name):
    # get the window with minimum distance (the window with desired word)
    word_match_idx = dists_value.argmin()
    # get the starting and ending index of the window of desired word
    word_match_idx_bnds = np.array([word_match_idx, np.ceil(word_match_idx + window_size_value)])
    samples_per_mfcc = 512
    word_samp_bounds = 1 + (word_match_idx_bnds * samples_per_mfcc)
    # get the boundaries of desired word from test audio series
    # save in .wav file
    word = y_test[int(word_samp_bounds[0]): int(word_samp_bounds[1])]
    audio = IPython.display.Audio(data=word, rate=sr_test)
    with open('P4/Audio/' + name + '.wav', 'wb') as f:
        f.write(audio.data)


# Time complexity: O(efw)
def speech_recognition_method(file_test, file_word_1, file_word_2, file_desired_word):
    y_test, sr_test = load_wav(file_test)  # O(1)
    y1, sr1 = load_wav(file_word_1)
    y2, sr2 = load_wav(file_word_2)
    display_waveform(file_test, y_test, sr_test)  # O(1)
    display_waveform(file_word_1, y1, sr1)
    display_waveform(file_word_2, y2, sr2)
    mfcc_test = convert_and_preprocess_mfcc(y_test, sr_test)  # O(c)
    mfcc1 = convert_and_preprocess_mfcc(y1, sr1)
    mfcc2 = convert_and_preprocess_mfcc(y2, sr2)
    mfcc = [mfcc1, mfcc2]
    window_size, dists = get_window_size(mfcc, mfcc_test)  # O(f)
    get_distances(file_desired_word, window_size, dists, mfcc_test, mfcc)  # O(efw)
    get_desired_word_audio(dists, window_size, y_test, sr_test, file_desired_word)  # O(1)
    y, sr = load_wav(file_desired_word)
    display_waveform(file_desired_word, y, sr)
    print("Done identifying. Audio name:  " + file_desired_word)


# Time complexity: O(efw)
def speech_recognition():
    print("\nImplementation of DTW in speech recognition")
    print("Identify 'kurier J&T ekspres' word")
    file_test = "harian_metro_jnt_ekspres"
    file_word_1 = "astro_kurier_jnt_ekspres"
    file_word_2 = "insight_kurier_jnt_ekspres"
    file_desired_word = "P4 kurier_jnt_ekspres"
    speech_recognition_method(file_test, file_word_1, file_word_2, file_desired_word)  # O(efw)
    print("Identify 'isu dalaman' word")
    file_test = "harian_metro_isu"
    file_word_1 = "insight_isu_dalaman"
    file_word_2 = "tv3_isu_dalaman"
    file_desired_word = "P4 isu_dalaman"
    speech_recognition_method(file_test, file_word_1, file_word_2, file_desired_word)
