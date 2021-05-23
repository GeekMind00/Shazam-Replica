from pydub import AudioSegment
import matplotlib.pyplot as plt
from scipy.io import wavfile
from tempfile import mktemp
import librosa
import numpy as np
import imagehash
from PIL import Image
import json
import os
from difflib import SequenceMatcher


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


def generateFeatures(audioData, samplingFreq):  # TODO: ADD MORE FEATURES
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
    songId = songName[5:7]+songName[-1]
    songHashes = {
        'Id': songId,
        'mfcc':
        {
            'full': str(mfccHash[0]),
            'music': str(mfccHash[1]),
            'vocal': str(mfccHash[2]),
        }
    }

    with open('database.json', 'a') as jsonFile:
        json.dump(songHashes, jsonFile)
        jsonFile.write(os.linesep)


def readFingerprintDatabase():
    with open('database.json') as jsonFile:
        songHash = [json.loads(line) for line in jsonFile]
    return songHash


def generateFingerprintUser(songPath):
    mfccHash = []
    samplingFreq, audioData = readAudioFile(songPath)  # read wav file
    generateSpectrogram(songPath, audioData, samplingFreq)
    mfcc = generateFeatures(audioData, samplingFreq)
    mfccHash = str(generatePerceptualHash(mfcc))
    return mfccHash


def parseFingerprintDatabase():  # TODO: needs some improvements
    parsedDatabaseSongHash = {}
    databaseSongHash = readFingerprintDatabase()
    for songs in databaseSongHash:
        for feature in songs:

            if(feature == 'Id'):
                songId = songs[feature]
            else:
                for keyHash in songs[feature]:
                    if(keyHash == 'full'):
                        songName = 'Group' + \
                            songId[0:2]+'_Song'+songId[2]
                        parsedDatabaseSongHash.update(
                            {songName: songs[feature][keyHash]})
                    else:
                        if(keyHash == 'music'):
                            songName = 'Group' + \
                                songId[0:2]+'_Song'+songId[2]
                            parsedDatabaseSongHash.update(
                                {songName: songs[feature][keyHash]})
                        else:
                            if(keyHash == 'vocal'):
                                songName = 'Group' + \
                                    songId[0:2]+'_Song'+songId[2]
                                parsedDatabaseSongHash.update(
                                    {songName: songs[feature][keyHash]})
    return parsedDatabaseSongHash


def compareFingerprint(userSongHash):
    similarityResults = {}
    databaseSongHash = parseFingerprintDatabase()
    for song in databaseSongHash:
        similarityIndex = SequenceMatcher(
            None, userSongHash, databaseSongHash[song]).ratio()
        # if(similarityIndex > 0.2):
        similarityResults.update({song: similarityIndex})
    similarityResults = sorted(
        similarityResults.items(), key=lambda x: x[1], reverse=True)
    return similarityResults


def generateWeightedAverageSong(songPath_1, songPath_2, weight_1, weight_2):
    samplingFreq_1, audioData_1 = readAudioFile(songPath_1)
    samplingFreq_2, audioData_2 = readAudioFile(songPath_2)

    print(samplingFreq_1)
    print(samplingFreq_2)
    weightedAverageSongData = weight_1*audioData_1 + weight_2*audioData_2

    return weightedAverageSongData, samplingFreq_1


def generateFingerprintUserMixing(songPath_1, songPath_2, weight_1, weight_2):
    weightedAverageSongData, samplingFreq = generateWeightedAverageSong(
        songPath_1, songPath_2, weight_1, weight_2)
    mfcc = generateFeatures(weightedAverageSongData, samplingFreq)
    mfccHash = str(generatePerceptualHash(mfcc))
    return mfccHash
