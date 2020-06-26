from grabber import YTGrabber
from downloader import YTDownloader
from converter import YTConverter

with YTGrabber() as ytg:
    page = ytg('https://www.youtube.com/playlist?list=PLyIFQr1wryPIw7xkMZH_HXmkQbXhZyOMJ')

ytd = YTDownloader()
ytd.set_directory_save("D:\music")
ytd.start(page)

YTConverter.convert(ytd.get_path_destination())
