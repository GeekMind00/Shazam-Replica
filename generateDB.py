
from DB_helpers import generateFingerprintDatabase

# ==============================================================================================
for i in range(4):
    songName = 'Group01_Song'
    generateFingerprintDatabase(songName+str(i+1))
