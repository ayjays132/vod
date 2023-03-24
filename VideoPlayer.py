import os
import pyav
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
from js import document
import cv2
import random

class VideoPlayer(Frame):
    def __init__(self, master, video_path):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
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
        self.progress_bar = ttk.Progressbar(self, orient=HORIZONTAL, length=200, mode='determinate')
        self.progress_bar.pack()

        # Create a volume control slider
        self.volume_slider = ttk.Scale(self, from_=0, to=100, orient=HORIZONTAL, command=self.set_volume)
        self.volume_slider.pack()

         # Create a Scale widget for volume control
        self.volume_scale = ttk.Scale(self.controls_frame, from_=0, to=1, orient="horizontal", value=self.player.audio_get_volume(), command=self.set_volume)
        self.volume_scale.pack(side="left", padx=5)

        # Set the initial volume level
        self.volume = self.player.audio_get_volume()

            

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

# Automatically detect the video path and format
video_path = input("Enter the video path: ")

if os.path.isfile(video_path) and mimetypes.guess_type(video_path)[0].startswith('video/'):
    video_format = os.path.splitext(video_path)[1].lower()
    print(f"Detected video format: {video_format}")

    # Play the video
    play_video(video_path)

    # Edit the video
    edited_video_path = f"edited_video{video_format}"
    edit_video(video_path, edited_video_path)

    # Play the edited video
    play_video(edited_video_path, f"edited_video{video_format}")
else:
    print("Invalid video file path.")



# define function to generate thumbnail from video file
def generate_thumbnail(video_path):
    clip = mp.VideoFileClip(video_path)
    thumbnail = clip.subclip(0, 1).resize((320, 240)).to_RGB()
    return thumbnail

def play_video(video_path):
    # Attempt to open the video file
    try:
        video = cv2.VideoCapture(video_path)
    except Exception as e:
        print(f"Error opening video file: {e}")
        return

    # Check if the video file was successfully opened
    if not video.isOpened():
        print("Error opening video file.")
        return

    # Create a window for the video player
    cv2.namedWindow("Video Player", cv2.WINDOW_NORMAL)

    # Play the video
    while True:
        # Read a frame from the video
        ret, frame = video.read()

        # Check if the frame was successfully read
        if not ret:
            break

        # Show the frame in the video player window
        cv2.imshow("Video Player", frame)

        # Check if a key was pressed
        key = cv2.waitKey(1) & 0xFF

        # Stop the video if the 'q' key is pressed
        if key == ord('q'):
            break

    # Release the video file and close the window
    video.release()
    cv2.destroyAllWindows()


# define function to play a 10 second clip when hovering over thumbnail
def play_clip(video_path):
    clip = mp.VideoFileClip(video_path).subclip(0, 10)
    clip.preview(fps=25)

def select_video():
    global cap
    # open file dialog to select video file
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mkv")])
    
    # check file extension
    ext = os.path.splitext(file_path)[1]
    
    # select appropriate processing and playback functions based on file extension
    if ext == '.mp4' or ext == '.avi':
        cap = cv2.VideoCapture(file_path)
        while True:
            ret, frame = cap.read()
            if ret:
                # pause video if paused flag is set
                if paused:
                    continue
                cv2.imshow('Video Player', frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()
        
        # generate thumbnail from video file
        thumbnail = generate_thumbnail(file_path)
        Image.fromarray(thumbnail)
        
        # create label to display thumbnail
        thumbnail_label = ttk.Label(root, image=thumbnail)
        thumbnail_label.grid(row=0, column=0)
        
        # play clip when hovering over thumbnail
        thumbnail_label.bind("<Enter>", lambda event: play_clip(file_path))
    elif ext == '.mkv':
        # process and play MKV video using appropriate library or command line tool
        pass
    else:
        print('Invalid file format')
        
# create button to select video file
select_button = ttk.Button(root, text="Select Video", command=select_video)
select_button.grid(row=1, column=0)

        
def play_video():
    global paused
    paused = False

def pause_video():
    global paused
    paused = True

def stop_video():
    global cap
    if cap is not None:
        cap.release()
        cv2.destroyAllWindows()
        cap = None

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

# extract the URL from the player element
video_url = player.get_attribute('src')

# pop out the video player
driver.execute_script('window.open(arguments[0], "_blank", "height=480,width=640")', video_url)

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

