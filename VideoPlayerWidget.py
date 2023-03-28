import os
import sys
import threading
import time
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QUrl, QSize
from PyQt5.QtGui import QIcon, QMovie, QPixmap
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton,
                             QSlider, QVBoxLayout, QWidget, QFileDialog, QMessageBox)

from PyQt5.QtMultimedia import QVideoFrame
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QWidget, QVBoxLayout
import VideoPlayer
from VideoPlayer import VideoPlayer



# Initialize the application
app = QApplication(sys.argv)


class VideoPlayerWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Set up video player
        self.video_player = VideoPlayer(self)

        # Set up video widget
        self.video_widget = QVideoWidget(self)
        palette = self.video_widget.palette()
        palette.setColor(QPalette.Window, Qt.black)
        self.video_widget.setPalette(palette)
        self.video_widget.setAutoFillBackground(True)

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)

        self.setLayout(layout)

        # Connect signals
        self.video_player.frame_available.connect(self.handle_frame_available)

    def handle_frame_available(self, frame: QVideoFrame):
        self.video_widget.surface().present(frame)

        # Video Widget
        self.video_widget = QVideoWidget(self)
        self.video_player.setVideoOutput(self.video_widget)

        self.fullscreen_button = QPushButton("Fullscreen", self)
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)

        # Controls
        self.play_button = QPushButton(self)
        self.play_button.setIcon(QIcon(os.path.join("icons", "play.png")))
        self.play_button.clicked.connect(self.play_video_thread)

        self.stop_button = QPushButton(self)
        self.stop_button.setIcon(QIcon(os.path.join("icons", "stop.png")))
        self.stop_button.clicked.connect(self.stop_video)

        self.pause_button = QPushButton(self)
        self.pause_button.setIcon(QIcon(os.path.join("icons", "pause.png")))
        self.pause_button.clicked.connect(self.pause_video)

        self.volume_button = QPushButton(self)
        self.volume_button.setIcon(QIcon(os.path.join("icons", "volume.png")))
        self.volume_button.setCheckable(True)
        self.volume_button.clicked.connect(self.toggle_mute)

        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setTickInterval(10)
        self.volume_slider.setSingleStep(1)
        self.volume_slider.valueChanged.connect(self.set_volume)

        self.progress_slider = QSlider(Qt.Horizontal, self)
        self.progress_slider.sliderMoved.connect(self.set_position)
        self.progress_slider.valueChanged.connect(self.set_position)

        # Labels
        self.time_label = QLabel("00:00 / 00:00", self)

        # Layout
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.pause_button)
        control_layout.addWidget(self.stop_button)
        control_layout.addWidget(self.volume_button)
        control_layout.addWidget(self.volume_slider)
        control_layout.addWidget(self.time_label)

        layout = QVBoxLayout(self)
        layout.addWidget(self.video_widget)
        layout.addWidget(self.progress_slider)
        layout.addLayout(control_layout)
        layout.addWidget(self.fullscreen_button)

        # Media Player
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVolume(50)
        self.media_player.positionChanged.connect(self.update_position)
        self.media_player.durationChanged.connect(self.set_duration)

    def open_file(self, file_path):
        if file_path != "":
            self.video_player.set_media(QMediaContent(QUrl.fromLocalFile(file_path)))
            self.play_button.setEnabled(True)

def play_video_thread(self):
    self.play_button.setEnabled(False)
    self.stop_button.setEnabled(True)
    self.pause_button.setEnabled(True)

    self.video_player.play()

    while self.video_player.is_playing:
        time.sleep(0.5)
        position = self.video_player.get_position()
        duration = self.video_player.get_duration()
        self.update_position(position, duration)

    self.play_button.setEnabled(True)
    self.stop_button.setEnabled(False)
    self.pause_button.setEnabled(False)

def stop_video(self):
    self.video_player.stop()

    # Reset the video progress slider
    self.progress_slider.setValue(0)

    # Reset the time label
    self.time_label.setText("00:00 / 00:00")

def set_volume(self, value):
    volume = value / 100.0
    self.media_player.setVolume(value)

def toggle_mute(self):
    if self.media_player.isMuted():
        self.media_player.setMuted(False)
        self.volume_slider.setValue(self.media_player.volume())
    else:
        self.media_player.setMuted(True)
        self.volume_slider.setValue(0)

@pyqtSlot()
def play_video(self):
    if not self.video_player.is_playing:
        self.play_video_thread = threading.Thread(target=self.play_video_thread)
        self.play_video_thread.start()

@pyqtSlot()
def pause_video(self):
    if self.video_player.is_playing:
        self.video_player.pause()

@pyqtSlot()
def toggle_fullscreen(self):
    if self.isFullScreen():
        self.showNormal()
    else:
        self.showFullScreen()

def set_position(self, position):
    self.video_player.set_position(position)
    self.position = position
    duration = self.video_player.get_duration()
    time_str = "{:02d}:{:02d} / {:02d}:{:02d}".format(position // 60000, (position // 1000) % 60,
                                                        duration // 60000, (duration // 1000) % 60)
    self.time_label.setText(time_str)

def update_position(self, position, duration):
    self.position = position
    time_str = "{:02d}:{:02d} / {:02d}:{:02d}".format(position // 60000, (position // 1000) % 60,
                                                        duration // 60000, (duration // 1000) % 60)
    self.time_label.setText(time_str)
    self.progress_slider.setMaximum(duration)
    self.progress_slider.setValue(position)


