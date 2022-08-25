from api import save_transcript
from yt_extractor import get_audio_url , get_video_info

def save_video_sentiments(url):
    video_info = get_video_info(url)
    audio_url = get_audio_url(video_info)
    title = video_info["title"]
    title = title.replace(" " , "_")
    title = "data_" + title
    save_transcript(audio_url , title , sentiment_analysis=True)

if __name__ == "__main__":
    save_video_sentiments("https://www.youtube.com/watch?v=H9WhjkwqntE")
