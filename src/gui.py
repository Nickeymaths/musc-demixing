from PyQt5.QtWidgets import QMainWindow

from .ui.appgui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QFileDialog
import os
from .ui import icons_rc
from pathlib import Path


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app
        self.setupUi(self)
        self.addAllEventHandelers()

        self.elements = {
            "vocals": QMediaPlayer(),
            "bass": QMediaPlayer(),
            "piano": QMediaPlayer(),
            "drums": QMediaPlayer(),
            "other": QMediaPlayer()
        }

        with open("user_data_location.txt") as f:
            self.user_data_folder = f.readlines()[0].strip()

        self.updateListSongFromLib()
        if len(self.listSong) == 0:
            self.currentSongName = ""
        else:
            self.currentSongName = self.listSong[0]
            self.nameSongPlayingSpleet.setText(self.currentSongName)

    def addAllEventHandelers(self):
        self.spleetBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.spleet))
        self.mixBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.mix))

        self.addBtnSpleet.clicked.connect(self.addSongSpleet)
        self.playBtnSpleet.clicked.connect(self.playOrPauseSong)
        self.prevBtnSpleet.clicked.connect(lambda: self.nextOrPrevSong(-1))
        self.nextBtnSpleet.clicked.connect(lambda: self.nextOrPrevSong(1))
        self.speedBtn.clicked.connect(self.adjustSpeed)
        self.sliderSongPlayingSpleet.valueChanged.connect(self.rewindSong)
        self.sliderVocalSpleet.valueChanged.connect(self.adjustVolume)
        self.sliderBassSpleet.valueChanged.connect(self.adjustVolume)
        self.sliderPianoSpleet.valueChanged.connect(self.adjustVolume)
        self.sliderDrumSpleet.valueChanged.connect(self.adjustVolume)
        self.sliderOtherSpleet.valueChanged.connect(self.adjustVolume)
        self.downVocalSpleet.clicked.connect(self.downSong)
        self.downBassSpleet.clicked.connect(self.downSong)
        self.downPianoSpleet.clicked.connect(self.downSong)
        self.downDrumSpleet.clicked.connect(self.downSong)
        self.downOtherSpleet.clicked.connect(self.downSong)
        self.playBtnMix.clicked.connect(lambda: self.playSong(0))
        self.sliderSongPlayingMix.valueChanged.connect(self.rewindSong)
        self.sliderEleMix.valueChanged.connect(self.adjustVolume)
        self.removeEleBtn.clicked.connect(self.removeEleMix)
        self.exportBtnMix.clicked.connect(self.downSong)
        self.comboBoxListMix.currentTextChanged.connect(self.addEleMix)

    def updateListSongFromLib(self):
        self.listSong = os.listdir(self.user_data_folder + "/lib")
        for i in range(len(self.listSong)):
            eSongBtn, downBtn = self.createElementSongUI(i)
            self.createElementSongEventHanlder(i, eSongBtn, downBtn)

    def createElementSongUI(self, index):
        frame = QtWidgets.QFrame(self.listSpleet)
        frame.setGeometry(QtCore.QRect(0, 45 * index, 150, 41))
        frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame.setFrameShadow(QtWidgets.QFrame.Raised)

        nameSongListSpleet = QtWidgets.QLabel(frame)
        nameSongListSpleet.setGeometry(QtCore.QRect(40, 12, 71, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        nameSongListSpleet.setFont(font)

        songListSpleet = QtWidgets.QPushButton(frame)
        songListSpleet.setGeometry(QtCore.QRect(0, 0, 140, 41))
        songListSpleet.setMinimumSize(QtCore.QSize(140, 0))
        songListSpleet.setMaximumSize(QtCore.QSize(140, 16777215))
        songListSpleet.setStyleSheet("background-color: transparent;\n"
                                     "border: 1px solid #9C9BBB;\n"
                                     "border-radius: 9;")
        songListSpleet.setText("")

        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/download.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        downSongSpleet = QtWidgets.QPushButton(frame)
        downSongSpleet.setGeometry(QtCore.QRect(113, 10, 22, 22))
        downSongSpleet.setStyleSheet("background: transparent;\n"
                                     "border-radius: 11;")
        downSongSpleet.setText("")
        downSongSpleet.setIcon(icon2)
        downSongSpleet.setIconSize(QtCore.QSize(12, 12))

        label = QtWidgets.QLabel(frame)
        label.setGeometry(QtCore.QRect(5, 5, 30, 30))
        label.setText("")
        label.setPixmap(QtGui.QPixmap(":/images/images/music.png"))

        nameSongListSpleet.setText(self.listSong[index])
        frame.show()

        return songListSpleet, downSongSpleet

    def createElementSongEventHanlder(self, i, eSongBtn, downBtn):
        eSongBtn.clicked.connect(lambda: self.showSongSpleet(i))
        downBtn.clicked.connect(self.downSong)

    # Thêm bài hát trong page Spleet
    def addSongSpleet(self):
        fileName = QFileDialog.getOpenFileName(filter="*.wav *.mp3")

        if fileName[0] != "":
            song_name = fileName[0].split("/")[-1].split(".")[0]
            if song_name not in self.listSong:
                # song_folder_in_lib = Path(self.user_data_folder, "lib", song_name)
                # song_folder_in_lib.mkdir(exist_ok=True, parents=True)
                self.app.spleetSong(fileName[0], self.user_data_folder)
                self.app.detachLyric(self.user_data_folder, song_name)
                self.updateListSongFromLib()

    # Cập nhật tên bài hát
    def showSongSpleet(self, index):
        self.currentSongName = self.listSong[index]
        self.nameSongPlayingSpleet.setText(self.currentSongName)

    # Phát hoặc dừng bài hát hiện tại
    def playOrPauseSong(self):
        if self.currentSongName != "":
            songFolder = Path(self.user_data_folder, "lib", self.currentSongName)

            for ePath in self.elements.keys():
                if self.elements[ePath].state() == QMediaPlayer.StoppedState:
                    url = QUrl.fromLocalFile(str(songFolder) + "/" + ePath + ".mp3")
                    content = QMediaContent(url)
                    self.elements[ePath].setMedia(content)
                    self.elements[ePath].play()
                elif self.elements[ePath].state() == QMediaPlayer.PlayingState:
                    self.elements[ePath].pause()
                else:
                    self.elements[ePath].play()

    # Phát bài hát trước hoặc sau
    def nextOrPrevSong(self, index):
        if self.currentSongName != "":
            currentIndex = self.listSong.index(self.currentSongName) + index

            if currentIndex < 0:
                self.currentSongName = self.listSong[0]
            elif currentIndex >= len(self.listSong):
                self.currentSongName = self.listSong[-1]
            else:
                self.currentSongName = self.listSong[currentIndex]

            self.nameSongPlayingSpleet.setText(self.currentSongName)

            songFolder = Path(self.user_data_folder, "lib", self.currentSongName)

            for ePath in self.elements.keys():
                url = QUrl.fromLocalFile(str(songFolder) + "/" + ePath + ".mp3")
                content = QMediaContent(url)
                self.elements[ePath].setMedia(content)
                self.elements[ePath].play()

    # Tải bài hát được tạo từ mảng tham số được truyền vào
    def downSong(self):
        print("*****")
        print("Tải bài hát")

    # Điều chỉnh tốc độ bài hát được tạo từ mảng tham số được truyền vào
    def adjustSpeed(self):
        print("*****")
        """
            input: speed
            output: void
        """
        print("Điều chỉnh tốc độ bài hát")

    # Tua bài hát được tạo từ mảng tham số được truyền vào đến vị trí mong muốn
    def rewindSong(self):
        print("*****")
        print("Tua bài hát đến vị trí mong muốn")

    # Điều chỉnh âm lượng thành phần được truyền làm tham số
    def adjustVolume(self):
        print("*****")
        print("Điều chỉnh âm lượng thành phần được truyền làm tham số")

    # Xóa thành phần được truyền tham số trong danh sách cần mix
    def removeEleMix(self):
        print("*****")
        print("Xóa thành phần được truyền tham số trong danh sách cần mix")

    # Thêm thành phần vào danh sách cần mix
    def addEleMix(self, value):
        if value != "None":
            print("*****")
            print("Thêm thành phần vào danh sách cần mix")
