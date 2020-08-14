from downloader import get_audio
from converter import convert
from slugify import slugify

audio = get_audio(r"https://www.youtube.com/watch?v=rDBbaGCCIhk")

path_destination = r'D:\music\newretrowave'
filename = slugify(audio.title)

path_to_file = "\\".join([path_destination, filename])

audio.download(
    output_path=path_destination,
    filename=filename
)

convert(
    dir_files=path_destination,
    remove=True
)
