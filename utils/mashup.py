import os
import urllib.request
from urllib.parse import quote
from pydub import AudioSegment
from pytube import YouTube
import re
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
import shutil
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
HOST = os.environ.get("MAIL_HOST")
USERNAME = os.environ.get("MAIL_USERNAME")
PASSWORD = os.environ.get("MAIL_PASSWORD")
PORT = os.environ.get("MAIL_PORT")

def search_videos(search_term: str, num: int):
  search_term = search_term + str(" songs")
  encoded_query = quote(search_term)
  # print(encoded_query)
  html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + encoded_query)
  video_ids = list(set(re.findall(r"watch\?v=(\S{11})", html.read().decode())))
  video_links = []
  for id in range(int(num)):
    video_links.append("https://www.youtube.com/watch?v=" + video_ids[id])
  return video_links[0:num]

def clean_string(input_string: str):
    # Define the regular expression pattern
    pattern = r'[#@$%^&*()]+|\s+'
    
    # Use re.sub() to replace the matched characters with an empty string
    cleaned_string = re.sub(pattern, '', input_string)
    return cleaned_string

import sys
import os
from pytube import YouTube
from moviepy.editor import AudioFileClip
from pydub import AudioSegment
from pytube.exceptions import AgeRestrictedError

def download_audio_streams(video_urls):
    print("Downloading audio streams...")
    audio_streams = []

    for url in video_urls:
          try:
            yt = YouTube(url)
            stream = yt.streams.filter(only_audio=True).first()
            audio_streams.append(stream)
          except AgeRestrictedError:
            print(f"Video {url} is age-restricted. Skipping...")
            continue
    return audio_streams

def select_audio_duration(audio_streams ,time):
    print("Selecting appropriate audio duration...")
    selected_durations = []

    for audio_stream in audio_streams:
        print("hello")
        audio_file = audio_stream.download(output_path="audios", filename=f"audio_{audio_streams.index(audio_stream)+1}.mp3")
        audio = AudioFileClip(audio_file)
        duration = min(audio.duration, time)
        selected_durations.append(duration)
    print("helllo")

    return selected_durations


def send_email(email, subject, body, attachment_path):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] =USERNAME 
    msg['To'] = email
    msg['Subject'] = subject

    # Attach the text body
    msg.attach(MIMEText(body, 'plain'))

    # Attach the file
    with open(attachment_path, 'rb') as file:
        attachment = MIMEApplication(file.read(), Name="attachment")
        attachment['Content-Disposition'] = f'attachment; filename={attachment_path}'
        msg.attach(attachment)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(HOST, PORT) as server:
        server.starttls()
        server.login(USERNAME ,PASSWORD)
        server.sendmail(USERNAME , email, msg.as_string())


def merge_audio_streams(audio_streams, selected_durations, output_file , email):
    print("Merging audio streams...")
    combined_audio = AudioSegment.empty()

    for audio_stream, duration in zip(audio_streams, selected_durations):
        audio_file = audio_stream.download(output_path="audios", filename=f"audio_{audio_streams.index(audio_stream)+1}.mp4")
        audio = AudioSegment.from_file(audio_file)
        combined_audio += audio[:int(duration * 1000)]  # Convert seconds to milliseconds

    combined_audio.export(output_file, format="mp3")
    print(f"Output file '{output_file}' created successfully.")
    send_email(email , "Audio From Mashup Site" , "Enjoy your Mashup" , output_file)
    shutil.rmtree('audios')
    return