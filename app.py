from grabber import YTGrabber
from downloader import YTDownloader
from converter import YTConverter

with YTGrabber() as ytg:
    page = ytg('https://www.youtube.com/playlist?list=PLyhufYmBlouSGqOqpIiX9CogKOalmTfeV')

ytd = YTDownloader()
ytd.set_directory_save("D:\music")
ytd.start(page)

ytc = YTConverter(ytd.get_path_destination())
ytc.convert()