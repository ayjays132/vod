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







SUPPORTED_FILE_EXTENSIONS = {".mp4", ".mkv", ".avi", ".flv", ".wmv", ".mov"}

root = tk.Tk()

root.withdraw()

class VideoPlayerWidget(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        # Create a frame to hold the video player widget
        self.video_frame = ttk.Frame(self)
        self.video_frame.pack()

        # Create a button to open a file dialog and choose a video file
        self.open_button = ttk.Button(self, text="Open", command=self.open_file)
        self.open_button.pack()

        # Create a button to play or pause the video
        self.play_button = ttk.Button(self, text="Play", command=self.play_pause)
        self.play_button.pack()

        # Create a progress bar to show the playback progress
        self.progress_bar = ttk.Progressbar(self, orient='horizontal', length=200, mode='determinate')
        self.progress_bar.pack()

        # Create a volume control slider
        self.volume_slider = ttk.Scale(self, from_=0, to=100, orient='horizontal', command=self.set_volume)
        self.volume_slider.pack()

        self.parent = parent

        # Set the initial volume level
        self.volume = self.player.audio_get_volume()

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            media = self.instance.media_new(file_path)
            self.player.set_media(media)
            self.play_button.config(text="Play")

    def play_pause(self):
        if self.player.get_state() == vlc.State.Playing:
            self.player.pause()
            self.play_button.config(text="Play")
        else:
            self.player.play()
            self.play_button.config(text="Pause")

    def set_volume(self, volume):
        self.player.audio_set_volume(int(volume))




        

        self.init_ui()

    def init_ui(self):
        # create a frame for the video player
        video_frame = tk.Frame(self.master)
        video_frame.pack(side=tk.TOP)

        # create the video player
        self.video_player = VideoElement(video_frame)

        # create a frame for the playback controls
        controls_frame = tk.Frame(self.master)
        controls_frame.pack(side=tk.TOP, padx=10, pady=10)

        # create the playback controls
        self.create_play_button(controls_frame)
        self.create_stop_button(controls_frame)
        self.create_progress_bar(controls_frame)
        self.create_current_time_label(controls_frame)
        self.create_duration_label(controls_frame)
        self.create_playback_speed_menu(controls_frame)
        self.create_thumbnail_widget(controls_frame)

    def create_play_button(self, parent):
        button = tk.Button(parent, text='Play', command=self.play)
        button.pack(side=tk.LEFT)

    def create_stop_button(self, parent):
        button = tk.Button(parent, text='Stop', command=self.stop)
        button.pack(side=tk.LEFT, padx=10)

    def create_progress_bar(self, parent):
        self.progressbar = tk.Scale(parent, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_position)
        self.progressbar.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def create_current_time_label(self, parent):
        self.current_time_label = tk.Label(parent, text='00:00')
        self.current_time_label.pack(side=tk.LEFT, padx=10)

    def create_duration_label(self, parent):
        self.duration_label = tk.Label(parent, text='00:00')
        self.duration_label.pack(side=tk.LEFT, padx=10)

    def create_playback_speed_menu(self, parent):
        self.playback_speed_var = tk.StringVar()
        self.playback_speed_var.set('1.0x')
        menu = tk.OptionMenu(parent, self.playback_speed_var, '0.5x', '1.0x', '1.5x', '2.0x', command=self.set_playback_speed)
        menu.pack(side=tk.LEFT, padx=10)

    def create_thumbnail_widget(self, parent):
        self.thumbnail_widget = tk.Label(parent)
        self.thumbnail_widget.pack(side=tk.RIGHT)





    def stop(self):
        # stop the video playback
        self.player.stop()

    def set_position(self, value):
        # set the playback position of the video
        self.player.set_position(float(value) / 100)

    def update_progress(self):
        # update the progress bar with the current playback position
        if self.player.is_playing():
            position = self.player.get_position()
            self.progress_bar.set(int(position * 100))
        self.after(100, self.update_progress)


def update_ui(self):
    # update the current time label
    current_time = self.video_player.get_time() / 1000
    current_time_str = format_time(current_time)
    self.current_time_label.config(text=current_time_str)

    # update the progress bar position
    progress = current_time / self.duration * 100
    self.progressbar.set(current_time)

    # update the thumbnail image
    thumbnail_index = int(current_time * THUMBNAIL_FRAMES_PER_SECOND)
    if thumbnail_index < len(self.thumbnail_images):
        thumbnail_image = self.thumbnail_images[thumbnail_index]
        self.thumbnail_widget.config(image=thumbnail_image)
        self.thumbnail_widget.image = thumbnail_image  # keep a reference to prevent garbage collection

    # update the duration label
    duration_str = format_time(self.duration)
    self.duration_label.config(text=duration_str)

    # update the playback speed menu
    self.playback_speed_var.set(f'{self.playback_speed}x')

    # schedule the next update
    if self.is_playing:
        self.after(1000 // VIDEO_FRAME_RATE, self.update_ui)

def on_seek(self, value):
    # seek to the specified time in the video
    time_in_seconds = float(value)
    time_in_milliseconds = int(time_in_seconds * 1000)
    self.video_player.set_time(time_in_milliseconds)
    
def on_play_pause(self):
    # toggle the play/pause state of the video player
    if self.is_playing:
        self.video_player.pause()
        self.is_playing = False
        self.play_button.config(text='Play')
    else:
        self.video_player.play()
        self.is_playing = True
        self.play_button.config(text='Pause')
        self.update_ui()
    
def on_mute_unmute(self):
    # toggle the mute/unmute state of the video player
    if self.is_muted:
        self.video_player.audio_toggle_mute()
        self.is_muted = False
        self.mute_button.config(text='Mute')
    else:
        self.video_player.audio_toggle_mute()
        self.is_muted = True
        self.mute_button.config(text='Unmute')
        
def on_volume_change(self, value):
    # set the volume of the video player
    volume = int(value)
    self.video_player.audio_set_volume(volume)
    
def on_playback_speed_change(self, value):
    # set the playback speed of the video player
    speed_str = self.playback_speed_var.get()
    speed = float(speed_str[:-1])
    self.playback_speed = speed
    self.video_player.set_rate(speed)
    
def on_hover(self, event):
    # show the controls when hovering over the video player
    self.progressbar.pack_forget()
    self.current_time_label.pack_forget()
    self.duration_label.pack_forget()
    self.play_button.pack_forget()
    self.mute_button.pack_forget()
    self.volume_slider.pack_forget()
    self.playback_speed_menu.pack_forget()
    
    self.progressbar.pack(fill='x')
    self.current_time_label.pack(side='left')
    self.duration_label.pack(side='right')
    self.play_button.pack(side='left')
    self.mute_button.pack(side='right')
    self.volume_slider.pack(side='right')
    self.playback_speed_menu.pack(side='right')
    
def on_leave(self, event):
    # hide the controls when leaving the video player
    self.progressbar.pack_forget()
    self.current_time_label.pack_forget()
    self.duration_label.pack_forget()
    self.play_button.pack_forget()
    self.mute_button.pack_forget()
    self.volume_slider.pack_forget()
    self.playback_speed_menu.pack_forget()



def generate_thumbnail(file_path, width=320):
    # Load video and get its width and height
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        raise ValueError("Could not open video file")
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    
    # Calculate new height based on the desired thumbnail width
    new_height = int(width / height * width)
    
    # Create a blank thumbnail image with the desired size
    thumbnail = np.zeros((new_height, width, 3), np.uint8)
    
    # Read first frame from video
    ret, frame = cap.read()
    
    # Loop through video frames and add them to the thumbnail image
    while ret:
        # Resize frame to match thumbnail aspect ratio and add to thumbnail image
        thumbnail_frame = cv2.resize(frame, (width, new_height))
        thumbnail[0:new_height, :] = thumbnail_frame
        
        # Read next frame from video
        ret, frame = cap.read()
    
    # Release video capture object
    cap.release()
    
    # Return thumbnail image
    return thumbnail

            

def open_file(self):
    file_path = filedialog.askopenfilename()
    if file_path:
        media = self.instance.media_new(file_path)
        self.player.set_media(media)
        self.player.set_hwnd(self.video_frame.winfo_id())

def play_pause(self):
    if self.player.get_state() == vlc.State.Ended:
        self.player.stop()
    elif self.player.get_state() == vlc.State.Playing:
        self.player.pause()
        self.play_button.config(text="Play")
    else:
        self.player.play()
        self.play_button.config(text="Pause")
        self.update_progress()

def update_progress(self):
    """Updates the progress bar to show the playback progress"""
    current_time = self.player.get_time() / 1000
    total_time = self.player.get_length() / 1000
    progress = (current_time / total_time) * 100
    self.progress_bar['value'] = progress
    if self.player.get_state() == vlc.State.Playing:
        self.after(1000, self.update_progress)

def set_volume(self, volume):
    # Update the volume of the player
    self.player.audio_set_volume(float(volume))
    # Update the volume attribute
    self.volume = float(volume)
        
def update(self):
    # ...

    # Update the volume scale widget
    if self.player.audio_get_volume() != self.volume:
        self.volume_scale.set(self.player.audio_get_volume())
        self.volume = self.player.audio_get_volume()


def edit_video(input_path, output_path):
    # Get the video file extension
    file_extension = os.path.splitext(input_path)[1].lower()

    # Use PyAV for decoding and encoding if the file is in a supported format
    if file_extension in ['.mp4', '.avi', '.mov', '.wmv', '.webm', '.mkv']:
        # Open the input video file
        input_video = pyav.open(input_path)

        # Get the video stream and video codec
        video_stream = next(s for s in input_video.streams if s.type == 'video')
        video_codec = video_stream.codec_context.codec.name

        # Get the video resolution
        width, height = video_stream.width, video_stream.height

        # Check if the video has an 8K resolution
        if width >= 7680 and height >= 4320:
            # Use FFmpeg to decode the video stream
            input_stream = ffmpeg.input(input_path)
            video = input_stream.video

            # Use FFmpeg to edit and process the video file
            (
                ffmpeg
                .output(video, output_path)
                .run(capture_stdout=True)
            )
        else:
            # Use PyAV to decode the video stream
            decoder = pyav.CodecContext.create_decoder(video_codec)

            # Use MoviePy to edit and process the video file
            video_clip = mp.VideoFileClip(input_path)
            edited_video = video_clip.resize((1920, 1080))
            edited_video.write_videofile(output_path, codec='libx264', fps=video_clip.fps)

    else:
        print(f"The video format {file_extension} is not supported.")

# Define available speeds
speeds = [1, 2, 4, 8]

# Initialize default speed index
current_speed_index = 0


def play_video(self):
    # Create a media object for the selected video file
    media = self.instance.media_new(self.video_path)

    # Set the media to be played by the player
    self.player.set_media(media)

    # Set the volume level
    self.player.audio_set_volume(int(self.volume_slider.get()))

    # Start playing the video
    self.player.play()

    # Set the maximum value of the progress bar to the duration of the video
    self.progress_bar['maximum'] = int(self.player.get_length() / 1000)

    # Start updating the progress bar every second
    self.update_progress()

def update_progress(self):
    # Update the value of the progress bar to the current time of the video
    self.progress_bar['value'] = int(self.player.get_time() / 1000)

    # Update the current time label
    current_time = int(self.player.get_time() / 1000)
    current_time_str = time.strftime('%M:%S', time.gmtime(current_time))
    self.current_time_label.config(text=current_time_str)

    # Update the duration label
    duration = int(self.player.get_length() / 1000)
    duration_str = time.strftime('%M:%S', time.gmtime(duration))
    self.duration_label.config(text=duration_str)

    # Schedule the next update in 1 second
    self.after(1000, self.update_progress)




def toggle_speed():
    global current_speed_index, speeds, cap
    current_speed_index = (current_speed_index + 1) % len(speeds)
    cap.set(cv2.CAP_PROP_FPS, speeds[current_speed_index])
    print(f"Current speed: {speeds[current_speed_index]}x")


def seek_backward():
    global video_player, current_speed_index, speeds, seek_interval
    
    # Get the current playback speed
    current_speed = speeds[current_speed_index]

    # Calculate the new time to seek to
    new_time = video_player.get_time() - (current_speed * seek_interval)

    # Check if the new time is less than 0
    if new_time < 0:
        new_time = 0

    # Seek to the new time
    video_player.set_time(new_time)

def seek_forward():
    global video_player, current_speed_index, speeds, seek_interval
    
    # Get the current playback speed
    current_speed = speeds[current_speed_index]

    # Calculate the new time to seek to
    new_time = video_player.get_time() + (current_speed * seek_interval)

    # Check if the new time is greater than the video duration
    if new_time > video_player.get_length():
        new_time = video_player.get_length()

    # Seek to the new time
    video_player.set_time(new_time)

# initialize video capture object
cap = cv2.VideoCapture('video.mp4')

# get total number of frames in video
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# get video frame rate
fps = int(cap.get(cv2.CAP_PROP_FPS))

# define duration of each thumbnail (in seconds)
thumbnail_duration = 2

# initialize variables
current_frame = 0
last_thumbnail_time = 0

# loop through video frames
while True:
    # read next frame
    ret, frame = cap.read()

    # break loop if end of video is reached
    if not ret:
        break

    # get current time (in seconds)
    current_time = current_frame / fps

    # check if enough time has elapsed since last thumbnail was generated
    if current_time - last_thumbnail_time >= thumbnail_duration:
        # generate thumbnail of current frame
        thumbnail = cv2.resize(frame, (320, 180))

        # save thumbnail as image file
        filename = f'thumbnail_{current_frame}.jpg'
        cv2.imwrite(filename, thumbnail)

        # update last thumbnail time
        last_thumbnail_time = current_time

    # update current frame
    current_frame += 1

    # do something with the current frame (e.g. display in video player)
    # ...

    # wait for user input (e.g. fast forward in timeline bar)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# release video capture object
cap.release()

def theater_mode():
    # get the video player element
    video_player = driver.find_element_by_tag_name('video')
    47
    # hide all elements except video player
    driver.execute_script("var elements = document.body.getElementsByTagName('*'); \
                          for (var i = 0; i < elements.length; i++) { \
                            if (elements[i] != arguments[0]) { \
                              elements[i].style.display = 'none'; \
                            } \
                          }", video_player)
    
    # set the video player to be the size of the window
    driver.execute_script("arguments[0].style.position='fixed'; \
                          arguments[0].style.top='0'; \
                          arguments[0].style.left='0'; \
                          arguments[0].style.width='100%'; \
                          arguments[0].style.height='100%'; \
                          arguments[0].style.zIndex='999999';", video_player)


def video_pop_out():
    # get the video player element
    video_player = driver.find_element_by_tag_name('video')

    # create a new window with the video player
    new_window = webdriver.Chrome()
    new_window.get(driver.current_url)
    new_window.set_window_size(video_player.size['width'], video_player.size['height'])
    new_window.execute_script("window.scrollTo(0,arguments[0].getBoundingClientRect().top)", video_player)
    new_window.execute_script("arguments[0].style.position='fixed'; \
                              arguments[0].style.top='0'; \
                              arguments[0].style.left='0'; \
                              arguments[0].style.width='100%'; \
                              arguments[0].style.height='100%'; \
                              arguments[0].style.zIndex='999999';", video_player)
    new_window.switch_to.window(new_window.window_handles[0])
    driver.switch_to.window(driver.window_handles[0])


# create video player instance
video_player = video_player_library.VideoPlayer()

def set_volume(volume):
    global video_player, current_speed_index, speed_options

    # ensure volume is within 0-100 range
    volume = max(0, min(volume, 100))

    # set volume of video player
    video_player.set_volume(volume)

# define the browser names and corresponding drivers
browser_drivers = {
    'chrome': webdriver.Chrome,
    'firefox': webdriver.Firefox,
    'edge': webdriver.Edge,
    'safari': webdriver.Safari,
    'opera': webdriver.Opera,
    'ie': webdriver.Ie,
    'chromium': lambda: webdriver.Chrome(options=Options().add_argument('--disable-gpu')),
    'brave': lambda: webdriver.Chrome(options=Options().add_argument('--disable-gpu')),
    'vivaldi': lambda: webdriver.Chrome(options=Options().add_argument('--disable-gpu')),
}

# prompt user to enter the browser name
browser_name = input("Enter browser name: ").lower()

# check if the entered browser name is valid
if browser_name in browser_drivers:
    # initialize the corresponding driver for the specified browser
    driver = browser_drivers[browser_name]()
else:
    print('Invalid browser name')

# navigate to the webpage with the video player
driver.get('https://www.example.com')

# search for the video player element
player = driver.find_element_by_xpath('//video')



# pop out the video player
driver.execute_script('window.open(arguments[0], "_blank", "height=480,width=640")',)

# enter theater mode
ActionChains(driver).move_to_element(player).send_keys(Keys.F11).perform()


def fullscreen_mode():
    # Press the F11 key to toggle fullscreen mode
    pyautogui.press('f11')


def set_subtitles(subtitles, input_path, output_path):
    # Get the video file extension
    file_extension = os.path.splitext(input_path)[1].lower()

    # Use FFmpeg to add subtitles if the file is in a supported format
    if file_extension in ['.mp4', '.avi', '.mov', '.wmv', '.webm', '.mkv']:
        # Use FFmpeg to add the subtitles to the video file
        (
            ffmpeg
            .input(input_path)
            .output(output_path, vcodec="copy", acodec="copy", s=subtitles)
            .run(capture_stdout=True)
        )
    else:
        print(f"The video format {file_extension} is not supported.")


def set_speed(speed):
    # Get the currently selected source element
    selected_source = document.querySelector('video source[selected]')

    # Get the parent video element
    video = selected_source.parentNode

    # Set the playback speed
    video.playbackRate = speed


def set_quality(quality):
    # Get the video file extension
    file_extension = os.path.splitext(input_path)[1].lower()

    # Use PyAV for decoding and encoding if the file is in a supported format
    if file_extension in ['.mp4', '.avi', '.mov', '.wmv', '.webm', '.mkv']:
        # Open the input video file
        input_video = pyav.open(input_path)

        # Get the video stream and video codec
        video_stream = next(s for s in input_video.streams if s.type == 'video')
        video_codec = video_stream.codec_context.codec.name

        # Get the video resolution
        width, height = video_stream.width, video_stream.height

        # Check if the video has an 8K resolution
        if width >= 7680 and height >= 4320:
            # Use FFmpeg to decode the video stream
            input_stream = ffmpeg.input(input_path)
            video = input_stream.video

            # Use FFmpeg to edit and process the video file
            output_video = (
                ffmpeg
                .output(video, output_path, **{'vf': f"scale={quality}"})
                .run(capture_stdout=True)
            )
        else:
            # Use PyAV to decode the video stream
            video_container = pyav.open(input_path)
            video_stream = next(s for s in video_container.streams if s.type == 'video')
            decoder = video_stream.codec_context.create_decoder(video_codec)

            # Use MoviePy to edit and process the video file
            video_clip = mp.VideoFileClip(input_path)
            edited_video = video_clip.resize((1920, 1080))
            edited_video.write_videofile(output_path)

    else:
        print(f"The video format {file_extension} is not supported.")

current_playlist = []

def set_playlist(playlist):
    global current_playlist
    current_playlist = []
    for url in playlist:
        # detect video name from URL
        match = re.search(r'(?<=v=)[^&#]+', url)
        if match:
            video_id = match.group(0)
            current_playlist.append(f"Video {len(current_playlist)+1}: {video_id}")
    print("Current Playlist:", current_playlist)

set_playlist(["Video 1", "Video 2", "Video 3"])

def set_repeat(repeat):
    # Get the currently selected source element
    selected_source = document.querySelector('video source[selected]')

    # Get the parent video element
    video = selected_source.parentNode

    # Set the repeat attribute to the provided value
    video.setAttribute('loop', str(repeat))

def set_shuffle(shuffle):
    # Check if shuffle is enabled or disabled
    if shuffle:
        # Enable shuffle
        random.shuffle(play_list)
        print("Shuffle enabled.")
    else:
        # Disable shuffle
        print("Shuffle disabled.")

def set_chapter(chapter):
    # Change current working directory to directory containing the video files
    os.chdir("path/to/video/files")
    
    # List all video files in the directory
    video_files = os.listdir()
    
    # Find the video file with the specified chapter in the filename
    for video_file in video_files:
        if f"chapter{chapter}" in video_file.lower():
            # Play the video file
            play_video(video_file)
            return
    
    # If no video file with the specified chapter was found, do nothing
    return
       

def get_time():
    current_time = datetime.datetime.now()
    return current_time.strftime("%H:%M:%S")

if __name__ == "__main__":
    root = tk.Tk()
    player_widget = VideoPlayerWidget(root)
    player_widget.pack()
    root.mainloop()

