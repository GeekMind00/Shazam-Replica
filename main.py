from helpers import *
# ================================================
# for i in range(4):
#     songName = 'Group01_Song'
#     generateFingerprintDatabase(songName+str(i+1))

userSongHash = generateFingerprintUser(
    '/Users/mostafaayad/Shazam-clone/songs/Group01_Song1/Group01_Song1_full.mp3')
# similarityResults =
similarityResults = compareFingerprint(userSongHash)

print(similarityResults)
