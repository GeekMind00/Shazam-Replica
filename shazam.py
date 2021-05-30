from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys
import mainWindow
from helpers import *
from DB_helpers import *
from USER_helpers import *


class ShazamApp(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow):

    def __init__(self):
        super(ShazamApp, self).__init__()
        self.setupUi(self)

    def scan(self):
        self.sliderValue = (self.horizontalSlider.value())
        weight_1 = self.sliderValue / 100
        weight_2 = 1-weight_1
        if(self.scanMode == 'One Song'):
            userSongHashes = generateFingerprintUser(self.filePath)
            self.similarityResults = compareFingerprint(userSongHashes)
        elif(self.scanMode == 'Two Songs'):
            userWeightedAverageSongHashes = generateFingerprintUserMixing(
                self.filePath[0], self.filePath[1], weight_1, weight_2)
            self.similarityResults = compareFingerprint(
                userWeightedAverageSongHashes)
        self.createTable()

    def browseOneFile(self):
        ''' Called when the user presses the Browse button
        '''
        # self.debugPrint( "Browse button pressed" )
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        self.filePath, _ = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "ShazamApp",
            "",
            "Audio File (*.mp3)",
            options=options)
        self.scanMode = 'One Song'

    def browseFiles(self):
        ''' Called when the user presses the Browse button
        '''
        # self.debugPrint( "Browse button pressed" )
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        self.filePath, _ = QtWidgets.QFileDialog.getOpenFileNames(
            None,
            "ShazamApp",
            "",
            "Audio Files (*.mp3)",
            options=options)
        self.scanMode = 'Two Songs'

    def createTable(self):
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


def main():
    App = QtWidgets.QApplication(sys.argv)
    main = ShazamApp()
    main.show()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()
