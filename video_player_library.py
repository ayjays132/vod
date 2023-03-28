import os
import vlc
from selenium import webdriver
import os
import av
import ffmpeg
import moviepy.editor as mp
import pyautogui
import cv2
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as filedialog
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import mimetypes
import vlc
from moviepy import editor as mp
import spacy
import re
import cv2
import random
from tkinter import Frame
import requests
from bs4 import BeautifulSoup
import pafy
import pydub
import numpy as np
from PIL import Image, ImageTk
from io import BytesIO
from urllib.request import urlopen
from tkinter import Button
from tkinter import Tk, filedialog, simpledialog
from tkinter import Tk
from moviepy.editor import VideoFileClip
import video_player_library
import VideoPlayer
from tkinter import *



class VideoPlayer:
    def __init__(self):
        self.video_path = None
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-extensions')
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=options)
        self.instance = vlc.Instance('--no-xlib')
        self.player = self.instance.media_player_new()
        self.playing = False

    def play(self, filepath):
        if self.playing:
            self.stop()
        media = self.instance.media_new(filepath)
        self.player.set_media(media)
        self.player.play()
        self.playing = True

    def pause(self):
        if self.playing:
            self.player.pause()
            self.playing = False

    def stop(self):
        if self.playing:
            self.player.stop()
            self.playing = False

    def set_volume(self, volume):
        self.player.audio_set_volume(volume)

    def mute(self):
        self.player.audio_toggle_mute()

    def get_length(self):
        return self.player.get_length()

    def get_time(self):
        return self.player.get_time()

    def set_time(self, time):
        self.player.set_time(time)

    def get_position(self):
        return self.player.get_position()

    def set_position(self, position):
        self.player.set_position(position)

    def get_state(self):
        return self.player.get_state()

    def get_fps(self):
        return self.player.get_fps()

    def get_width(self):
        return self.player.get_width()

    def get_height(self):
        return self.player.get_height()

    def get_dimensions(self):
        return self.player.video_get_size()

    def is_playing(self):
        return self.playing

    def take_screenshot(self, path, width=None, height=None):
        if width and height:
            vlc_options = f"--no-audio --rate=1 --video-filter=scene --vout=dummy --scene-format=png --scene-prefix=snap --scene-path={path} --scene-width={width} --scene-height={height} --no-snapshot-preview"
        else:
            vlc_options = f"--no-audio --rate=1 --video-filter=scene --vout=dummy --scene-format=png --scene-prefix=snap --scene-path={path} --no-snapshot-preview"
        media = self.instance.media_new(filepath)
        media.get_mrl()
        self.instance.vlm_add_broadcast("snapshot", media, vlc_options, 0, None, True, False)
        self.instance.vlm_play_media("snapshot")

    def set_video_path(self, path):
        self.video_path = path

    def play(self):
        if self.video_path is None:
            raise ValueError("Video path is not set")
        if self.playing:
            self.stop()
        media = self.instance.media_new(self.video_path)
        self.player.set_media(media)
        self.player.play()
        self.playing = True

if __name__ == '__main__':
    player = VideoPlayer()
    filepath = 'test.mp4'
    player.play(filepath)
    input('Press any key to pause...')
    player.pause()
    input('Press any key to resume...')
    player.play(filepath)
    input('Press any key to stop...')
    player.stop()
