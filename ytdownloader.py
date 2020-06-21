import os
from slugify import slugify
from pytube import YouTube, Stream
from urllib.error import URLError
from time import sleep


class YTDownloader:
    __directory_save = None

    def set_directory_save(self, path):
        self.__directory_save = path

    def get_directory_save(self, path):
        return self.__directory_save

    @staticmethod
    def _sleep(wait: int):
        sleep_ = wait
        print("***** sleep %s sec. *****" % sleep_)
        sleep(sleep_)

    def start(self, page, type='audio'):
        self._download(page['videos'], page['channel'], page['playlist'], type)
        print('YTDownloader work complete.')

    def get_audio(self, link) -> Stream:
        yt = YouTube(link)
        return yt.streams.filter(only_audio=True).last()

    def get_video(self, link) -> Stream:
        yt = YouTube(link)
        return yt.streams.get_lowest_resolution()

    def check_files_is_downloaded(self, file_name):
        files = os.scandir(self.__path_destination)

        for file in files:
            if file_name == file.name.split(".")[0]:
                return True

        return False

    def _download(self, links: list, channel: str, playlist: str = None, type: str = 'audio'):
        self._check_directory(channel, playlist)

        for link in links:
            filename = slugify(link['title'])

            if self.check_files_is_downloaded(filename):
                print("Downloaded: %s" % link['href'])
                continue

            print("Start download: %s" % link['href'])

            if type == 'audio':
                while True:
                    try:
                        self.get_audio(link['href']).download(output_path=self.__path_destination, filename=filename)
                        break
                    except URLError as err:
                        print("Error: %s" % err)
                        self._sleep(10)

            elif type == 'video':
                while True:
                    try:
                        self.get_video(link['href']).download(output_path=self.__path_destination, filename=filename)
                        break
                    except URLError as err:
                        print("Error: %s" % err)
                        self._sleep(10)

            print("Download complete: %s" % link['href'])

    def _check_directory(self, channel, playlist: str = None):
        channel = slugify(channel).lower()
        playlist = slugify(playlist).lower() if playlist else None

        if self.__directory_save:
            if os.path.isdir(self.__directory_save):

                if playlist:
                    self.__path_destination = os.path.join(self.__directory_save, channel, playlist)
                else:
                    self.__path_destination = os.path.join(self.__directory_save, channel)

                if not os.path.isdir(self.__path_destination):
                    os.makedirs(self.__path_destination)
        else:
            if playlist:
                self.__path_destination = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', channel, playlist)
            else:
                self.__path_destination = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', channel)

            if not os.path.isdir(self.__path_destination):
                os.makedirs(os.path.realpath(self.__path_destination))

        return self.__path_destination


if __name__ == '__main__':
    ytd = YTDownloader()

    _ = {
        "videos": [{"href": "https://youtu.be/ZLjX1HmccvU?list=PLyIFQr1wryPKfm76f3TkP61TaUJb049p5",
                    "title": "Flux Gemini - Andromeda"}],
        "channel": "NewRetroWave2",
        "playlist": "NRW Presents: Supreme Spacewave",
    }

    ytd.start(_)
