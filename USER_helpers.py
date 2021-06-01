from helpers import *


# ==============================================================================================


def generateFingerprintUserMixing(songOne, songTwo, weightOne, weightTwo):
    """
    generateFingerprintUserMixing generates the fingerprint of a weighted average song.

    :param songOne: the first song chosen by the user represented as a Song object 
    :param songTwo: the second song chosen by the user represented as a Song object 
    :param weightOne: the weight of the first song represented as an integer
    :param weightTwo: the weight of the second song represented as an integer
    :return: a dictionary that contains the hashed fingerprint of a weighted average song
    """

    weightedAverageSong = Song()
    weightedAverageSong.audioData, weightedAverageSong.samplingFreq = generateWeightedAverageSong(
        songOne, songTwo, weightOne, weightTwo)

    userWeightedAverageSongHashes = weightedAverageSong.generateFingerprint()

    logger.debug(
        "fingerprint of the weighted average song has been generated successfully")

    return userWeightedAverageSongHashes

# ==============================================================================================


def generateWeightedAverageSong(songOne, songTwo, weightOne, weightTwo):
    """
    generateWeightedAverageSong sums two audio signals in time domain.

    :param songOne: the first song chosen by the user represented as a Song object 
    :param songTwo: the second song chosen by the user represented as a Song object 
    :param weightOne: the weight of the first song represented as an integer
    :param weightTwo: the weight of the second song represented as an integer
    :return: data and sampling frequency of the created weighted average song
    """

    weightedAverageSongData = weightOne * \
        songOne.audioData + weightTwo*songTwo.audioData

    logger.debug(
        songOne.path + ", " + songTwo.path + " : has been mixed successfully")

    return weightedAverageSongData, songOne.samplingFreq


# ==============================================================================================
