import sys
import youtube_dl


# url = 'https://www.youtube.com/watch?v=e9BLw4W5KU8'
# url = 'https://www.youtube.com/watch?v=X-KwYX2u8e4'
# url = 'https://www.youtube.com/watch?v=dGfdGZ8cH-o'

url = sys.argv[1]
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '-',
    #'ignoreerrors': True,
    'quiet': True,
    'ratelimit': 1048576,   # 1Mb/sec
    'buffersize': 4194304,  # 4Mb
    'noresizebuffer': True
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    file = ydl.extract_info(url, download=True)

