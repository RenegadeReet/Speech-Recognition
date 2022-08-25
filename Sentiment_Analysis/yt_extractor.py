import youtube_dl

Yt = youtube_dl.YoutubeDL()

def get_video_info(url):
    with Yt:
        result = Yt.extract_info(url , download=False)

    if "entries" in result:
        return result["entries"][0]
    return result

def get_audio_url( video_info ):
    for f in video_info["formats"]:
        if f["ext"]=="m4a":
            return f["url"]

if __name__=="__main__":
    video_info = get_video_info("https://www.youtube.com/watch?v=H9WhjkwqntE")
    get_audio_url(video_info)

