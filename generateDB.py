
from DB_helpers import generateFingerprintDatabase

# ==============================================================================================
for i in range(23):
    if(i == 5 or i == 18 or i == 15):
        continue
    if(i+1) < 10:
        songName = 'Group0'+str(i+1)+'_Song'
    else:
        songName = 'Group'+str(i+1)+'_Song'
    for j in range(4):

        generateFingerprintDatabase(songName+str(j+1))
