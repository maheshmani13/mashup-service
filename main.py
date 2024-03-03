from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from utils.mashup import search_videos, merge_audio_streams , select_audio_duration , download_audio_streams, send_email
from model.form import Form
from fastapi.middleware.cors import CORSMiddleware
import random
import shutil
random.seed(5)
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.mount("/static", StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')
@app.route("/", methods=["GET", "POST"])
def main(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")
@app.post("/submitform")
def util(data:Form):
    name = data.name
    email = data.email
    num_videos = data.num_videos
    duration= data.duration
    print(name, email, num_videos, duration)
    temp_folder = f"fold{random.randint(10000000, 99999999)}"
    print(temp_folder)
    video_links = search_videos(name, num_videos)
    print(video_links)
    streams =  download_audio_streams(video_links)
    selected =  select_audio_duration(streams, duration)
    merge_audio_streams(streams ,selected ,f'audios/audio{temp_folder}.mp3' , email)
    
    
    return RedirectResponse(url="/")