from pydantic import BaseModel


class Form(BaseModel):
    name: str
    email: str
    num_videos: int
    duration: int