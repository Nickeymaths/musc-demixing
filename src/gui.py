from PyQt5.QtWidgets import QMainWindow

from .ui.appgui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QFileDialog
import os


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app
        self.setupUi(self)
        self.addAllEventHandelers()
        self.listSong = ["D:\Downloads\\7 Years - Lukas Graham.mp3", "D:\Downloads\Perfect - Ed Sheeran.mp3"]
        self.currentIndex = 0

        with open("user_data_location.txt") as f:
            self.user_data_folder = f.readlines()[0]
    
    def addAllEventHandelers(self):
        self.spleetBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.spleet))
        self.mixBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.mix))

        self.addBtnSpleet.clicked.connect(self.addSongSpleet)
        self.songListSpleet.clicked.connect(self.showSongSpleet)
        self.downSongSpleet.clicked.connect(self.downSong)
        self.playBtnSpleet.clicked.connect(lambda: self.playSong(0))
        self.prevBtnSpleet.clicked.connect(lambda: self.playSong(-1))
        self.nextBtnSpleet.clicked.connect(lambda: self.playSong(1))
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
        self.addBtnMix.clicked.connect(self.addSongMix)
        self.playBtnMix.clicked.connect(lambda: self.playSong(0))
        self.sliderSongPlayingMix.valueChanged.connect(self.rewindSong)
        self.sliderEleMix.valueChanged.connect(self.adjustVolume)
        self.removeEleBtn.clicked.connect(self.removeEleMix)
        self.exportBtnMix.clicked.connect(self.downSong)
        self.comboBoxListMix.currentTextChanged.connect(self.addEleMix)

    # Thêm bài hát trong page Spleet
    def addSongSpleet(self):
        print("*****")
        mp3_path = "../user_data/foo.mp3"
        self.app.spleetSong(mp3_path, self.user_data_folder)
        self.app.detachLyric(self.user_data_folder, "foo")
        print("Thêm bài hát trong page Spleet")
        hisPath = os.path.join(os.getcwd(), 'data/lib/list.txt')
        fileName = QFileDialog.getOpenFileName(filter="*.wav *.mp3")
        if fileName[0] != "":
            with open(hisPath, 'a+') as f:
                f.seek(0)
                lines = f.read().split("\n")
                if fileName[0] not in lines:
                    f.write(fileName[0] + "\n")

    # Hiện bài hát hiện tại ra giữa màn hình Spleet, cập nhật tên bài hát và tác giả
    # sau khi tách bài hát đấy thành các thành phần
    def showSongSpleet(self, index=0):
        print("*****")
        self.currentSong = index
        print("Hiện bài hát hiện tại ra giữa màn hình Spleet")
        print("Cập nhật tên bài hát")
        self.nameSongPlayingSpleet.setText(self.listSong[index].split("\\")[-1].split(".")[0])

    # Tách bài hát thành các thành phần
    def spleetSong(self, path):
        print("Tách bài hát thành các thành phần")
        """
            input: đường dẫn đến bài hát
            output: void
        """

    # Tạo bài hát hoàn chỉnh từ mảng tham số được truyền vào
    def combineSong(self):
        print("Tạo bài hát hoàn chỉnh từ mảng tham số được truyền vào")
        """
            input: Array: là 1 danh sách các đường dẫn của các thành phần cần nối 
            output: đường dẫn bài hát sau khi nối
        """

    # Phát bài hát được tạo từ mảng tham số được truyền vào
    def playSong(self, index):
        print("*****")
        self.currentIndex += index
        if self.currentIndex < 0:
            self.currentIndex = 0
        elif self.currentIndex >= len(self.listSong):
            self.currentIndex = len(self.listSong) - 1

        nameSong = self.listSong[self.currentIndex].split("\\")[-1].split(".")[0]
        pathSong = "data\lib\\" + nameSong + "\\" + nameSong + ".mp3"
        fullpath = os.path.join(os.getcwd(), pathSong)
        url = QUrl.fromLocalFile(fullpath)
        content = QMediaContent(url)
        self.player = QMediaPlayer()
        self.player.setMedia(content)
        self.player.play()

    # Tải bài hát được tạo từ mảng tham số được truyền vào
    def downSong(self):
        print("*****")
        # self.combineSong()
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

    # Thêm bài hát trong page Mix
    # sau khi tách bài hát thành 5 thành phần
    def addSongMix(self):
        print("*****")
        print("Thêm bài hát trong page Mix")

    # Xóa thành phần được truyền tham số trong danh sách cần mix
    def removeEleMix(self):
        print("*****")
        print("Xóa thành phần được truyền tham số trong danh sách cần mix")

    # Thêm thành phần vào danh sách cần mix
    def addEleMix(self, value):
        if value != "None":
            print("*****")
            print("Thêm thành phần vào danh sách cần mix")