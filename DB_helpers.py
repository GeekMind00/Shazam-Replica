import helpers
import json
import os

# ==============================================================================================


def generateFingerprintDatabase(songName):
    path = './songs/'+songName+'/'+songName
    songComponentsPaths = [path+'_full.mp3',
                           path+'_music.mp3', path+'_vocals.mp3']

    mfccHashes, melSpectrogramHashes = [], []

    for i in range(3):

        samplingFreq, audioData = helpers.readAudioFile(
            songComponentsPaths[i])  # read wav file

        helpers.generateSpectrogram(
            songComponentsPaths[i], audioData, samplingFreq)

        melSpectrogram, mfcc = helpers.generateFeatures(
            audioData, samplingFreq)

        melSpectrogramHashes.append(
            helpers.generatePerceptualHash(melSpectrogram))
        mfccHashes.append(helpers.generatePerceptualHash(mfcc))

    songId = songName[5:7]+songName[-1]
    songHashes = {
        'ID': songId,
        'mel-spectrogram': {
            'full': str(melSpectrogramHashes[0]),
            'music': str(melSpectrogramHashes[1]),
            'vocals': str(melSpectrogramHashes[2]),
        },
        'mfcc':
        {
            'full': str(mfccHashes[0]),
            'music': str(mfccHashes[1]),
            'vocals': str(mfccHashes[2]),
        }
    }
    writeFingerprintDatabase(songHashes)


# ==============================================================================================


def writeFingerprintDatabase(songHashes):
    with open('database.json', 'a') as jsonFile:
        json.dump(songHashes, jsonFile)
        jsonFile.write(os.linesep)


# ==============================================================================================


def readFingerprintDatabase():
    with open('database.json') as jsonFile:
        songsHash = [json.loads(line) for line in jsonFile]
    return songsHash


# ==============================================================================================
