from grabber import YTGrabber
from downloader import start_download
from converter import convert

datas: YTGrabber = None

with YTGrabber() as ytg:
    datas = ytg('https://www.youtube.com/playlist?list='
                'PLyIFQr1wryPKTGEB3dNxktq2htXoRetIV')

path_destination = start_download(
    datas=datas,
    to_save=r'D:\music'
)

convert(
    dir_files=path_destination,
    remove=True
)
