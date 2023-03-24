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

root = tk.Tk()
root.title("Video Player")



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
     
        thumbnail_label = ttk.Label(root, image=thumbnail)
        thumbnail_label.pack(side='left', padx=10, pady=10)  # Change the parameters to adjust placement and padding
        thumbnail_label.grid(row=1, column=0, padx=10, pady=10)  # Change the parameters to adjust placement and padding
      
     
        self.parent = parent
        self.video_path = video_path
        self.thumbnail_dir = thumbnail_dir
        self.thumbnail_images = []
        self.thumbnail_widget = tk.Label(self, bg='black')
        self.thumbnail_widget.pack(side='left')
        self.progressbar = ttk.Scale(self, orient='horizontal', from_=0, to=100, command=self.on_seek)
        self.progressbar.pack(fill='x')
        self.current_time_label = tk.Label(self, text='0:00')
        self.current_time_label.pack(side='left')
        self.duration_label = tk.Label(self, text='0:00')
        self.duration_label.pack(side='right')
        self.play_button = tk.Button(self, text='Play', command=self.on_play_pause)
        self.play_button.pack(side='left')
        self.mute_button = tk.Button(self, text='Mute', command=self.on_mute_unmute)
        self.mute_button.pack(side='right')
        self.volume_slider = ttk.Scale(self, orient='horizontal', from_=0, to=100, command=self.on_volume_change)
        self.volume_slider.pack(side='right')
        self.volume_slider.set(50)
        self.playback_speed_var = tk.StringVar(value='1x')
        self.playback_speed_menu = tk.OptionMenu(self, self.playback_speed_var, '0.25x', '0.5x', '1x', '1.25x', '1.5x', '2x', command=self.on_playback_speed_change)
        self.playback_speed_menu.pack(side='right')
        self.is_playing = False
        self.is_muted = False
        self.playback_speed = 1.0
        self.create_video_player()
        self.load_thumbnail_images()
        self.update_ui()
        self.bind('<Enter>', self.on_hover)
        self.bind('<Leave>', self.on_leave)


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

# replace this with the URL of the webpage containing the video
url = "https://www.example.com"

# send a GET request to the webpage
response = requests.get(url)

# open the URL and read its content
response = urlopen(url)
html_content = response.read()

# create a BeautifulSoup object
soup = BeautifulSoup(html_content, 'html.parser')

# use BeautifulSoup to parse HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# find the video element on the webpage and extract its source URL
video_element = soup.find('video')
if video_element is not None:
    video_url = video_element.get('src')
    if video_url is not None:
        file_extension = os.path.splitext(video_url)[1]
        if file_extension in ['.mp4', '.mkv']:
            # process and play the video file
            pass
        else:
            print('Invalid file format')
    else:
        print('Video URL not found')
else:
    print('Video element not found')




# find the video element on the webpage and extract its source URL
video_element = soup.find('video')
video_url = video_element['src']



# determine the file extension of the video by looking at the URL
file_extension = os.path.splitext(video_url)[1]

# call the play_video function with the video URL
play_video(video_url)

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

def play_video(file_path):
    # check if file is a local video file
    if os.path.isfile(file_path):
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
    # check if file is a YouTube video
    elif 'youtube.com' in file_path:
        video = pafy.new(file_path)
        best = video.getbest(preftype="mp4")
        url = best.url
        # download video as bytes
        video_bytes = urlopen(url).read()
        # convert bytes to audio data for playback
        audio_data = pydub.AudioSegment.from_file(BytesIO(video_bytes)).raw_data
        # convert audio data to numpy array
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        # play audio with sounddevice
        sd.play(audio_array, video.fps)
        sd.wait()
    # check if file is from another source
    else:
        # process and play video using appropriate library or command line tool
        pass
        
        # generate thumbnail from video file
        thumbnail = generate_thumbnail(video_path)
        thumbnail_img = Image.fromarray(thumbnail)
        
        # create label to display thumbnail
        thumbnail_label.configure(image=thumbnail_img)
        thumbnail_label.image = thumbnail_img
        
      # play clip when hovering over thumbnail
thumbnail_label.bind("<Enter>", lambda event: play_video(video_path))

# check file extension
ext = os.path.splitext(video_path)[1]

# select appropriate processing and playback functions based on file extension
if ext in ['.mp4', '.mov', '.avi']:
    play_video(video_path)
elif ext == '.mkv':
    # process and play MKV video using appropriate library or command line tool
    pass
else:
    print('Invalid file format')



# define function to play a 10 second clip when hovering over thumbnail
def play_clip(video_path):
    clip = mp.VideoFileClip(video_path).subclip(0, 10)
    clip.preview(fps=25)

# get video path or URL from user
source = input("Enter video path or URL: ")

# check if source is a URL
if source.startswith("http"):
    try:
        # extract video URL from webpage using BeautifulSoup
        html = urlopen(source)
        soup = BeautifulSoup(html, 'html.parser')
        video_element = soup.find('video')
        video_url = video_element['src']
    except:
        print('Error: could not extract video URL from webpage')
else:
    # assume source is a local file path
    video_path = source
    ext = os.path.splitext(video_path)[1]
    if ext == '.mp4':
        # play MP4 video clip using pydub and sounddevice
        thumbnail_label.bind("<Enter>", lambda event: play_clip(video_path))
    elif ext == '.mkv':
        # process and play MKV video using appropriate library or command line tool
        pass
    else:
        print('Invalid file format')
        sys.exit()
        
    # exit after video is finished playing
    while True:
        if not sd.get_stream_active(stream):
            break
        time.sleep(1)

def select_video():
    video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.mov *.avi")])
    if video_path:
        play_video(video_path)

select_button = ttk.Button(root, text="Select Video", command=select_video)
select_button.pack()

root.mainloop()

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

