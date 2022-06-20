from PyQt5.QtWidgets import QMainWindow

from .ui.appgui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QMovie
import os
from .ui import icons_rc
from pathlib import Path
from shutil import copy
import glob

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

        self.speedSongList = [0.5, 1, 1.5, 2]
        self.currentSpeedSongIndex = 1

        self.currentMixSongElement = {
            "vocals": {"path": [], "player": [], "ui": []},
            "bass": {"path": [], "player": [], "ui": []},
            "piano": {"path": [], "player": [], "ui": []},
            "drums": {"path": [], "player": [], "ui": []},
            "other": {"path": [], "player": [], "ui": []},
        }

        with open("user_data_location.txt") as f:
            self.user_data_folder = f.readlines()[0].strip()

        self.hintLabelEmptySongList = QtWidgets.QLabel(self.spleet)
        self.hintLabelEmptySongList.setGeometry(QtCore.QRect(50, 50, 270, 100))
        self.hintLabelEmptySongList.setText("Hãy thêm bài hát")

        self.hintLabelEmptyMixPartSongList = QtWidgets.QLabel(self.mix)
        self.hintLabelEmptyMixPartSongList.setGeometry(QtCore.QRect(50, 50, 270, 100))
        self.hintLabelEmptyMixPartSongList.setText("Hãy thêm bài hát")

        self.labelLoading = QtWidgets.QLabel(self.spleet)
        self.labelLoading.setGeometry(QtCore.QRect(100, 100, 100, 100))
        self.labelLoading.setMovie(QMovie("loading.gif"))
        self.labelLoading.movie().start()
        self.labelLoading.hide()

        self.updateHintEmptyPartSongMixList()
        self.updateListSongFromLib()
        if len(self.listSong) == 0:
            self.currentSongName = ""
        else:
            self.currentSongName = self.listSong[0]
            self.nameSongPlayingSpleet.setText(self.currentSongName)

            # with open(Path(self.user_data_folder, "lib", "7 Years", "song_duration.txt")) as f:
            #     self.maxDurationMix = int(f.readlines()[0].strip())
            #     self.sliderSongPlayingMix.setMaximum(self.maxDurationMix)
            #     self.sliderSongPlayingMix.setMinimum(0)

    def addAllEventHandelers(self):
        self.spleetBtn.clicked.connect(self.routeSpleetScreen)
        self.mixBtn.clicked.connect(self.routeMixScreen)

        self.addBtnSpleet.clicked.connect(self.addSongSpleet)
        self.playBtnSpleet.clicked.connect(self.playOrPauseSong)
        self.prevBtnSpleet.clicked.connect(lambda: self.nextOrPrevSong(-1))
        self.nextBtnSpleet.clicked.connect(lambda: self.nextOrPrevSong(1))
        self.speedBtn.clicked.connect(self.adjustSpeed)
        self.sliderVocalSpleet.valueChanged.connect(lambda:
                                                    self.adjustVolume(self.sliderVocalSpleet.value()
                                                                      , self.elements["vocals"]))
        self.sliderBassSpleet.valueChanged.connect(lambda: self.adjustVolume(self.sliderBassSpleet.value()
                                                                             , self.elements["bass"]))
        self.sliderPianoSpleet.valueChanged.connect(lambda: self.adjustVolume(self.sliderPianoSpleet.value()
                                                                              , self.elements["piano"]))
        self.sliderDrumSpleet.valueChanged.connect(lambda: self.adjustVolume(self.sliderDrumSpleet.value()
                                                                             , self.elements["drums"]))
        self.sliderOtherSpleet.valueChanged.connect(lambda: self.adjustVolume(self.sliderOtherSpleet.value()
                                                                              , self.elements["other"]))
        self.downVocalSpleet.clicked.connect(
            lambda: self.downPartSong(Path(self.user_data_folder, "lib", self.currentSongName, "vocals.mp3")))
        self.downBassSpleet.clicked.connect(
            lambda: self.downPartSong(Path(self.user_data_folder, "lib", self.currentSongName, "bass.mp3")))
        self.downPianoSpleet.clicked.connect(
            lambda: self.downPartSong(Path(self.user_data_folder, "lib", self.currentSongName, "piano.mp3")))
        self.downDrumSpleet.clicked.connect(
            lambda: self.downPartSong(Path(self.user_data_folder, "lib", self.currentSongName, "drums.mp3")))
        self.downOtherSpleet.clicked.connect(
            lambda: self.downPartSong(Path(self.user_data_folder, "lib", self.currentSongName, "other.mp3")))
        self.playBtnMix.clicked.connect(self.playMixSong)
        self.exportBtnMix.clicked.connect(self.exportMixedSong)

        self.sliderSongPlayingMix.valueChanged.connect(self.setPositionMixPlayer)
        self.sliderSongPlayingSpleet.sliderMoved.connect(self.setPositionSpleetPlayer)

    def routeSpleetScreen(self):
        self.stackedWidget.setCurrentWidget(self.spleet)
        self.playBtnMix.setChecked(True)
        for key in self.currentMixSongElement.keys():
            for player in self.currentMixSongElement[key]["player"]:
                player.stop()

    def routeMixScreen(self):
        self.stackedWidget.setCurrentWidget(self.mix)
        self.playBtnSpleet.setChecked(True)
        for key in self.elements.keys():
            self.elements[key].stop()

    def adjustVolume(self, value, player):
        player.setVolume(value)

    def updateListSongFromLib(self):
        libFolder = Path(self.user_data_folder + "/lib")
        if not libFolder.exists():
            libFolder.mkdir(parents=True, exist_ok=True)
        self.listSong = os.listdir(libFolder)
        for i in range(len(self.listSong)):
            eSongBtn, downBtn = self.createElementSongUI(i)
            self.createElementSongEventHanlder(i, eSongBtn, downBtn)

            eMixSongComboList = self.createElementSongMixUI(i)
            self.createElementMixSongEventHanlder(i, eMixSongComboList)

        if len(self.listSong) == 0:
            self.frame.hide()
            self.hintLabelEmptySongList.show()
        else:
            self.frame.show()
            self.hintLabelEmptySongList.hide()

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

    def createElementSongMixUI(self, index):
        frame_39 = QtWidgets.QFrame(self.listMix)
        frame_39.setGeometry(QtCore.QRect(0, index * 45, 140, 42))
        frame_39.setStyleSheet("")
        frame_39.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame_39.setFrameShadow(QtWidgets.QFrame.Raised)
        nameSongListMix = QtWidgets.QLabel(frame_39)
        nameSongListMix.setGeometry(QtCore.QRect(40, 12, 41, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        nameSongListMix.setFont(font)
        songListMix = QtWidgets.QPushButton(frame_39)
        songListMix.setGeometry(QtCore.QRect(0, 0, 140, 41))
        songListMix.setMinimumSize(QtCore.QSize(140, 0))
        songListMix.setMaximumSize(QtCore.QSize(140, 16777215))
        songListMix.setStyleSheet("background-color: transparent;\n"
                                  "border: 1px solid #9C9BBB;\n"
                                  "border-radius: 9;")
        songListMix.setText("")
        label_85 = QtWidgets.QLabel(frame_39)
        label_85.setGeometry(QtCore.QRect(5, 5, 30, 30))
        label_85.setText("")
        label_85.setPixmap(QtGui.QPixmap(":/images/images/music.png"))
        comboBoxListMix = QtWidgets.QComboBox(frame_39)
        comboBoxListMix.setGeometry(QtCore.QRect(85, 10, 55, 22))
        font = QtGui.QFont()
        font.setPointSize(6)
        comboBoxListMix.setFont(font)
        comboBoxListMix.setStyleSheet("border: none;\n"
                                      "background-color: transparent;\n"
                                      "border-radius: 6px;")
        comboBoxListMix.setIconSize(QtCore.QSize(8, 8))
        comboBoxListMix.setItemText(0, "None")
        comboBoxListMix.setItemText(1, "Vocals")
        comboBoxListMix.setItemText(2, "Bass")
        comboBoxListMix.setItemText(3, "Piano")
        comboBoxListMix.setItemText(4, "Drums")
        comboBoxListMix.setItemText(5, "Other")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/icons/hash.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        comboBoxListMix.addItem(icon8, "None")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/images/images/vocal.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        comboBoxListMix.addItem(icon9, "Vocals")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/images/images/bass.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        comboBoxListMix.addItem(icon10, "Bass")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/images/images/piano.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        comboBoxListMix.addItem(icon11, "Piano")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/images/images/drum.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        comboBoxListMix.addItem(icon12, "Drums")
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/images/images/other.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        comboBoxListMix.addItem(icon13, "Other")
        nameSongListMix.setText(self.listSong[index])

        return comboBoxListMix

    def createElementSongMixList(self, part, songName):
        mixMix = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
        mixMix.setGeometry(QtCore.QRect(0, 0, 251, 45))
        mixMix.setFrameShape(QtWidgets.QFrame.StyledPanel)
        mixMix.setFrameShadow(QtWidgets.QFrame.Raised)
        layoutWidget1 = QtWidgets.QWidget(mixMix)
        layoutWidget1.setGeometry(QtCore.QRect(1, 1, 251, 43))
        horizontalLayout_12 = QtWidgets.QHBoxLayout(layoutWidget1)
        horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        frame_51 = QtWidgets.QFrame(layoutWidget1)
        frame_51.setMinimumSize(QtCore.QSize(110, 41))
        frame_51.setMaximumSize(QtCore.QSize(16777215, 41))
        frame_51.setStyleSheet("")
        frame_51.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame_51.setFrameShadow(QtWidgets.QFrame.Raised)
        label_105 = QtWidgets.QLabel(frame_51)
        label_105.setGeometry(QtCore.QRect(5, 0, 47, 41))
        label_105.setText("")
        label_105.setPixmap(QtGui.QPixmap(":/images/images/music.png"))
        nameSongPartEleMix = QtWidgets.QLabel(frame_51)
        nameSongPartEleMix.setGeometry(QtCore.QRect(40, 3, 65, 20))
        nameSongEleMix = QtWidgets.QLabel(frame_51)
        nameSongEleMix.setGeometry(QtCore.QRect(40, 19, 65, 20))
        nameSongEleMix.setStyleSheet("color: #9C9BBB;\n"
                                     "font-size: 10px;")
        horizontalLayout_12.addWidget(frame_51)
        sliderEleMix = QtWidgets.QSlider(layoutWidget1)
        sliderEleMix.setEnabled(True)
        sliderEleMix.setMinimumSize(QtCore.QSize(0, 0))
        sliderEleMix.setMaximumSize(QtCore.QSize(16777215, 16777215))
        sliderEleMix.setTracking(True)
        sliderEleMix.setOrientation(QtCore.Qt.Horizontal)
        sliderEleMix.setMinimum(0)
        sliderEleMix.setMaximum(100)
        sliderEleMix.setValue(100)
        horizontalLayout_12.addWidget(sliderEleMix)
        removeEleBtn = QtWidgets.QPushButton(layoutWidget1)
        removeEleBtn.setMinimumSize(QtCore.QSize(18, 18))
        removeEleBtn.setMaximumSize(QtCore.QSize(18, 18))
        removeEleBtn.setStyleSheet("")
        removeEleBtn.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/icons/minus.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        removeEleBtn.setIcon(icon7)
        removeEleBtn.setIconSize(QtCore.QSize(12, 12))
        horizontalLayout_12.addWidget(removeEleBtn)
        nameSongPartEleMix.setText(part.capitalize())
        nameSongEleMix.setText(songName)
        mixMix.show()

        return sliderEleMix, removeEleBtn, mixMix

    def createElementSongEventHanlder(self, i, eSongBtn, downBtn):
        eSongBtn.clicked.connect(lambda: self.showSongSpleet(i))
        downBtn.clicked.connect(lambda: self.downSong(Path(self.user_data_folder, "lib", self.currentSongName)))

    def createElementMixSongEventHanlder(self, i, eMixSongComboList):
        eMixSongComboList.currentTextChanged.connect(
            lambda: self.addEleMix(eMixSongComboList, self.listSong[i]))

    # Thêm bài hát trong page Spleet
    def addSongSpleet(self):
        fileName = QFileDialog.getOpenFileName(filter="*.wav *.mp3")

        if fileName[0] != "":
            song_name = fileName[0].split("/")[-1].split(".")[0]
            if song_name not in self.listSong:
                # song_folder_in_lib = Path(self.user_data_folder, "lib", song_name)
                # song_folder_in_lib.mkdir(exist_ok=True, parents=True)
                self.labelLoading.show()
                self.app.spleetSong(fileName[0], self.user_data_folder)
                self.app.detachLyric(self.user_data_folder, song_name)
                self.app.export_duration_info(self.user_data_folder, song_name)
                self.updateListSongFromLib()
                self.labelLoading.hide()

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
                    url = QUrl.fromLocalFile(str(Path(songFolder, ePath + ".mp3").resolve()))
                    content = QMediaContent(url)
                    self.elements[ePath].setMedia(content)
                    self.elements[ePath].play()
                    self.playBtnSpleet.setChecked(False)
                elif self.elements[ePath].state() == QMediaPlayer.PlayingState:
                    self.elements[ePath].pause()
                    self.playBtnSpleet.setChecked(True)
                else:
                    self.elements[ePath].play()
                    self.playBtnSpleet.setChecked(False)

                self.elements[ePath].positionChanged.connect(
                    lambda: self.sliderSongPlayingSpleet.setValue(self.elements[ePath].position()))
                self.elements[ePath].durationChanged.connect(
                    lambda: self.sliderSongPlayingSpleet.setRange(0, self.elements[ePath].duration()))

    def playMixSong(self):
        currentPlayState = None

        for key in self.currentMixSongElement.keys():
            for player in self.currentMixSongElement[key]["player"]:
                if not currentPlayState:
                    currentPlayState = player.state()
                if currentPlayState == QMediaPlayer.PlayingState:
                    player.pause()
                    self.playBtnMix.setChecked(True)
                else:
                    player.play()
                    self.playBtnMix.setChecked(False)

    # Reset tất cả bài hát về ban đầu và dừng lại
    def resetMixSong(self):
        for key in self.currentMixSongElement.keys():
            for player in self.currentMixSongElement[key]["player"]:
                player.stop()
        self.sliderSongPlayingMix.setValue(0)
        self.playBtnMix.setChecked(True)

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
                url = QUrl.fromLocalFile(str(Path(songFolder, ePath + ".mp3").resolve()))
                content = QMediaContent(url)
                self.elements[ePath].setMedia(content)
                self.elements[ePath].play()

            self.sliderSongPlayingSpleet.setValue(0)

    # Tải thành phần bài hát
    def downPartSong(self, partSongPath):
        fileName = QFileDialog.getSaveFileName(filter="*.mp3 *.wav")
        if fileName[0] != "":
            output_folder = os.path.dirname(fileName[0])
            new_song_name = os.path.basename(fileName[0]).split(".")[0]

            copy(partSongPath, os.path.join(output_folder, new_song_name+".mp3"))

    # Tải bài hát
    def downSong(self, songPath):
        fileName = QFileDialog.getSaveFileName(filter="*.mp3 *.wav")
        if fileName[0] != "":
            output_folder = os.path.dirname(fileName[0])
            new_song_name = os.path.basename(fileName[0]).split(".")[0]

            input_part_song_path = glob.glob(str(songPath)+"/*.mp3")
            self.app.export_custom_mixing_song(output_folder, input_part_song_path, new_song_name)

    # Tải bài hát được tạo từ mảng tham số được truyền vào
    def exportMixedSong(self):
        fileName = QFileDialog.getSaveFileName(filter="*.mp3 *.wav")
        if fileName[0] != "":
            output_folder = os.path.dirname(fileName[0])
            new_song_name = os.path.basename(fileName[0]).split(".")[0]

            all_song_part_list = []
            for key in self.currentMixSongElement.keys():
                all_song_part_list += self.currentMixSongElement[key]["path"]

            for key in self.currentMixSongElement.keys():
                part_song_path_i = self.currentMixSongElement[key]["path"]
                self.app.export_custom_mixing_song(str(Path(self.user_data_folder, "lib").resolve()), part_song_path_i,
                                                   new_song_name)

            self.app.export_custom_mixing_song(output_folder, all_song_part_list, new_song_name)

    # Điều chỉnh tốc độ bài hát được tạo từ mảng tham số được truyền vào
    def adjustSpeed(self):
        self.currentSpeedSongIndex = (self.currentSpeedSongIndex + 1) % 4
        for key in self.elements:
            self.elements[key].setPlaybackRate(self.speedSongList[self.currentSpeedSongIndex])
        self.speedBtn.setText("x" + format(self.speedSongList[self.currentSpeedSongIndex], ".1f"))

    # Tua bài hát được tạo từ mảng tham số được truyền vào đến vị trí mong muốn
    def setPositionSpleetPlayer(self, position):
        for ePath in self.elements.keys():
            self.elements[ePath].setPosition(position)

    def setPositionMixPlayer(self, position):
        for key in self.currentMixSongElement.keys():
            for player in self.currentMixSongElement[key]["player"]:
                player.setPosition(position)

    # Xóa thành phần được truyền tham số trong danh sách cần mix
    def removeMixSongElement(self, mixMix):
        index = None
        currentKey = None
        for key in self.currentMixSongElement.keys():
            for i, e in enumerate(self.currentMixSongElement[key]["ui"]):
                if id(mixMix) == id(e):
                    currentKey = key
                    index = i

        self.currentMixSongElement[currentKey]["player"][index].positionChanged.disconnect()

        mixMix.deleteLater()
        del self.currentMixSongElement[currentKey]["path"][index]
        del self.currentMixSongElement[currentKey]["player"][index]
        del self.currentMixSongElement[currentKey]["ui"][index]

        self.updateChooseMixE()

        count = 0
        for key in self.currentMixSongElement.keys():
            count += len(self.currentMixSongElement[key]["player"])

        if count == 0:
            self.sliderSongPlayingMix.setValue(0)

        self.updateHintEmptyPartSongMixList()

    def updateHintEmptyPartSongMixList(self):
        count = 0
        for key in self.currentMixSongElement.keys():
            count += len(self.currentMixSongElement[key]["player"])

        if count == 0:
            self.frame_46.hide()
            self.hintLabelEmptyMixPartSongList.show()
            self.playBtnMix.setCheckable(True)
        else:
            self.frame_46.show()
            self.hintLabelEmptyMixPartSongList.hide()

    # Thêm thành phần vào danh sách cần mix
    def addEleMix(self, eMixSongComboList, songName):
        index = eMixSongComboList.currentIndex()
        indexToPartName = {0: "none", 1: "vocals", 2: "bass", 3: "piano", 4: "drums", 5: "other"}

        if index > 0:
            currentPartSong = indexToPartName[index]
            pathToPartSong = Path(self.songNameToPath(songName), currentPartSong + ".mp3")
            self.currentMixSongElement[currentPartSong]["path"].append(pathToPartSong)

            url = QUrl.fromLocalFile(str(pathToPartSong.resolve()))
            content = QMediaContent(url)
            player = QMediaPlayer()
            player.setMedia(content)

            # Thêm tua bài hát
            player.positionChanged.connect(lambda: self.sliderSongPlayingMix.setValue(player.position()))

            self.currentMixSongElement[currentPartSong]["player"].append(player)

            sliderEleMix, removeEleBtn, mixMix = self.createElementSongMixList(currentPartSong, songName)
            self.currentMixSongElement[currentPartSong]["ui"].append(mixMix)
            self.updateChooseMixE()

            sliderEleMix.valueChanged.connect(lambda:
                                              self.adjustVolume(sliderEleMix.value()
                                                                , player))

            removeEleBtn.clicked.connect(lambda: self.removeMixSongElement(mixMix))
            self.resetMixSong()
            eMixSongComboList.setCurrentIndex(0)
            self.updateHintEmptyPartSongMixList()

    def updateDict(self, currentPartSong, pathToPartSong):
        self.currentMixSongElement[currentPartSong]["path"].append(pathToPartSong)

        url = QUrl.fromLocalFile(str(pathToPartSong.resolve()))
        content = QMediaContent(url)
        player = QMediaPlayer()
        player.setMedia(content)
        self.currentMixSongElement[currentPartSong]["player"].append(player)

    def updateChooseMixE(self):
        count = 0
        for i, k in enumerate(self.currentMixSongElement.keys()):
            for j in range(len(self.currentMixSongElement[k]["ui"])):
                self.currentMixSongElement[k]["ui"][j].move(QtCore.QPoint(0, count * 50))
                count += 1

    def songNameToPath(self, songName):
        return Path(self.user_data_folder, "lib", songName)
