from helpers import *
import json
import os

# ==============================================================================================


def generateFingerprintDatabase(songName):
    """
    generateFingerprintDatabase generates the fingerprint of the three components of a song (full,music,vocals) then saves it to the database, generates and saves the spectrogram, mfcc, mel-spectrogram as images.

    :param songName: a string that represents the name of the song
    """
    # initializing the paths of the three components of the song (full,music,vocals) from its name
    path = './songs/'+songName+'/'+songName
    songComponentsPaths = [path+'_Full.mp3',
                           path+'_Music.mp3', path+'_Vocals.mp3']

    mfccHashes, melSpectrogramHashes = [], []

    for i in range(3):
        # creating song object which reads the song by a constructor that takes the path as an argument
        song = Song(songComponentsPaths[i])

        #  generate and save the spectrogram of a song
        song.generateAndSaveSpectrogram()

        # generate the fingerprint of a song ( hashed mel_spectrogram, hashed mfcc )
        songHashes = song.generateFingerprint()

        melSpectrogramHashes.append(songHashes['melSpectrogramHash'])
        mfccHashes.append(songHashes['mfccHash'])

        # save the features as images
        song.saveFeatures()

    # create a unique id to each song from its name
    songId = songName[5:7]+songName[-1]
    # the fingerprint format which will be saved in the json file to each song
    songHashes = {
        'ID': songId,
        'mel-spectrogram': {
            'Full': str(melSpectrogramHashes[0]),
            'Music': str(melSpectrogramHashes[1]),
            'Vocals': str(melSpectrogramHashes[2]),
        },
        'mfcc':
        {
            'Full': str(mfccHashes[0]),
            'Music': str(mfccHashes[1]),
            'Vocals': str(mfccHashes[2]),
        }
    }
    writeFingerprintDatabase(songHashes)

    logger.debug(
        songName + " : hashed fingerprint of the three components of the song (full,music,vocals) has been saved successfully")


# ==============================================================================================


def writeFingerprintDatabase(songHashes):
    """
    writeFingerprintDatabase writes the hashed fingerprint of the song's three components (full,music,vocals) in one line in a json file then inserts a newline.

    :param songHashes: a dictionary that contains hashed fingerprint of the three components of a song
    """
    with open('database.json', 'a') as jsonFile:
        json.dump(songHashes, jsonFile)
        jsonFile.write(os.linesep)


# ==============================================================================================


def readFingerprintDatabase():
    """
    readFingerprintDatabase reads all the hashed fingerprint of all the songs in the database.

    :return: a list of dictionaries that contain the hashed fingerprint of each song
    """

    with open('database.json') as jsonFile:
        songsHash = [json.loads(line) for line in jsonFile]
    return songsHash


# ==============================================================================================
