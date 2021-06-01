from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys
import mainWindow
from helpers import *
from DB_helpers import *
from USER_helpers import *

# ==============================================================================================


class ShazamApp(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow):

    def __init__(self):
        super(ShazamApp, self).__init__()
        self.setupUi(self)

    # ==============================================================================================

    def scan(self):
        """
        scan is the main function that generates the fingerprint from the input files then initiates the comparing process then show the ouput in a table in the UI.
        gets called when the user presses 'scan' button.
        """

        self.sliderValue = (self.horizontalSlider.value())
        weight_1 = self.sliderValue / 100
        weight_2 = 1-weight_1
        if(self.scanMode == 'One Song'):
            userSong = Song(self.filePath)
            userSongHashes = userSong.generateFingerprint()
            self.similarityResults = compareFingerprint(userSongHashes)
        elif(self.scanMode == 'Two Songs'):
            songOne = Song(self.filePath[0])
            songTwo = Song(self.filePath[1])
            userWeightedAverageSongHashes = generateFingerprintUserMixing(
                songOne, songTwo, weight_1, weight_2)
            self.similarityResults = compareFingerprint(
                userWeightedAverageSongHashes)
        logger.debug(
            "scan button returned the results successfully")
        self.createTable()

    # ==============================================================================================

    def browseOneFile(self):
        """
        browseFiles saves the file path that the user chose from the UI.
        gets called when the user presses 'Browse a File' button.

        :return: a string that represents thepath to the chosen file by the user
        """

        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        self.filePath, _ = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "ShazamApp",
            "",
            "Audio File (*.mp3)",
            options=options)
        self.scanMode = 'One Song'

        logger.debug(
            "Browse a File button returned the file path successfully")

    # ==============================================================================================

    def browseFiles(self):
        """
        browseFiles saves the file paths that the user chose from the UI.
        gets called when the user presses 'Browse Files' button.

        :return: a list of paths to the chosen files by the user
        """

        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        self.filePath, _ = QtWidgets.QFileDialog.getOpenFileNames(
            None,
            "ShazamApp",
            "",
            "Audio Files (*.mp3)",
            options=options)
        self.scanMode = 'Two Songs'

        logger.debug(
            "Browse Files button returned the file paths successfully")

    # ==============================================================================================

    def createTable(self):
        """
        createTable creates the table in the UI and show the similarity index of each song.

        """
        i = 0
        numResults = len(self.similarityResults)
        # Row count
        self.tableWidget.setRowCount(numResults)

        # Column count
        self.tableWidget.setColumnCount(2)

        self.tableWidget.setItem(0, 0, QTableWidgetItem("Song Name"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("Matching Percentage"))
        for songData in self.similarityResults:
            self.tableWidget.setItem(i, 0, QTableWidgetItem(songData[0]))
            self.tableWidget.setItem(
                i, 1, QTableWidgetItem(str(songData[1])+'%'))
            i = i+1
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)

        logger.debug("Table has been created successfully")


# ==============================================================================================


def main():
    App = QtWidgets.QApplication(sys.argv)
    main = ShazamApp()
    main.show()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()
