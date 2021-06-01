from pydub import AudioSegment
import matplotlib.pyplot as plt
from scipy.io import wavfile
from tempfile import mktemp
import librosa
import numpy as np
import imagehash
from PIL import Image
import DB_helpers
import logging
# ==============================================================================================

# config of the logger
logging.basicConfig(filename="Shazam.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()  # Logger maintainer
logger.setLevel(logging.DEBUG)

# ==============================================================================================


class Song:
    """
    A class to represent a song.

    ...

    Attributes
    ----------
    path (essential) : str
        path of the audio file
    audioData (optional) : list
        the sampled data of the audio signal in time domain
    samplingFreq (optional) : int
        the sampling frequency of the audio signal
    melSpectrogramFeatureImage (optional) : PIL image
        the mel-spectrogram feature represented as a PIL image
    mfccFeatureImage (optional) : PIL image
        the mfccm feature represented as a PIL image

    Methods
    -------
    readAudioFile():
        reads an mp3 audio file.
    generateAndSaveSpectrogram():
        generates and saves the spectrogram of a signal.
    generateFeatures():
        generates the spectral features of a signal.
    saveFeatures():
        saves the spectral features of a signal as a PNG image.
    generateFingerprint():
        generates the fingerprint of each song as a hashed mfcc & mel-spectrogram features.
    """

    def __init__(self, path=''):
        """
        Constructs all the necessary attributes for the song object.

        Parameters
        ----------
        path : str
            path of the audio file
        """
        self.path = path
        if(self.path):
            self.samplingFreq, self.audioData = self.readAudioFile()
            logger.debug(self.path+" : audio has been read succesfully")
    # ==============================================================================================

    def readAudioFile(self):
        """
        readAudioFile reads an mp3 audio file.

        :return: data & sampling frequency of the signal
        """

        mp3_audio = AudioSegment.from_file(
            self.path, format="mp3")  # read mp3
        mp3_audio = mp3_audio[:60000]  # take the first 60 sec of the audio
        wname = mktemp('.wav')  # use temporary file
        mp3_audio.export(wname, format="wav", parameters=[
            "-ac", "1"])  # convert to wav  # convert to mono wav instead of stereo
        samplingFreq, audioData = wavfile.read(wname)  # read wav file
        return samplingFreq, audioData
    # ==============================================================================================

    def generateAndSaveSpectrogram(self):
        """
        generateAndSaveSpectrogram generates and saves the spectrogram of a signal.

        """

        fig = plt.figure()  # create a figure
        spectro = plt.specgram(self.audioData, Fs=self.samplingFreq,
                               NFFT=128, noverlap=0)  # plot spectrogram
        spectrogamFilePath = self.path[:-4]  # remove '.mp3' from the path
        fig.savefig(spectrogamFilePath)  # save the spectrogram
        plt.close(fig)

        logger.debug(
            self.path+" : spectrogram has been saved successfully")

    # ==============================================================================================

    def generateFeatures(self):
        """
        generateFeatures generates the spectral features of a signal.

        :return: mfcc & mel-spectrogram features as images
        """

        # generate the mel-spectrogram spectral feature
        melSpectrogram = librosa.feature.melspectrogram(
            self.audioData.astype('float64'), sr=self.samplingFreq)
        # generate the mfcc spectral feature
        mfcc = librosa.feature.mfcc(
            self.audioData.astype('float64'), sr=self.samplingFreq)

        # convert the array of the feature to a PIL image
        self.melSpectrogramFeatureImage = Image.fromarray(
            melSpectrogram, mode='RGB')
        self.mfccFeatureImage = Image.fromarray(mfcc, mode='RGB')

    # ==============================================================================================

    def saveFeatures(self):
        """
        saveFeatures saves the spectral features of a signal as a PNG image.

        """

        # remove '.mp3' from the path and add the corresponding name
        melSpectrogramPath = self.path[:-4] + '_melSpectrogam.png'
        mfccPath = self.path[:-4] + '_mfcc.png'
        self.melSpectrogramFeatureImage.save(melSpectrogramPath)
        self.mfccFeatureImage.save(mfccPath)

        logger.debug(
            self.path+" : features has been saved successfully")

    # ==============================================================================================

    def generateFingerprint(self):
        """
        generateFingerprint generates the fingerprint of each song as a hashed mfcc & mel-spectrogram features.

        :return: a dictionary that contains the hashed features as: key=> name of the feature, value=> hash of the feature
        """

        SongHashes = {}
        self.generateFeatures()
        SongHashes['melSpectrogramHash'] = generatePerceptualHash(
            self.melSpectrogramFeatureImage)
        SongHashes['mfccHash'] = generatePerceptualHash(self.mfccFeatureImage)

        logger.debug(
            self.path+" : fingerprint has been generated successfully")

        return SongHashes


# ==============================================================================================


def generatePerceptualHash(feature):
    """
    generatePerceptualHash computes the perceptual hash of a signal feature represented by an image.

    :param feature: a PIL image that represents a signal feature
    :return: the hashed feature as a string
    """

    featureHash = imagehash.phash(  # generate perceptual hash
        feature, hash_size=16)

    return str(featureHash)


# ==============================================================================================


def getHammingDistance(hashOne, hashTwo):
    """
    getHammingDistance calculates the hamming distance between two strings which represents the differences between them.

    :param hashOne: the first hash represented as a string
    :param hashTwo: the second hash represented as a string
    :return: the hamming distance as an integer
    """
    # convert each string to an imageHash object so we can calculate the hamming distance by substracting one from the other
    return imagehash.hex_to_hash(hashOne)-imagehash.hex_to_hash(hashTwo)


# ==============================================================================================


def mapValue(inputValue: float, inputMin: float, inputMax: float, outputMin: float, outputMax: float):
    """
    mapValue maps a value from a certain range to another.

    :param inputValue: the wannabe mapped value with its current range of inputMin & inputMax
    :param inputMin: minimum range of the input value
    :param inputMax: maximum range of the input value
    :param outputMin: minimum range of the output value
    :param outputMax: maximum range of the output value
    :return: the mapped value within the range of outputMin & outputMax
    """

    slope = (outputMax-outputMin) / (inputMax-inputMin)
    return outputMin + slope*(inputValue-inputMin)


# ==============================================================================================


def compareFingerprint(userSongHashes):
    """
    compareFingerprint compares the hashed fingerprint of a user-given song against the hashed fingerprint of all database songs.

    :param userSongHashes: a dictionary that contains the hash of mfcc & mel-spectrogram features
    :return: a dictionary that contains the result of the comparison process as: key=> name of the song, value=> the similarity index of the two compared songs
    """

    # initialization
    similarityResults = {}
    songComponents = ['Full', 'Music', 'Vocals']

    # fetches the hashes from the database
    databaseSongsHash = DB_helpers.readFingerprintDatabase()

    logger.debug(
        "all the hashes in the database has been retrieved successfully")

    # iterate over the hashes to get a result against each one
    for songHash in databaseSongsHash:

        # generate the song name from the ID that we fetched from the database
        songName = 'Group' + songHash['ID'][0:2]+'_Song'+songHash['ID'][2]

        maxSimilarityIndex = 0

        # iterate over each song component (full,music,vocal)
        for songComponent in songComponents:

            # compute hamming distance of each feature
            melSpectrogramHammingDistance = getHammingDistance(
                songHash['mel-spectrogram'][songComponent], userSongHashes['melSpectrogramHash'])
            mfccHammingDistance = getHammingDistance(
                songHash['mfcc'][songComponent], userSongHashes['mfccHash'])

            # get the average of the differences of the two features
            avgDifference = (melSpectrogramHammingDistance +
                             mfccHammingDistance)/2

            # map the value between 0 => 1 instead of 0 => 256, sso we can represent it better
            mappedAvgDifference = mapValue(avgDifference, 0, 256, 0, 1)

            # calculate the similarity index
            similarityIndex = int((1-mappedAvgDifference)*100)

            # save the results in the dictionary mentioned above
            if(similarityIndex > maxSimilarityIndex):
                similarityResults.update({songName: similarityIndex})
                maxSimilarityIndex = similarityIndex

        logger.debug(
            "similarity index for " + songName + " has been generated successfully")

    # sort the results in a descending order
    similarityResults = sorted(
        similarityResults.items(), key=lambda x: x[1], reverse=True)

    return similarityResults


# ==============================================================================================
