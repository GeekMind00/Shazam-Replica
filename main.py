from helpers import *
from DB_helpers import *
from USER_helpers import *
# # ==============================================================================================
# for i in range(4):
#     songName = 'Group01_Song'
#     generateFingerprintDatabase(songName+str(i+1))

# ==============================================================================================
userSongHashes = generateFingerprintUser(
    '/Users/mostafaayad/Shazam-clone/songs/Group01_Song1/Group01_Song1_full.mp3')
# ==============================================================================================
userWeightedAverageSongHashes = generateFingerprintUserMixing(
    '/Users/mostafaayad/Shazam-clone/songs/Group01_Song3/Group01_Song3_full.mp3', '/Users/mostafaayad/Shazam-clone/songs/Group01_Song4/Group01_Song4_full.mp3', 0.5, 0.5)
# ==============================================================================================
similarityResultsOne = compareFingerprint(userSongHashes)
similarityResultsTwo = compareFingerprint(userWeightedAverageSongHashes)
print('Test of one song:')
print(similarityResultsOne)
print('==========================================')
print('Test of two songs:')
print(similarityResultsTwo)
