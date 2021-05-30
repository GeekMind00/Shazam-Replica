from pydub import AudioSegment
import matplotlib.pyplot as plt
from scipy.io import wavfile
from tempfile import mktemp
import librosa
import numpy as np
import imagehash
from PIL import Image
from DB_helpers import readFingerprintDatabase


# ==============================================================================================


def readAudioFile(path):
    mp3_audio = AudioSegment.from_file(
        path, format="mp3")  # read mp3
    mp3_audio = mp3_audio[:60000]  # take the first 60 sec of the audio
    wname = mktemp('.wav')  # use temporary file
    mp3_audio.export(wname, format="wav", parameters=[
        "-ac", "1"])  # convert to wav  # convert to mono wav instead of stereo
    samplingFreq, audioData = wavfile.read(wname)  # read wav file
    return samplingFreq, audioData


# ==============================================================================================


def generateSpectrogram(path, audioData, samplingFreq):
    fig = plt.figure()
    spectro = plt.specgram(audioData, Fs=samplingFreq,
                           NFFT=128, noverlap=0)  # plot
    spectrogamFilePath = path[:-4]  # remove '.mp3' from the path
    fig.savefig(spectrogamFilePath)  # save the spectrogram


# ==============================================================================================


def generateFeatures(audioData, samplingFreq):  # TODO: ADD MORE FEATURES
    melSpectrogram = librosa.feature.melspectrogram(
        audioData.astype('float64'), sr=samplingFreq)
    # generate the mfcc spectral feature
    mfcc = librosa.feature.mfcc(audioData.astype('float64'), sr=samplingFreq)
    return melSpectrogram, mfcc


# ==============================================================================================


def generatePerceptualHash(feature):
    feature = Image.fromarray(feature)  # convert the array to a PIL image
    featureHash = imagehash.phash(
        feature, hash_size=16)  # generate perceptual hash
    return featureHash


# ==============================================================================================


def generateFingerprint(audioData, samplingFreq):
    SongHashes = {}
    melSpectrogram, mfcc = generateFeatures(audioData, samplingFreq)
    SongHashes['mfccHash'] = str(generatePerceptualHash(mfcc))
    SongHashes['melSpectrogramHash'] = str(
        generatePerceptualHash(melSpectrogram))
    return SongHashes


# ==============================================================================================


def getHammingDistance(hashOne, hashTwo):
    return imagehash.hex_to_hash(hashOne)-imagehash.hex_to_hash(hashTwo)


# ==============================================================================================


def mapValue(inputValue: float, inputMin: float, inputMax: float, outputMin: float, outputMax: float):
    slope = (outputMax-outputMin) / (inputMax-inputMin)
    return outputMin + slope*(inputValue-inputMin)


# ==============================================================================================


def compareFingerprint(userSongHashes):
    similarityResults = {}
    songComponents = ['full', 'music', 'vocals']

    databaseSongsHash = readFingerprintDatabase()

    for songHash in databaseSongsHash:
        songName = 'Group' + songHash['ID'][0:2]+'_Song'+songHash['ID'][2]
        for songComponent in songComponents:
            melSpectrogramHammingDistance = getHammingDistance(
                songHash['mel-spectrogram'][songComponent], userSongHashes['melSpectrogramHash'])
            mfccHammingDistance = getHammingDistance(
                songHash['mfcc'][songComponent], userSongHashes['mfccHash'])

            avgDifference = (melSpectrogramHammingDistance +
                             mfccHammingDistance)/2

            mappedAvgDifference = mapValue(avgDifference, 0, 256, 0, 1)
            similarityIndex = int((1-mappedAvgDifference)*100)
            similarityResults.update({songName: similarityIndex})

    similarityResults = sorted(
        similarityResults.items(), key=lambda x: x[1], reverse=True)
    return similarityResults


# ==============================================================================================
