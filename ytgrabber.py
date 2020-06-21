import re
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions

from ytexception import PageNotFound, PageOops


def _run_from_ipython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False


if _run_from_ipython():
    from xvfbwrapper import Xvfb


class YTGrabber:
    '''
    Класс принимает Youtube URL страниц, плейлист и видео,
    и возваращает все видеоматериалы данной страницы.
    '''

    __SELECTOR_PLAYLIST_VIDEOS = "#contents #contents #contents > *"
    __SELECTOR_ALL_VIDEOS = "#contents #contents #items > *"
    __SELECTOR_SPINNER = "#contents #contents #continuations #spinner"
    __SELECTOR_NAME_PLAYLIST = ".yt-simple-endpoint.style-scope.yt-formatted-string"
    __SELECTOR_CHANNEL_NAME = ".style-scope.ytd-channel-name"

    @staticmethod
    def _run_from_ipython():
        try:
            __IPYTHON__
            return True
        except NameError:
            return False

    def _check_os_name(self):
        if os.name == 'nt':
            self.__executable_path = "driver/chromedriver.exe"
        else:
            self.__executable_path = "driver/chromedriver"

    def _check_valid_url(self, url):

        if type(url) is int:
            raise TypeError("URL is not to be int type!")

        self.__url = url.strip()

        if re.match(r"^https://www\.youtube\.com/user/[\W\w]+/videos$", self.__url):
            return True

        if re.match(r"^https://www\.youtube\.com/(playlist\?list=|channel/)[\W\w]+(/playlists|/videos)$", self.__url):
            return True

        if re.match(r"https://www\.youtube\.com/(playlist\?list=|channel/)[\W\w]+", self.__url):
            return True

        raise ValueError("URL is not correct!")

    def _find_html_block(self):
        self.__html = WebDriverWait(self.__driver, 3).until(
            EC.presence_of_element_located((By.TAG_NAME, "html")),
            "`html` tag not found !")

    def _get_page(self, url):
        self._check_valid_url(url)

        resp = requests.get(self.__url, allow_redirects=True)

        if resp.text.find("404 Not Found") >= 0:
            raise PageNotFound

        if resp.url == 'https://www.youtube.com/oops':
            raise PageOops

        self.__driver.get(self.__url)

    def _preloader_handler(self):
        while True:
            self.__html.send_keys(Keys.END)
            try:
                WebDriverWait(self.__driver, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, self.__SELECTOR_SPINNER))
                )
            except:
                break

    def _find_videos(self):
        videos = self.__html.find_elements(By.CSS_SELECTOR, self.__SELECTOR_ALL_VIDEOS)

        if not videos:
            videos = self.__html.find_elements(By.CSS_SELECTOR, self.__SELECTOR_PLAYLIST_VIDEOS)

        if not videos:
            raise Exception("Videos not found !")

        return videos

    def _find_name_playlist(self):
        return self.__html.find_elements(By.CSS_SELECTOR, self.__SELECTOR_NAME_PLAYLIST)[0] or None

    def _find_name_channel(self) -> str:
        channel_name = self.__html.find_elements(By.CSS_SELECTOR, self.__SELECTOR_CHANNEL_NAME)[2]

        if not channel_name.text:
            raise Exception("Channel name not found !")

        return channel_name

    def get_content(self, url):
        self._get_page(url)

        self._find_html_block()

        videos = self._find_videos()

        channel_name = self._find_name_channel()

        playlist_name = self._find_name_playlist()

        content = {
            "playlist": playlist_name.text if playlist_name else None,
            "channel": channel_name.text,
            "videos": [],
        }

        for video in videos:
            content['videos'].append({
                "title": video.find_element_by_id("video-title").get_attribute("title"),
                "href": video.find_element_by_id("video-title").get_attribute("href") or
                        video.find_element_by_class_name("ytd-thumbnail").get_attribute("href"),
                "thumbnail": video.find_element_by_id("img").get_attribute("src"),
            })

        return content

    def __init__(self):
        self.__driver = None
        self.__vdisplay = None

    def __call__(self, url):
        return self.get_content(url)

    def __enter__(self):
        if _run_from_ipython():
            self.__vdisplay = Xvfb()
            self.__vdisplay.start()

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")

        self._check_os_name()

        self.__driver = webdriver.Chrome(options=options, executable_path=self.__executable_path)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("YTGrabber finished working.")

        if self.__driver:
            self.__driver.close()

        if _run_from_ipython() and self.vdisplay:
            self.__vdisplay.stop()


if __name__ == '__main__':
    with YTGrabber() as yt:
        print(yt('https://www.youtube.com/user/FlandyMusic/videos'))
        print(yt('https://www.youtube.com/playlist?list=PLnwx-Ko_Jo_360x-41QTqiiG7lTWGn-Tp'))
