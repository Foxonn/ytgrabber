import os
from slugify import slugify
import pytube
from pytube import exceptions
from urllib.error import URLError
from time import sleep
from exception import VideoPermissionDenied


class YTDownloader:
    """
    Downloading audio track from YouTube video file.
    __call__ take YTGrabber dictionary.
    """
    __directory_save: str = None

    def set_directory_save(self, path: str):
        self.__directory_save = path

    def get_directory_save(self):
        return self.__directory_save

    def get_path_destination(self):
        return os.path.realpath(self.__path_destination)

    def get_audio(self, link) -> pytube.Stream:
        yt = pytube.YouTube(link)
        return yt.streams.filter(only_audio=True).last()

    def get_video(self, link: str) -> pytube.Stream:
        yt = pytube.YouTube(link)
        return yt.streams.get_lowest_resolution()

    def start(self, videos: dict, type='audio') -> None:
        self._download(videos['videos'], videos['channel'], videos['playlist'], type)
        print('YTDownloader work complete.')

    def _check_files_is_downloaded(self, file_name) -> bool:
        files = os.scandir(self.__path_destination)

        for file in files:
            if file_name == file.name.split(".")[0]:
                return True

        return False

    def _download(self, links: list, channel: str, playlist: str = None, type: str = 'audio') -> None:
        if not type in ['audio', 'video']:
            raise ValueError("Type '%s' not support." % type)

        self._check_directory(channel, playlist)

        for link in links:
            filename = slugify(link['title'])

            if self._check_files_is_downloaded(filename):
                print("Downloaded: %s" % link['href'])
                continue

            print("Start download: %s" % link['href'])

            while True:
                try:
                    if type == 'audio':
                        self.get_audio(link['href']).download(output_path=self.__path_destination, filename=filename)
                    elif type == 'video':
                        self.get_video(link['href']).download(output_path=self.__path_destination, filename=filename)

                    print("Download complete: %s" % link['href'])
                    break
                except exceptions.RegexMatchError:
                    print(VideoPermissionDenied())
                    break
                except URLError as err:
                    print("Error: %s" % err)
                    self._sleep(10)

    def _check_directory(self, channel, playlist: str = None) -> str:
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
                NotADirectoryError(self.__directory_save)
        else:
            if playlist:
                self.__path_destination = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', channel,
                                                       playlist)
            else:
                self.__path_destination = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', channel)

            if not os.path.isdir(self.__path_destination):
                os.makedirs(os.path.realpath(self.__path_destination))

        return self.__path_destination

    @staticmethod
    def _sleep(wait: int):
        sleep_ = wait
        print("***** sleep %s sec. *****" % sleep_)
        sleep(sleep_)


if __name__ == '__main__':
    ytd = YTDownloader()

    videos = {
        "videos": [
            {"href": "https://www.youtube.com/watch?v=b6J7aez8-qU&list=PLyIFQr1wryPKdWJzPV-bRccsnJqbNP1a6&index=21",
             "title": "Flux Gemini - Andromeda"}],
        "channel": "NewRetroWave",
        "playlist": "NRW Presents: Supreme Spacewave",
    }

    ytd.set_directory_save(path="D:\music")
    ytd.start(videos=videos, type='audio')
