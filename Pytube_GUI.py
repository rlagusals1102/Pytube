import sys
import pytube
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QRadioButton, QFileDialog
from PyQt5.QtCore import QSize
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

class Downloader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setFixedSize(QSize(406, 246))

    def initUI(self):
        self.url = QLineEdit(self)
        self.url.setPlaceholderText("Youtube URL : ")
        self.url.move(100, 50)
        self.url.resize(200, 30)

        self.select_location = QPushButton('Select Save Location', self)
        self.select_location.move(100, 90)
        self.select_location.resize(200, 30)
        self.select_location.clicked.connect(self.get_save_location)

        self.mp4_button = QRadioButton('MP4', self)
        self.mp4_button.move(135, 130)
        self.mp4_button.setChecked(True)

        self.mp3_button = QRadioButton('MP3', self)
        self.mp3_button.move(210, 130)

        self.download = QPushButton('Download', self)
        self.download.move(100, 170)
        self.download.clicked.connect(self.start_download)
        self.download.resize(200, 30)

        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('YouTube Downloader')
        self.show()

    def get_save_location(self):
        self.save_location = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

    def start_download(self):
        video_url = self.url.text()
        yt = pytube.YouTube(video_url)
        if self.mp4_button.isChecked():
            # stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
            # stream.download(self.save_location)
            video = yt.streams.filter(subtype='mp4', progressive=True).order_by('resolution').desc().first()
            video.download(self.save_location)
        else:
            stream = yt.streams.filter(only_audio=True).first()
            stream.download(self.save_location, filename=yt.title + ".mp3")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Downloader()
    sys.exit(app.exec_())
