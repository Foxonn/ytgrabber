from ytgrabber import YTGrabber
from ytdownloader import YTDownloader

with YTGrabber() as ytg:
    page = ytg('https://www.youtube.com/playlist?list=PLyIFQr1wryPIu-ta_1RTxj52EZo8CWH-K')

ytd = YTDownloader()
ytd.start(page)
