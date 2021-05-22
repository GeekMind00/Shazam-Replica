from pydub import AudioSegment
import matplotlib.pyplot as plt
from scipy.io import wavfile
from tempfile import mktemp
import librosa
import numpy as np
import imagehash
from PIL import Image
import json

my_details = {
    'name': 'John Doe',
    'age': 29
}


def readAudioFile(path):
    mp3_audio = AudioSegment.from_file(
        path, format="mp3")  # read mp3
    wname = mktemp('.wav')  # use temporary file
    mp3_audio.export(wname, format="wav", parameters=[
        "-ac", "1"])  # convert to wav  # convert to mono wav instead of stereo
    samplingFreq, audioData = wavfile.read(wname)  # read wav file
    return samplingFreq, audioData


def generateSpectrogram(path, audioData, samplingFreq):
    fig = plt.figure()
    spectro = plt.specgram(audioData, Fs=samplingFreq,
                           NFFT=128, noverlap=0)  # plot
    spectrogamFilePath = path[:-4]  # remove '.mp3' from the path
    fig.savefig(spectrogamFilePath)  # save the spectrogram


def generateFeatures(audioData, samplingFreq):
    mfcc = librosa.feature.mfcc(
        audioData.astype('float64'), sr=samplingFreq)  # generate the mfcc spectral feature
    return mfcc


def generatePerceptualHash(mfcc):
    mfcc = Image.fromarray(mfcc)  # convert the array to a PIL image
    mfccHash = imagehash.phash(mfcc)  # generate perceptual hash
    return mfccHash


def generateFingerprintDatabase(songName):
    path = './songs/'+songName+'/'+songName
    songComponentsPaths = [path+'_full.mp3',
                           path+'_music.mp3', path+'_vocals.mp3']
    mfccHash = []
    for i in range(3):

        samplingFreq, audioData = readAudioFile(
            songComponentsPaths[i])  # read wav file

        generateSpectrogram(songComponentsPaths[i], audioData, samplingFreq)

        mfcc = generateFeatures(audioData, samplingFreq)
        mfccHash.append(generatePerceptualHash(mfcc))
    mfccHash = str(mfccHash)
    songId = songName[5:7]+songName[-1]
    songHashes = {
        'Id': songId,
        'mfcc':
        {
            'full': mfccHash[0],
            'music': mfccHash[1],
            'vocal': mfccHash[2],
        }
    }
    with open('database.json', 'w') as json_file:
        json.dump(songHashes, json_file)


for i in range(4):
    songName = 'Group01_Song'
    generateFingerprintDatabase(songName+str(i+1))
