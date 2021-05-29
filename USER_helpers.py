from helpers import *


# ==============================================================================================


def generateFingerprintUser(songPath):
    samplingFreq, audioData = readAudioFile(songPath)  # read wav file
    userSongHashes = generateFingerprint(audioData, samplingFreq)
    return userSongHashes


# ==============================================================================================


def generateFingerprintUserMixing(songPath_1, songPath_2, weight_1, weight_2):
    weightedAverageAudioData, samplingFreq = generateWeightedAverageSong(
        songPath_1, songPath_2, weight_1, weight_2)
    userWeightedAverageSongHashes = generateFingerprint(
        weightedAverageAudioData, samplingFreq)
    return userWeightedAverageSongHashes

# ==============================================================================================


def generateWeightedAverageSong(songPath_1, songPath_2, weight_1, weight_2):
    samplingFreq_1, audioData_1 = readAudioFile(songPath_1)
    samplingFreq_2, audioData_2 = readAudioFile(songPath_2)
    weightedAverageSongData = weight_1*audioData_1 + weight_2*audioData_2

    return weightedAverageSongData, samplingFreq_1


# ==============================================================================================
