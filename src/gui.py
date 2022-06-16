from PyQt5.QtWidgets import QMainWindow

from .ui.appgui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app
        self.setupUi(self)
        self.addAllEventHandelers()
    
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
        print("Thêm bài hát trong page Spleet")

    # Hiện bài hát hiện tại ra giữa màn hình Spleet, cập nhật tên bài hát và tác giả
    # sau khi tách bài hát đấy thành các thành phần
    def showSongSpleet(self):
        print("*****")
        self.spleetSong()
        print("Hiện bài hát hiện tại ra giữa màn hình Spleet")
        print("Cập nhật tên bài hát và tác giả")

    # Tách bài hát thành các thành phần
    def spleetSong(self):
        print("Tách bài hát thành các thành phần")

    # Tạo bài hát hoàn chỉnh từ mảng tham số được truyền vào
    def combineSong(self):
        print("Tạo bài hát hoàn chỉnh từ mảng tham số được truyền vào")

    # Phát bài hát được tạo từ mảng tham số được truyền vào
    def playSong(self, index):
        print("*****")
        self.combineSong()
        if index == 0:
            print("Phát bài hát")
        elif index == -1:
            print("Phát bài hát trước")
        else:
            print("Phát bài hát sau")

    # Tải bài hát được tạo từ mảng tham số được truyền vào
    def downSong(self):
        print("*****")
        self.combineSong()
        print("Tải bài hát")

    # Điều chỉnh tốc độ bài hát được tạo từ mảng tham số được truyền vào
    def adjustSpeed(self):
        print("*****")
        self.combineSong()
        print("Điều chỉnh tốc độ bài hát")

    # Tua bài hát được tạo từ mảng tham số được truyền vào đến vị trí mong muốn
    def rewindSong(self):
        print("*****")
        self.combineSong()
        print("Tua bài hát đến vị trí mong muốn")

    # Điều chỉnh âm lượng thành phần được truyền làm tham số
    def adjustVolume(self):
        print("*****")
        print("Điều chỉnh âm lượng thành phần được truyền làm tham số")
        self.combineSong()

    # Thêm bài hát trong page Lyric
    def addSongLyric(self):
        print("*****")
        print("Thêm bài hát trong page Lyric")

    # Hiện bài hát hiện tại ra giữa màn hình Lyric
    # sau khi đã tách lyric bài hát
    def showSongLyric(self):
        print("*****")
        self.detachLyric()
        print("Hiện bài hát hiện tại ra giữa màn hình Lyric")
        print("Cập nhật tên bài hát và tác giả")

    # Tách lời bài hát
    def detachLyric(self):
        print("Tách lời bài hát")

    # Thêm bài hát trong page Mix
    # sau khi tách bài hát thành 5 thành phần
    def addSongMix(self):
        print("*****")
        self.spleetSong()
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