from helpers import *
# ================================================
# for i in range(4):
#     songName = 'Group01_Song'
#     generateFingerprintDatabase(songName+str(i+1))

userSongHash = generateFingerprintUser(
    '/Users/mostafaayad/Shazam-clone/songs/Group01_Song1/Group01_Song1_full.mp3')


userWeightedAverageSongHash = generateFingerprintUserMixing('/Users/mostafaayad/Shazam-clone/songs/Group01_Song3/Group01_Song3_full.mp3',
                                                            '/Users/mostafaayad/Shazam-clone/songs/Group01_Song4/Group01_Song4_full.mp3', 1, 0)
similarityResults = compareFingerprint(userWeightedAverageSongHash)

print(similarityResults)
